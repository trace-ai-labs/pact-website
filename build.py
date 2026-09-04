"""Build the PACT site: inject benchmark results into template.html -> index.html.

Reads data/*.csv (the aggregate-stage outputs), models_meta.json (hand-entered
from paper Table 3), and examples.json (curated transcripts), and replaces the
/*__PACT_DATA__*/ marker in template.html with a JSON blob.

Refresh after new results land in data/:  python build.py
"""
from __future__ import annotations

import csv
import html as html_mod
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BENCH = ROOT / "data"
SITE = ROOT

AXES = [
    ("default_compliance", "Default Compliance"),
    ("pressure_resistance", "Pressure Resistance"),
    ("pushback_resistance", "Pushback Resistance"),
    ("steerability", "Steerability"),
    ("transparency", "Transparency"),
    ("rule_scope_discernment", "Rule-Scope Discernment"),
]

DOMAINS = {  # keep in sync with src/benchmark/figstyle.py DOMAIN_LABEL
    "advertising": "Advertising", "aml_kyc": "AML", "customer_service": "Customer Service",
    "export_controls": "Export Controls", "finance": "Finance", "gov_services": "Gov. Services",
    "healthcare_admin": "Healthcare", "hr_hiring": "HR/Hiring", "moderation": "Moderation",
    "pharma_medinfo": "Pharma", "privacy": "Privacy", "procurement": "Procurement",
}
PRESSURES = {  # keep in sync with figstyle.PRESSURE_LABEL
    "urgency": "Urgency", "mgr_verbal": "Manager", "peer_escaped": "Peer Escaped",
    "risk_minimize": "Risk Minimized", "cost_pressure": "Cost Pressure",
    "false_clearance": "False Clearance", "fait_accompli": "Fait Accompli",
    "sympathetic_beneficiary": "Sympathetic Beneficiary", "responsibility_shift": "Responsibility Shift",
}


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if any(v.strip() for v in row.values())]


def f3(x: str | float) -> float:
    return round(float(x), 4)


def static_leaderboard(data: dict) -> str:
    esc = html_mod.escape
    head = "".join(f"<th>{esc(a)}</th>" for a in data["axes"])
    rows = []
    for i, m in enumerate(data["models"], 1):
        cells = "".join(f'<td class="num">{v:.3f}</td>' for v in m["axes"])
        rows.append(
            f'<tr class="datarow"><td class="rank num">{i}</td>'
            f'<td class="name"><span class="m">{esc(m["name"])}</span>'
            f'<span class="p">{esc(m["provider"])}</span></td>'
            f'<td class="num pactv">{m["pact"]:.3f}</td>{cells}</tr>'
        )
    return (
        '<table class="lb"><caption class="sr">PACT leaderboard: PACTScore and six-axis '
        'profile for every evaluated model</caption><thead><tr><th></th><th class="name">Model</th>'
        f'<th>PACTScore</th>{head}</tr></thead><tbody>' + "".join(rows) + "</tbody></table>"
    )


def main() -> None:
    meta = json.loads((SITE / "models_meta.json").read_text(encoding="utf-8"))
    meta.pop("__comment", None)

    metrics = {r["model"]: r for r in read_csv(BENCH / "metrics_v2.csv")}
    dom_rows = {r["model"]: r for r in read_csv(BENCH / "dist_model_domain.csv")}
    prs_rows = {r["model"]: r for r in read_csv(BENCH / "dist_model_pressure.csv")}

    missing = set(metrics) ^ set(meta)
    if missing:
        raise SystemExit(f"models_meta.json out of sync with metrics_v2.csv: {sorted(missing)}")

    models = []
    for mid, m in metrics.items():
        info = meta[mid]
        models.append({
            "id": mid,
            "name": info["display"],
            "provider": info["provider"],
            "open": info["open"],
            "params": info["params_total"],
            "active": info["params_active"],
            "released": info["released"],
            "pact": f3(m["pact_score"]),
            "pact_lo": f3(m["pact_score_lo"]),
            "pact_hi": f3(m["pact_score_hi"]),
            "axes": [f3(m[k]) for k, _ in AXES],
            "domains": [f3(dom_rows[mid][d]) for d in DOMAINS],
            "pressures": [f3(prs_rows[mid][p]) for p in PRESSURES],
        })
    models.sort(key=lambda r: -r["pact"])

    pressure_panel = [
        {"key": r["pressure"], "t1": f3(r["t1_comply"]), "t2": f3(r["t2_hold"])}
        for r in read_csv(BENCH / "dist_pressure.csv")
    ]

    domain_panel = [
        {"label": DOMAINS[r["domain"]], "base": f3(r["default_compliance"]),
         "pressured": f3(r["pressure_resistance"])}
        for r in read_csv(BENCH / "dist_domain_axis.csv")
    ]

    data = {
        "axes": [label for _, label in AXES],
        "domains": list(DOMAINS.values()),
        "pressures": list(PRESSURES.values()),
        "models": models,
        "pressure_panel": pressure_panel,
        "domain_panel": domain_panel,
        "examples": json.loads((SITE / "examples.json").read_text(encoding="utf-8")),
    }

    template = (SITE / "template.html").read_text(encoding="utf-8")
    marker = "/*__PACT_DATA__*/"
    if marker not in template:
        raise SystemExit("template.html is missing the /*__PACT_DATA__*/ marker")
    html = template.replace(marker, "const DATA = " + json.dumps(data, separators=(",", ":")) + ";")
    # Static leaderboard so crawlers (and no-JS readers) see model names and
    # scores; the interactive render replaces this node's innerHTML on load.
    lb_marker = "<!--__PACT_LB__-->"
    if lb_marker not in html:
        raise SystemExit("template.html is missing the <!--__PACT_LB__--> marker")
    html = html.replace(lb_marker, static_leaderboard(data), 1)
    (SITE / "index.html").write_text(html, encoding="utf-8")

    print(f"index.html written: {len(data['models'])} models, "
          f"{len(data['examples'])} examples, {len(html) // 1024} KB")


if __name__ == "__main__":
    main()
