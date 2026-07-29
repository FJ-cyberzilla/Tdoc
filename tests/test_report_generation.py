"""
Integration tests for report generation.

This test suite verifies that the reporting utility can correctly
process and format service data.
"""

from unittest.mock import patch

from src.utils.report import compile_and_save_telemetry


def test_report_generation():
    """Test generating a simple report."""
    data = {"system": "ok", "network": "fast"}

    with (
        patch("src.utils.report.Path.write_text"),
        patch("src.utils.report.Path.mkdir"),
    ):
        json_path, html_path = compile_and_save_telemetry(data)

    assert json_path.suffix == ".json"
    assert html_path.suffix == ".html"
