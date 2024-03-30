import asyncio
from enum import Enum
import logging
from typing import AsyncGenerator, Optional

import aiohttp

from SunGrowDataCollector.Core.BackgroundService import BackgroundService
from SunGrowDataCollector.Client.Messages.ConnectMessage import ConnectRequest, ConnectResponse
from SunGrowDataCollector.Client.Configuration import Configuration
from SunGrowDataCollector.Client.Messages.BaseMessage import RequestBase, ResponseBase
from SunGrowDataCollector.Client.Services.IManagedConnection import IManagedConnection

_LOGGER = logging.getLogger(__name__)

class ConnectionState(Enum):
    DISCONNECTED = 0
    LINKESTABLISHING = 1
    CONNECTING = 2
    CONNECTED = 3
    FAULTED = 4

class ManagedConnection(BackgroundService, IManagedConnection):
    """Represents a managed connection to a WebSocket server.

    This class manages the connection state and provides methods for connecting,
    establishing the connection, sending and receiving messages, and disconnecting.

    Args:
        configuration (Configuration): The configuration object for the connection.

    Attributes:
        State (ConnectionState): The current state of the connection.

    """

    def __init__(self, configuration: Configuration):
        super().__init__()
        self._state = ConnectionState.DISCONNECTED
        self._configuration = configuration

    @property
    def State(self):
        """Get the current state of the connection.

        Returns:
            ConnectionState: The current state of the connection.

        """
        return self._state

    async def Connect(self):
        """Connect to the WebSocket server.

        This method establishes a connection to the WebSocket server using the
        configuration provided during initialization.

        """
        _LOGGER.info(f"Connecting to {self._configuration.GenerateWebsocktUri()}")
        self._session = aiohttp.ClientSession()
        self._ws = await self._session.ws_connect(self._configuration.GenerateWebsocktUri())
        self._state = ConnectionState.LINKESTABLISHING

    async def Establish(self):
        """Establish the connection.

        This method sends a connect request to the WebSocket server to establish
        the connection.

        """
        if self._session.closed or self._ws.closed:
            _LOGGER.error(f"Connection closed before establishing, setting connection as faulted")
            self._state = ConnectionState.FAULTED
            return
        
        _LOGGER.info("Establishing connection")
        request = ConnectRequest(self._configuration.LANG, self._configuration.TOKEN)
        await self._ws.send_json(request.Serialise())
        self._state = ConnectionState.CONNECTING

    def CheckConnection(self):
        """Check the connection status.

        This method checks if the connection is still active and updates the
        connection state accordingly.

        """
        if self._state == ConnectionState.CONNECTED and self._ws.closed:
            _LOGGER.error(f"Websocket Connection closed, setting connection as faulted")
            self._state = ConnectionState.FAULTED

    async def Disconnect(self):
        """Disconnect from the WebSocket server.

        This method closes the WebSocket connection and releases the associated
        resources.

        """
        _LOGGER.info("Disconnecting")
        await self._ws.close()
        await self._session.close()
        self._state = ConnectionState.DISCONNECTED

    async def Execute(self):
        """Execute the managed connection.

        This method continuously checks the connection state and performs the
        necessary actions (connect, establish, disconnect) based on the state.

        """
        while self.IsStopRequested() != True:
            if self._state == ConnectionState.DISCONNECTED:
                await self.Connect()
            elif self._state == ConnectionState.LINKESTABLISHING:
                await self.Establish()
            elif self._state == ConnectionState.FAULTED:
                await self.Disconnect()
            else:
                self.CheckConnection()

            await asyncio.sleep(1)

        _LOGGER.info("Stopping ManagedConnection")
        await self.Disconnect()

    async def SendMessage(self, message: RequestBase):
        """Send a message to the WebSocket server.

        Args:
            message (RequestBase): The message to send.

        """
        if self._state == ConnectionState.CONNECTED:
            _LOGGER.debug(f"Sending message")
            try:
                await self._ws.send_json(message.Serialise())
            except ConnectionResetError:
                _LOGGER.error(f"Connection reset error, setting connection as faulted")
                self._state = ConnectionState.FAULTED
                

    def ProcessConnectMessage(self, responseBase: ResponseBase):
        """Process a connect message.

        This method processes a connect message received from the WebSocket server
        and updates the connection state accordingly.

        Args:
            responseBase (ResponseBase): The connect message response.

        """
        response = ConnectResponse(responseBase)
        if response.Validate():
            if response.message == "success":
                self._state = ConnectionState.CONNECTED
                _LOGGER.info(f"Connection established with data {response._data}")
            else:
                self._state = ConnectionState.FAULTED

    def PreprocessMessage(self, message: aiohttp.WSMessage) -> Optional[ResponseBase]:
        """Preprocess a message received from the WebSocket server.

        This method preprocesses the message to ensure it is a valid response.
        If it's a connect message, it processes it and updates the connection state.
        Otherwise, it returns the response.

        Args:
            message (aiohttp.WSMessage): The raw message from the WebSocket server.

        Returns:
            Optional[ResponseBase]: A valid response if the message is valid, otherwise None.

        """
        response = ResponseBase.Deserialise(message.json())
        if response is not None:
            if response.service == "connect":
                self.ProcessConnectMessage(response)
                return None
            if response.service == "notice":
                _LOGGER.warn(f"Notice message received: {message.json()}")
                return response

            return response
        else:
            _LOGGER.error(f"Invalid message received: {message.json()}")
            return None

    async def GetMessages(self) -> AsyncGenerator[ResponseBase, None]:
        """Get all messages from the WebSocket server.

        This method retrieves all messages from the WebSocket server and yields
        the valid response messages.

        Returns:
            AsyncGenerator[ResponseBase, None]: A generator of valid response messages.

        """
        if self._state == ConnectionState.DISCONNECTED:
            return

        async for message in self._ws:
            if message.type == aiohttp.WSMsgType.TEXT:
                output_message = self.PreprocessMessage(message)
                if output_message is not None:
                    yield output_message
                    

            
