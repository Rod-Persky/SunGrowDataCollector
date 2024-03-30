from SunGrowDataCollector.Client.Messages.BaseMessage import ResponseBase


from abc import ABC, abstractmethod


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