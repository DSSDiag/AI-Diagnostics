import os
import importlib
import pytest
import src.storage

def test_data_file_env_var(monkeypatch):
    """Test that DATA_FILE respects the DIAGNOSTICS_DATA_FILE environment variable."""

    # Set the environment variable
    custom_data_file = "custom_data.json"
    monkeypatch.setenv("DIAGNOSTICS_DATA_FILE", custom_data_file)

    # Reload the module to pick up the environment variable
    importlib.reload(src.storage)

    # Check if DATA_FILE is updated
    assert src.storage.DATA_FILE == custom_data_file

def test_data_file_default(monkeypatch):
    """Test that DATA_FILE defaults to diagnostics_data.json when env var is not set."""

    # Ensure the environment variable is not set
    monkeypatch.delenv("DIAGNOSTICS_DATA_FILE", raising=False)

    # Reload the module to pick up the default
    importlib.reload(src.storage)

    # Check if DATA_FILE is the default
    assert src.storage.DATA_FILE == "diagnostics_data.json"
