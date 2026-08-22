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
            return self._empty_analysis()

        sender_freq: Counter[str] = Counter()
        time_dist: Counter[int] = Counter()
        domain_freq: Counter[str] = Counter()
        total_sent = 0
        total_recv = 0

        for msg in messages:
            stats = self._process_message(msg)
            total_sent += stats["sent"]
            total_recv += stats["recv"]
            if stats["sender"]:
                sender_freq[stats["sender"]] += 1
            if stats["hour"] is not None:
                time_dist[stats["hour"]] += 1
            domain_freq.update(stats["domains"])

        return self._summarize_analysis(
            len(messages), total_sent, total_recv, sender_freq, time_dist, domain_freq
        )

    def _empty_analysis(self) -> dict[str, Any]:
        return {
            "total_messages": 0,
            "sent_recv_ratio": "0/0",
            "sender_diversity": 0.0,
            "peak_hour": "N/A",
            "risky_domains": [],
            "domain_count": 0,
        }

    def _calculate_diversity(self, sender_freq: Counter[str], total: int) -> float:
        if not sender_freq or total == 0:
            return 0.0
        entropy = 0.0
        for count in sender_freq.values():
            p = count / total
            entropy -= p * math.log2(p)
        return round(entropy, 2)

    def _summarize_analysis(
        self,
        total: int,
        sent: int,
        recv: int,
        sender_freq: Counter[str],
        time_dist: Counter[int],
        domain_freq: Counter[str],
    ) -> dict[str, Any]:
        risky_domains = [d for d, c in domain_freq.items() if c > 2]

        return {
            "total_messages": total,
            "sent_recv_ratio": f"{sent}/{recv}",
            "sender_diversity": self._calculate_diversity(sender_freq, total),
            "peak_hour": time_dist.most_common(1)[0][0] if time_dist else "N/A",
            "risky_domains": risky_domains,
            "domain_count": len(domain_freq),
        }

    def _process_message(self, msg: dict[str, Any]) -> dict[str, Any]:
        sender = cast(str, msg.get("address", "Unknown"))
        body = cast(str, msg.get("body", ""))

        sent = 1 if msg.get("type") == 2 else 0
        recv = 1 - sent

        ts = msg.get("date")
        hour = datetime.fromtimestamp(ts / 1000.0).hour if isinstance(ts, (int, float)) else None

        return {
            "sent": sent,
            "recv": recv,
            "sender": sender,
            "hour": hour,
            "domains": self._extract_domains(body),
        }

    def _extract_domains(self, body: str) -> list[str]:
        url_pattern = re.compile(r'https?://[^\s<>"]+')
        urls = url_pattern.findall(body)
        domains = []
        for url in urls:
            try:
                domains.append(urlparse(url).netloc)
            except Exception:
                continue
        return domains
