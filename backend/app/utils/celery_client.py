from celery import Celery

class CeleryClient:
    def __init__(self, name: str, broker_url: str, backend_url: str):
        """
        Initializes the Celery client.

        Args:
            name (str): Name of the Celery app.
            broker_url (str): URL of the message broker (Redis in this case).
            backend_url (str): URL of the result backend.
        """
        self.app = Celery(
            name,
            broker=broker_url,
            backend=backend_url,
        )

    @classmethod
    def get_app(cls, name: str, broker_url: str, backend_url: str):
        """
        Returns the Celery app.

        Args:
            name (str): Name of the Celery app.
            broker_url (str): URL of the message broker (Redis in this case).
            backend_url (str): URL of the result backend.

        Returns:
            Celery: Celery app.
        """
        return cls(name, broker_url, backend_url).app    
