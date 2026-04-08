import sys
from unittest.mock import MagicMock, patch
import os
import importlib
import pytest

def test_expert_password_env_var(monkeypatch):
    """Test that EXPERT_PASSWORD respects the EXPERT_PASSWORD environment variable."""
    # Mock streamlit and other modules locally to avoid affecting other tests
    with patch.dict(sys.modules, {
        "streamlit": MagicMock(),
        "src.storage": MagicMock(),
        "src.validation": MagicMock()
    }):
        # Mock st.columns and st.tabs
        import streamlit as st
        st.columns.side_effect = lambda spec: [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
        st.tabs.side_effect = lambda tabs: [MagicMock() for _ in range(len(tabs))]
        st.selectbox.return_value = "Select Year"

        custom_password = "custom_expert_pass"
        monkeypatch.setenv("EXPERT_PASSWORD", custom_password)

        import app
        importlib.reload(app)
        assert app.EXPERT_PASSWORD == custom_password

def test_admin_password_env_var(monkeypatch):
    """Test that ADMIN_PASSWORD respects the ADMIN_PASSWORD environment variable."""
    with patch.dict(sys.modules, {
        "streamlit": MagicMock(),
        "src.storage": MagicMock(),
        "src.validation": MagicMock()
    }):
        import streamlit as st
        st.columns.side_effect = lambda spec: [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
        st.tabs.side_effect = lambda tabs: [MagicMock() for _ in range(len(tabs))]
        st.selectbox.return_value = "Select Year"

        custom_password = "custom_admin_pass"
        monkeypatch.setenv("ADMIN_PASSWORD", custom_password)

        import app
        importlib.reload(app)
        assert app.ADMIN_PASSWORD == custom_password

def test_passwords_default(monkeypatch):
    """Test that passwords default to original values when env vars are not set."""
    with patch.dict(sys.modules, {
        "streamlit": MagicMock(),
        "src.storage": MagicMock(),
        "src.validation": MagicMock()
    }):
        import streamlit as st
        st.columns.side_effect = lambda spec: [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
        st.tabs.side_effect = lambda tabs: [MagicMock() for _ in range(len(tabs))]
        st.selectbox.return_value = "Select Year"

        monkeypatch.delenv("EXPERT_PASSWORD", raising=False)
        monkeypatch.delenv("ADMIN_PASSWORD", raising=False)

        import app
        importlib.reload(app)
        assert app.EXPERT_PASSWORD == "password123"
        assert app.ADMIN_PASSWORD == "admin456"
