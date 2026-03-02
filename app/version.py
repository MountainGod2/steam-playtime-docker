"""Version information for the package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("steam-playtime-docker")
    """__version__: The current version of the package."""
except PackageNotFoundError:
    __version__ = "0.0.0"
    """__version__: Default version set to '0.0.0'."""
