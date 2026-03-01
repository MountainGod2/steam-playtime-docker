"""FastAPI service that aggregates total playtime from the Steam Web API."""


from .main import app
from .version import __version__

__all__ = ["__version__", "app"]
