from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from SunGrowDataCollector.Client.Messages.BaseMessage import ResponseBase

T = TypeVar('T', bound=ResponseBase)

class IMessageHandler(ABC, Generic[T]):
    """Interface for message handlers."""
    
    @abstractmethod
    async def OnMessage(self, message: T):
        pass

    @abstractmethod
    async def HandleMessage(self, message: ResponseBase) -> bool:
        """Handle the given message.

        Args:
            message (ResponseBase): The message to handle.

        Returns:
            bool: True if the message was handled successfully, False otherwise.
        """
        pass