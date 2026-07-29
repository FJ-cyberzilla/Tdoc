import json
import math
import re
import subprocess
from collections import Counter
from datetime import datetime
from typing import Any, cast
from urllib.parse import urlparse


class SMSChecker:
    """Advanced SMS metadata analysis engine."""

    def check(self) -> dict[str, Any]:
        """Performs SMS metadata analysis."""
        try:
            res = subprocess.run(
                ["termux-sms-list", "--message-limit=200"],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
            if res.returncode != 0 or not res.stdout.strip():
                return {"error": "Failed to access SMS"}

            messages: list[dict[str, Any]] = json.loads(res.stdout)
            return self.analyze_messages(messages)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
            return {"error": "Analysis failed"}

    def analyze_messages(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        """Analyzes a list of SMS messages."""
        if not messages:
            return {
                "total_messages": 0,
                "sent_recv_ratio": "0/0",
                "sender_diversity": 0.0,
                "peak_hour": "N/A",
                "risky_domains": [],
                "domain_count": 0,
            }

        # Analytics structures
        sender_freq: Counter[str] = Counter()
        time_dist: Counter[int] = Counter()
        domain_freq: Counter[str] = Counter()
        total_sent: int = 0
        total_recv: int = 0

        url_pattern = re.compile(r'https?://[^\s<>"]+')

        for msg in messages:
            sender = cast(str, msg.get("address", "Unknown"))
            body = cast(str, msg.get("body", ""))
            msg_type = msg.get("type")

            # Stats
            if msg_type == 2:
                total_sent += 1
            else:
                total_recv += 1
            sender_freq[sender] += 1

            # Temporal
            ts = msg.get("date")
            if isinstance(ts, (int, float)):
                hour = datetime.fromtimestamp(ts / 1000.0).hour
                time_dist[hour] += 1

            # Domain Extraction
            urls = url_pattern.findall(body)
            for url in urls:
                try:
                    domain = urlparse(url).netloc
                    domain_freq[domain] += 1
                except Exception:
                    continue

        # Calculations
        num_senders = len(sender_freq)
        # Shannon Entropy for sender diversity
        entropy = 0.0
        if num_senders > 0:
            for count in sender_freq.values():
                p = count / len(messages)
                entropy -= p * math.log2(p)

        # High volume sender detection (Heuristic)
        risky_domains = [d for d, c in domain_freq.items() if c > 2]

        return {
            "total_messages": len(messages),
            "sent_recv_ratio": f"{total_sent}/{total_recv}",
            "sender_diversity": round(entropy, 2),
            "peak_hour": time_dist.most_common(1)[0][0] if time_dist else "N/A",
            "risky_domains": risky_domains,
            "domain_count": len(domain_freq),
        }
