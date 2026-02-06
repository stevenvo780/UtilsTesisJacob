#!/usr/bin/env python3
"""Genera un resumen de metricas para todas las simulaciones.

Uso:
  python3 scripts/evaluar_simulaciones.py > /tmp/reporte.md

Opcional:
  python3 scripts/evaluar_simulaciones.py --write
"""
from pathlib import Path
import json
import argparse

ROOT = Path(__file__).resolve().parents[2]
CASES_ROOT = ROOT / 'TesisDesarrollo' / '02_Modelado_Simulacion'
OUTPUT = CASES_ROOT / 'Reporte_General_Simulaciones.md'


def read_metrics(case_dir: Path):
    p = case_dir / 'metrics.json'
    if not p.exists():
        return None
    return json.loads(p.read_text())


def compute_metrics(metrics_obj):
    if not metrics_obj:
        return None
    ph = metrics_obj.get('phases', {}).get('real') or metrics_obj.get('phases', {}).get('synthetic')
    if not ph:
        return None
    errors = ph.get('errors', {})
    symploke = ph.get('symploke', {})
    rmse_reduced = errors.get('rmse_reduced')
    rmse_abm = errors.get('rmse_abm')
    edi = None
    if rmse_reduced and rmse_abm is not None and rmse_reduced != 0:
        edi = (rmse_reduced - rmse_abm) / rmse_reduced
    internal = symploke.get('internal')
    external = symploke.get('external')
    cr = None
    if internal is not None and external not in (None, 0):
        cr = internal / external
    return {
        'edi': edi,
        'cr': cr,
        'overall_pass': ph.get('overall_pass')
    }


def fmt(x):
    if x is None:
        return 'n/a'
    return f"{x:.3f}"


def build_table():
    rows = []
    for case_dir in sorted(CASES_ROOT.glob('*_caso_*')):
        metrics_obj = read_metrics(case_dir)
        m = compute_metrics(metrics_obj)
        case = case_dir.name
        report_link = f"`{case_dir.name}/report.md`"
        rows.append((case, m, report_link))

    lines = []
    lines.append("# Reporte General de Simulaciones")
    lines.append("")
    lines.append("| Caso | EDI | CR | Estado | Reporte |")
    lines.append("| :--- | ---: | ---: | :--- | :--- |")
    for case, m, report_link in rows:
        edi = fmt(m['edi']) if m else 'n/a'
        cr = fmt(m['cr']) if m else 'n/a'
        state = str(m['overall_pass']) if m else 'n/a'
        lines.append(f"| {case} | {edi} | {cr} | {state} | {report_link} |")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='Write to Reporte_General_Simulaciones.md')
    args = parser.parse_args()

    table = build_table()
    if args.write:
        OUTPUT.write_text(table.strip() + "\n", encoding='utf-8')
    else:
        print(table)


if __name__ == '__main__':
    main()
