import os
import importlib
import pytest
import sys
from unittest.mock import MagicMock

# Mock streamlit before importing app
mock_st = MagicMock()

def mock_columns(spec):
    if isinstance(spec, int):
        return [MagicMock() for _ in range(spec)]
    elif isinstance(spec, list):
        return [MagicMock() for _ in range(len(spec))]
    return [MagicMock(), MagicMock()]

mock_st.columns.side_effect = mock_columns
mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
mock_st.query_params = {}
mock_st.form_submit_button.return_value = False
mock_st.button.return_value = False
mock_st.checkbox.return_value = False
mock_st.text_input.return_value = ""
mock_st.selectbox.return_value = "Select Year"
mock_st.number_input.return_value = 0
mock_st.text_area.return_value = ""
mock_st.date_input.return_value = None
mock_st.file_uploader.return_value = None

sys.modules["streamlit"] = mock_st

import app

def test_expert_password_env_var(monkeypatch):
    """Test that EXPERT_PASSWORD respects the environment variable."""
    custom_password = "custom_expert_pw"
    monkeypatch.setenv("EXPERT_PASSWORD", custom_password)

    # Reload the module to pick up the environment variable
    importlib.reload(app)

    assert app.EXPERT_PASSWORD == custom_password

def test_admin_password_env_var(monkeypatch):
    """Test that ADMIN_PASSWORD respects the environment variable."""
    custom_password = "custom_admin_pw"
    monkeypatch.setenv("ADMIN_PASSWORD", custom_password)

    # Reload the module to pick up the environment variable
    importlib.reload(app)

    assert app.ADMIN_PASSWORD == custom_password

def test_passwords_none_when_env_not_set(monkeypatch):
    """Test that passwords are None when environment variables are not set."""
    monkeypatch.delenv("EXPERT_PASSWORD", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

    # Reload the module to pick up the changes
    importlib.reload(app)

    assert app.EXPERT_PASSWORD is None
    assert app.ADMIN_PASSWORD is None
