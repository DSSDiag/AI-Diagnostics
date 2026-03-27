import sys
from unittest.mock import MagicMock, patch
import importlib
import pytest
import html

def test_user_profile_xss_protection():
    """
    Test that user-provided name and email are properly escaped in the profile render.
    """
    # Clear app from sys.modules to ensure a fresh import
    if 'app' in sys.modules:
        del sys.modules['app']

    mock_st = MagicMock()
    # Mock st.columns to return the right number of columns and support context manager
    def mock_columns(spec):
        n = len(spec) if isinstance(spec, list) else spec
        cols = [MagicMock() for _ in range(n)]
        for col in cols:
            col.__enter__.return_value = col
        return cols

    mock_st.columns.side_effect = mock_columns
    mock_st.tabs.side_effect = lambda tabs: [MagicMock() for _ in range(len(tabs))]
    mock_st.query_params = {}

    # Simulate a logged-in user with malicious tags
    malicious_name = "<b>Hacked</b><script>alert('xss')</script>"
    malicious_email = '"><img src=x onerror=alert(1)>'

    # We use a real dict for session_state
    session_state = {
        'logged_in_user': {
            'name': malicious_name,
            'email': malicious_email
        }
    }
    mock_st.session_state = session_state

    # st.stop should stop execution
    class StopException(Exception): pass
    mock_st.stop.side_effect = StopException

    mock_storage = MagicMock()
    mock_validation = MagicMock()

    with patch.dict(sys.modules, {
        "streamlit": mock_st,
        "src.storage": mock_storage,
        "src.validation": mock_validation
    }):
        try:
            import app
        except StopException:
            pass
        except Exception as e:
            pytest.fail(f"App execution failed with: {e}")

        # Check all calls to st.markdown
        markdown_calls = [call.args[0] for call in mock_st.markdown.call_args_list if call.args]

        # Find the call that renders "Logged in as:"
        profile_render = None
        for call in markdown_calls:
            if isinstance(call, str) and "Logged in as:" in call:
                profile_render = call
                break

        assert profile_render is not None, "Profile render st.markdown call not found"

        # Verify that malicious strings are escaped
        assert html.escape(malicious_name) in profile_render
        assert html.escape(malicious_email) in profile_render
        # Verify unescaped strings are NOT present
        assert malicious_name not in profile_render
        assert malicious_email not in profile_render
