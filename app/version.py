"""Version information for the package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("steam-playtime-docker")
    """str: The current version of the package."""
except PackageNotFoundError:
    __version__: str = "0.0.0"
    """str: Default version set to '0.0.0'."""
