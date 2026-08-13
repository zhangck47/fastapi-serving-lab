"""Pytest configuration shared by the test suite."""

import os
from pathlib import Path

import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Keep Windows test temp directories separate for each login identity."""

    if config.option.basetemp is not None:
        return

    try:
        login_name = os.getlogin()
    except OSError:
        login_name = "current-user"

    safe_login_name = "".join(
        character if character.isalnum() or character in "-_" else "_"
        for character in login_name
    )
    config.option.basetemp = Path(f".pytest-tmp-{safe_login_name}")
