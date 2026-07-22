"""Startup behavior tests."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.dependencies import get_settings
from app.main import app


def test_app_startup_fails_without_required_steam_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Startup should fail fast when required Steam settings are missing."""
    # Run from an empty directory so Settings can't fall back to project .env values.
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("STEAM_API_KEY", raising=False)
    monkeypatch.delenv("STEAM_ID_64", raising=False)
    get_settings.cache_clear()

    with pytest.raises(ValidationError) as error_info, TestClient(app):
        pass

    error_text = str(error_info.value)
    assert "STEAM_API_KEY" in error_text
    assert "STEAM_ID_64" in error_text
