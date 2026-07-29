"""
Unit tests for the NetworkService and its checkers.

This test suite covers connectivity checks, speed measurements, DNS resolution,
proxy detection, timeout handling, and retry logic.
"""

import os
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.exceptions import NetworkError
from src.services.network import NetworkService
from src.services.network_checkers import (
    DNSChecker,
    NetworkSpeedChecker,
    ProxyChecker,
    VPNStatusChecker,
)


def test_connectivity_checks_and_retry_logic():
    """Test that NetworkService correctly checks mirrors and retries on failure."""
    service = NetworkService()

    # We patch VPN and Speed checkers to avoid their internal network calls
    # interfering with our count
    with (
        patch.object(VPNStatusChecker, "check", return_value={"ip": "1.1.1.1", "active": False}),
        patch.object(NetworkSpeedChecker, "check", return_value={"status": "OK"}),
    ):
        # Case 1: First mirror works
        with patch("urllib.request.urlopen") as mock_url:
            mock_url.return_value.__enter__.return_value = MagicMock()
            results = service.run()
            assert results["mirror"]["online"] is True
            assert results["mirror"]["details"] == "packages.termux.dev"
            assert mock_url.call_count == 1

        # Case 2: First mirror fails, second succeeds (Retry Logic)
        with patch("urllib.request.urlopen") as mock_url:
            # First call raises TimeoutError, second succeeds
            mock_url.side_effect = [TimeoutError(), MagicMock()]
            results = service.run()
            assert results["mirror"]["online"] is True
            assert results["mirror"]["details"] == "packages.termux.org"
            assert mock_url.call_count == 2

        # Case 3: All mirrors fail
        with patch("urllib.request.urlopen") as mock_url:
            mock_url.side_effect = TimeoutError()
            results = service.run()
            assert results["mirror"]["online"] is False
            assert "timed out" in results["mirror"]["details"]
            # It tries 4 mirrors
            assert mock_url.call_count == 4


def test_speed_measurements():
    """Test the NetworkSpeedChecker's ability to measure download speed."""
    checker = NetworkSpeedChecker()

    # Mock successful download of 10KB in 0.5 seconds (20 KB/s)
    mock_response = MagicMock()
    mock_response.read.return_value = b"0" * 1024 * 10
    mock_response.__enter__.return_value = mock_response

    with (
        patch("urllib.request.urlopen", return_value=mock_response),
        patch("time.time", side_effect=[0, 0.5]),
    ):
        results = checker.check()
        assert results["status"] == "OK"
        assert results["speed_kb_s"] == 20.0
        assert results["latency_ms"] == 500.0


def test_dns_resolution():
    """Test DNSChecker via getprop and resolv.conf."""
    checker = DNSChecker()

    # Test getprop success
    mock_res = MagicMock(returncode=0, stdout="8.8.8.8\n")
    with patch("subprocess.run", return_value=mock_res):
        results = checker.check()
        assert "8.8.8.8" in results["servers"]
        assert results["status"] == "OK"

    # Test resolv.conf fallback
    m = mock_open(read_data="nameserver 1.1.1.1\n")
    with (
        patch("subprocess.run", return_value=MagicMock(returncode=1, stdout="")),
        patch("os.path.exists", return_value=True),
        patch("builtins.open", m),
    ):
        results = checker.check()
        assert "1.1.1.1" in results["servers"]
        assert results["status"] == "OK"


def test_proxy_detection():
    """Test ProxyChecker with environment variables."""
    checker = ProxyChecker()

    # Case 1: No proxies
    with patch.dict(os.environ, {}, clear=True):
        results = checker.check()
        assert results["active"] is False
        assert results["proxies"] == {}

    # Case 2: HTTP Proxy set
    with patch.dict(os.environ, {"http_proxy": "http://proxy.example.com:8080"}, clear=True):
        results = checker.check()
        assert results["active"] is True
        assert results["proxies"]["http_proxy"] == "http://proxy.example.com:8080"


# ... (existing imports)


def test_timeout_handling():
    """Verify that checkers use appropriate timeouts for network operations."""
    # Test NetworkSpeedChecker timeout
    checker = NetworkSpeedChecker()
    with patch("urllib.request.urlopen") as mock_url:
        mock_url.side_effect = TimeoutError()
        with pytest.raises(NetworkError) as excinfo:
            checker.check()
        assert "Network speed check failed" in str(excinfo.value)
        assert "url" in excinfo.value.context
        # Verify that timeout parameter was passed to urlopen (last call)
        args, kwargs = mock_url.call_args
        assert kwargs["timeout"] == 2.5
