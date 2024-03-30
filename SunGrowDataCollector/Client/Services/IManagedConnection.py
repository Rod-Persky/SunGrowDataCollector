from abc import ABC, abstractmethod

from SunGrowDataCollector.Client.Messages.BaseMessage import RequestBase


class IManagedConnection(ABC):
    """Interface for a managed connection."""

    @abstractmethod
    async def SendMessage(self, message: RequestBase):
        """Send a message through the connection."""
        pass