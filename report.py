"""
TDoc Command Center - Structured Telemetry Reporting Engine
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, Tuple

from rich.console import Console
from rich.theme import Theme
from constants import ORANGE_THEME, HOME

logger = logging.getLogger(__name__)
console = Console(theme=Theme(ORANGE_THEME))


def _build_html_template(data: Dict[str, Any], timestamp: str) -> str:
    """Compiles a responsive, modern dark/orange terminal operational dashboard."""
    # JSON dump for embedding raw state safely into the document body
    raw_json = json.dumps(data, indent=2)
    
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
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{
            border: 1px solid #ff9100; background: #161616; padding: 15px;
            position: relative; overflow: hidden;
        }}
        .card::before {{
            content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #ff3d00;
        }}
        .card-title {{ color: #ff3d00; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }}
        .meta-val {{ color: #ffd180; }}
        pre {{
            background: #050505; color: #00e676; padding: 15px; border: 1px solid #222;
            overflow-x: auto; font-size: 0.85rem; max-height: 300px;
        }}
        .footer {{ text-align: center; margin-top: 30px; color: #ffd180; font-size: 0.8rem; opacity: 0.7; }}
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
                    <div>Host Platform: <span class="meta-val">Android (Termux Container)</span></div>
                    <div>Data Schema: <span class="meta-val">v2.6.0-SOTA</span></div>
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
</html>
"""
    return html_content


def compile_and_save_telemetry(snapshot_data: Dict[str, Any]) -> Tuple[Path, Path]:
    """Pipes memory state metrics to structured file volumes inside the workspace."""
    reports_dir = Path(HOME) / "TDoc" / "reports"
    
    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logger.error("Failed creating report container folder boundary: %s", err)
        raise

    # Generate persistent epoch string formatting
    epoch = int(time.time())
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    json_file = reports_dir / f"tdoc_telemetry_{epoch}.json"
    html_file = reports_dir / f"tdoc_dashboard_{epoch}.html"

    try:
        # Write 1: Structured Data Blob
        json_file.write_text(json.dumps(snapshot_data, indent=4), encoding="utf-8")
        
        # Write 2: Interactive Orange Spectrum HUD HTML Dashboard
        html_markup = _build_html_template(snapshot_data, timestamp)
        html_file.write_text(html_markup, encoding="utf-8")
        
        console.print(f"\n[bold green]✅ Telemetry Matrices Compiled Successfully![/bold green]")
        console.print(f"  [bold #FF6D00]▪ Data Node Log :[/bold #FF6D00] [grey62]{json_file.name}[/grey62]")
        console.print(f"  [bold #FF6D00]▪ Visual Dashboard:[/bold #FF6D00] [grey62]{html_file.name}[/grey62]")

    except OSError as io_err:
        console.print(f"[status.critical]✗ Telemetry Pipeline Write Exception: {io_err}[/status.critical]")
        logger.error("IO operation barrier encountered during report mapping: %s", io_err)

    return json_file, html_file
