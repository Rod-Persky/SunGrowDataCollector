from abc import ABC, abstractmethod
from SunGrowDataCollector.Messages.BaseMessage import RequestBase, ResponseBase

class IMessageRouter(ABC):
    """Interface for message routing."""

    @abstractmethod
    async def RouteMessage(self, message : ResponseBase):
        """Routes the given message to the appropriate destination.

        Args:
            message (ResponseBase): The message to be routed.

        Returns:
            None
        """
        pass
    
    
class IMessageHandler(ABC):
    """Interface for message handlers."""

    @abstractmethod
    async def HandleMessage(self, message: ResponseBase) -> bool:
        """Handle the given message.

        Args:
            message (ResponseBase): The message to handle.

        Returns:
            bool: True if the message was handled successfully, False otherwise.
        """
        pass
class IMessageHandler(ABC):
    @abstractmethod
    async def HandleMessage(self, message : ResponseBase) -> bool:
        pass


class IManagedConnection(ABC):
    """Interface for a managed connection."""

    @abstractmethod
    async def SendMessage(self, message: RequestBase):
        """Send a message through the connection."""
        pass

