import sys
from unittest.mock import MagicMock, patch

# Mock streamlit and other modules before importing app
with patch.dict(sys.modules, {
    "streamlit": MagicMock(),
    "src.storage": MagicMock(),
    "src.validation": MagicMock()
}):
    # Mock st.columns and st.tabs to return lists of mocks
    import streamlit as st
    st.columns.side_effect = lambda spec: [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
    st.tabs.side_effect = lambda tabs: [MagicMock() for _ in range(len(tabs))]
    # Mock st.selectbox to return a string to satisfy any validation logic on import
    st.selectbox.return_value = "Select Year"

    from app import _fmt_symptoms

def test_fmt_symptoms_empty():
    assert _fmt_symptoms({}) == []

def test_fmt_symptoms_boolean_keys():
    d = {
        "loss_of_power": True,
        "intermittent_power_loss": False,
        "power_surges": True
    }
    # "loss_of_power" -> "Loss Of Power"
    # "power_surges" -> "Power Surges"
    result = _fmt_symptoms(d)
    assert "Loss Of Power" in result
    assert "Power Surges" in result
    assert "Intermittent Power Loss" not in result
    assert len(result) == 2

def test_fmt_symptoms_other_key():
    # 'other' key with non-empty value
    d = {"other": "Strange rattling"}
    assert _fmt_symptoms(d) == ["Other: Strange rattling"]

    # 'other' key with empty value
    d = {"other": ""}
    assert _fmt_symptoms(d) == []

def test_fmt_symptoms_mixed_keys():
    d = {
        "vibration": True,
        "rough_engine": False,
        "other": "Steering pull"
    }
    result = _fmt_symptoms(d)
    assert "Vibration" in result
    assert "Other: Steering pull" in result
    assert "Rough Engine" not in result
    assert len(result) == 2

def test_fmt_symptoms_all_false():
    d = {
        "vibration": False,
        "rough_engine": False,
        "other": ""
    }
    assert _fmt_symptoms(d) == []
