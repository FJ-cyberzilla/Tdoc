"""
Structured Telemetry Reporting Engine for Termux-Doctor.

This module is responsible for compiling raw diagnostics and telemetry data
into structured, persistent report formats, specifically JSON files for raw data
archiving and responsive, styled HTML/CSS dashboards for human review.

Output Formats:
    1. Raw Data Log (.json): A detailed, well-formatted JSON file detailing all
       collected system metrics. Ideal for ingestion by other monitoring tools.
    2. Visual Dashboard (.html): A single-file, highly-responsive dark mode UI
       featuring diagnostic cards and embedded syntax-highlighted raw telemetry logs.

Configuration & Paths:
    - Reports are saved to `~/TDoc/reports/` using the system's home directory.
    - Files are dynamically named with UNIX epoch timestamps (`tdoc_telemetry_<epoch>.json`,
      `tdoc_dashboard_<epoch>.html`) to prevent collision.

Example usage:
    from src.utils.report import compile_and_save_telemetry
    data = {"system": {"cpu": "Octa-core", "ram": "8GB"}}
    json_path, html_path = compile_and_save_telemetry(data)
    print(f"Report compiled successfully to: {html_path}")
"""

import json
import logging
import time
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.theme import Theme

from src.constants import RICH_THEME_CONFIG

logger = logging.getLogger(__name__)
console = Console(theme=Theme(RICH_THEME_CONFIG))


def _build_html_template(data: dict[str, Any], timestamp: str) -> str:
    """
    Compiles a responsive, modern dark/orange terminal operational HTML dashboard.

    The HTML template contains inline styles for layout (CSS Grid), responsive cards,
    and a container showing the raw JSON payload in a code block.

    Args:
        data (dict[str, Any]): The raw telemetry metrics dataset.
        timestamp (str): Formatted date string for the report compilation time.

    Returns:
        str: Fully compiled, self-contained HTML/CSS markup string.
    """
    raw_json = json.dumps(data, indent=2)

    # ✅ FIX: break the long string using parentheses (implicit concatenation)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TDoc Systems Report // {timestamp}</title>
    <style>
        body {{
            background-color: #0d0d0d; color: #ffab40; font-family: 'Courier New', monospace;
            margin: 0; padding: 20px; line-height: 1.5;
        }}
        .hud-frame {{
            border: 2px solid #ff6d00; max-width: 1000px; margin: 0 auto;
            background: #121212; box-shadow: 0 0 20px rgba(255,109,0,0.15);
        }}
        .hud-header {{
            background: #ff6d00; color: #000; padding: 15px; font-weight: bold;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .hud-title {{ font-size: 1.3rem; letter-spacing: 2px; }}
        .hud-body {{ padding: 20px; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .card {{
            border: 1px solid #ff9100;
            background: #161616;
            padding: 15px;
            position: relative;
            overflow: hidden;
        }}
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: #ff3d00;
        }}
        .card-title {{
            color: #ff3d00;
            font-weight: bold;
            margin-bottom: 10px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }}
        .meta-val {{ color: #ffd180; }}
        pre {{
            background: #050505;
            color: #00e676;
            padding: 15px;
            border: 1px solid #222;
            overflow-x: auto;
            font-size: 0.85rem;
            max-height: 300px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #ffd180;
            font-size: 0.8rem;
            opacity: 0.7;
        }}

    </style>
</head>
<body>
    <div class="hud-frame">
        <div class="hud-header">
            <span class="hud-title">🗲 TDOC TERMINAL TELEMETRY MATRIX</span>
            <span>GEN_TIME: {timestamp}</span>
        </div>
        <div class="hud-body">
            <div class="grid">
                <div class="card">
                    <div class="card-title">⨠ ENGINE EXECUTION META</div>
                    <div>Status: <span class="meta-val" style="color:#00e676;">OPTIMAL</span></div>
                    <div>Host Platform: <span class="meta-val">Android</span></div>
                    <div>Data Schema: <span class="meta-val">v5.4.9-SOTA</span></div>
                </div>
                <div class="card">
                    <div class="card-title">⨠ DISK SUBSYSTEM DATA</div>
                    <div>Report Location: <span class="meta-val">~/TDoc/reports/</span></div>
                    <div>Formats Emitted: <span class="meta-val">JSON, HTML Engine Logs</span></div>
                </div>
            </div>
            <br>
            <div class="card-title">📊 RAW STRUCTURAL CAPTURE LOGS</div>
            <pre><code>{raw_json}</code></pre>
        </div>
    </div>
    <div class="footer">TDoc Operational Control Center Core // Automated Matrix Dump</div>
</body>
</html>"""
    return html_content


def compile_and_save_telemetry(snapshot_data: dict[str, Any]) -> tuple[Path, Path]:
    """
    Pipes memory state metrics to structured file volumes inside the workspace.

    This function automatically ensures that the report output directory exists,
    resolves paths, formats dates, saves both JSON and HTML representations of the
    diagnostics, and displays rich feedback on the terminal console.

    Args:
        snapshot_data (dict[str, Any]): Full system diagnostic telemetry snapshot.

    Returns:
        tuple[Path, Path]: A pair of (JSON path, HTML path) for the compiled reports.

    Raises:
        OSError: If directory creation or file writing fails due to permission barriers.
    """
    # ✅ FIX: use Path.home() instead of missing HOME constant
    reports_dir = Path.home() / "TDoc" / "reports"

    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logger.error("Failed creating report container folder boundary: %s", err)
        raise

    epoch = int(time.time())
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    json_file = reports_dir / f"tdoc_telemetry_{epoch}.json"
    html_file = reports_dir / f"tdoc_dashboard_{epoch}.html"

    try:
        json_file.write_text(json.dumps(snapshot_data, indent=4), encoding="utf-8")

        html_markup = _build_html_template(snapshot_data, timestamp)
        html_file.write_text(html_markup, encoding="utf-8")

        # ✅ FIX: removed f prefix (no interpolation)
        console.print("\n[bold green]✅ Telemetry Matrices Compiled Successfully![/bold green]")
        console.print(
            f"  [bold #FF6D00]▪ Data Node Log :[/bold #FF6D00] [grey62]{json_file.name}[/grey62]"
        )
        console.print(
            f"  [bold #FF6D00]▪ Visual Dashboard:[/bold #FF6D00] [grey62]{html_file.name}[/grey62]"
        )

    except OSError as io_err:
        console.print(
            f"[status.critical]✗ Telemetry Pipeline Write Exception: {io_err}[/status.critical]"
        )
        logger.error("IO operation barrier encountered during report mapping: %s", io_err)

    return json_file, html_file
