"""Version information for the package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("steam-playtime-docker")
except PackageNotFoundError:
    __version__ = "0.0.0"
