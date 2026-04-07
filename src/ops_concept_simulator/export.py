"""Export ConOps simulation outputs."""

from __future__ import annotations

from csv import DictWriter
from html import escape
from pathlib import Path
from typing import Iterable, Mapping

from .simulate import SimulationResult


def export_reports(result: SimulationResult, export_dir: Path | str) -> None:
    """Write report artifacts."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    _write_text(export_path / "conops-summary.md", _render_summary_markdown(result))
    _write_csv(export_path / "scenario-catalog.csv", result.scenario_rows)
    _write_csv(export_path / "subsystem-utilization.csv", result.utilization_rows)
    _write_text(export_path / "conops-dashboard.html", _render_dashboard_html(result))


def _write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[Mapping[str, str]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def _render_summary_markdown(result: SimulationResult) -> str:
    summary = result.summary
    scenarios = "\n".join(
        f"- {row['id']} | {row['title']} | {row['duration_hours']} hours | {row['handoff_count']} handoffs"
        for row in result.scenario_rows
    ) or "- None"
    warnings = "\n".join(f"- {item}" for item in result.warnings) or "- None"
    errors = "\n".join(f"- {item}" for item in result.errors) or "- None"
    return (
        "# ConOps Summary\n\n"
        f"- Scenarios: {summary['scenario_count']}\n"
        f"- Total hours simulated: {summary['total_hours']}\n"
        f"- Longest scenario hours: {summary['longest_scenario_hours']}\n"
        f"- Unique systems involved: {summary['subsystem_count']}\n"
        f"- Total handoffs: {summary['handoff_count']}\n"
        f"- Errors: {summary['error_count']}\n"
        f"- Warnings: {summary['warning_count']}\n\n"
        "## Scenario Catalog\n\n"
        f"{scenarios}\n\n"
        "## Errors\n\n"
        f"{errors}\n\n"
        "## Warnings\n\n"
        f"{warnings}\n"
    )


def _render_dashboard_html(result: SimulationResult) -> str:
    summary = result.summary
    cards = [
      ("Scenarios", str(summary["scenario_count"])),
      ("Total Hours", summary["total_hours"]),
      ("Systems", str(summary["subsystem_count"])),
      ("Handoffs", str(summary["handoff_count"])),
    ]
    card_html = "\n".join(
        f"<article class=\"card\"><span>{escape(label)}</span><strong>{escape(value)}</strong></article>"
        for label, value in cards
    )
    scenario_table = _render_table(
        result.scenario_rows,
        ["id", "title", "phase_count", "handoff_count", "duration_hours", "active_system_count"],
        "No scenarios available.",
    )
    utilization_table = _render_table(
        result.utilization_rows,
        ["system", "hours_active", "scenario_count"],
        "No subsystem rollup available.",
    )
    warnings = "".join(f"<li>{escape(item)}</li>" for item in (result.warnings or ["None"]))
    errors = "".join(f"<li>{escape(item)}</li>" for item in (result.errors or ["None"]))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ops Concept Simulator</title>
  <style>
    :root {{
      --bg: #edf4f6;
      --panel: rgba(255,255,255,0.9);
      --ink: #17333a;
      --muted: #5a7379;
      --accent: #0f766e;
      --line: rgba(23,51,58,0.12);
      --shadow: 0 18px 40px rgba(21, 53, 61, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      color: var(--ink);
      background: linear-gradient(180deg, #eef7fa, #ddecef);
    }}
    main {{
      width: min(1100px, calc(100% - 28px));
      margin: 0 auto;
      padding: 28px 0 54px;
    }}
    .hero, section, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      box-shadow: var(--shadow);
      border-radius: 24px;
    }}
    .hero {{
      padding: 28px;
      background: linear-gradient(135deg, rgba(15,118,110,0.95), rgba(14,116,144,0.95));
      color: #f3fffe;
    }}
    h1, h2 {{
      margin: 0 0 12px;
      font-family: "Georgia", serif;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin: 18px 0;
    }}
    .card {{
      padding: 20px;
      min-height: 116px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .card span {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.84rem;
      letter-spacing: 0.07em;
    }}
    .card strong {{
      color: var(--accent);
      font-size: 1.9rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 18px;
    }}
    section {{
      padding: 22px;
      overflow: hidden;
    }}
    .wide {{
      grid-column: 1 / -1;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.94rem;
    }}
    th, td {{
      text-align: left;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      text-transform: uppercase;
      font-size: 0.8rem;
      letter-spacing: 0.06em;
    }}
    ul {{
      margin: 0;
      padding-left: 20px;
    }}
    @media (max-width: 860px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>Ops Concept Simulator</h1>
      <p>Scenario-level concept-of-operations simulator for a disaster-response system-of-systems portfolio.</p>
    </section>
    <div class="metrics">{card_html}</div>
    <div class="grid">
      <section class="wide">
        <h2>Scenario Catalog</h2>
        {scenario_table}
      </section>
      <section>
        <h2>Subsystem Utilization</h2>
        {utilization_table}
      </section>
      <section>
        <h2>Warnings</h2>
        <ul>{warnings}</ul>
      </section>
      <section class="wide">
        <h2>Errors</h2>
        <ul>{errors}</ul>
      </section>
    </div>
  </main>
</body>
</html>
"""


def _render_table(rows: Iterable[Mapping[str, str]], columns: list[str], empty_message: str) -> str:
    row_list = list(rows)
    if not row_list:
        return f"<p>{escape(empty_message)}</p>"
    header_html = "".join(f"<th>{escape(column.replace('_', ' '))}</th>" for column in columns)
    body_html = []
    for row in row_list:
        body_html.append(
            "<tr>" + "".join(f"<td>{escape(str(row.get(column, '')))}</td>" for column in columns) + "</tr>"
        )
    return f"<table><thead><tr>{header_html}</tr></thead><tbody>{''.join(body_html)}</tbody></table>"
