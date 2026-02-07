#!/usr/bin/env python3
"""Actualiza tablas de 02_Modelado_Simulacion usando metrics.json.

- Genera Reporte_General_Simulaciones.md
- Reemplaza la tabla en 02_Modelado_Simulacion.md
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
CASES_ROOT = ROOT / 'TesisDesarrollo' / '02_Modelado_Simulacion'
MAIN_DOC = CASES_ROOT / '02_Modelado_Simulacion.md'
REPORT_DOC = CASES_ROOT / 'Reporte_General_Simulaciones.md'

LOE_MAP = {
    '01_caso_clima': 5,
    '02_caso_conciencia': 1,
    '03_caso_contaminacion': 4,
    '04_caso_energia': 4,
    '05_caso_epidemiologia': 4,
    '06_caso_estetica': 2,
    '07_caso_falsacion_exogeneidad': 1,
    '08_caso_falsacion_no_estacionariedad': 1,
    '09_caso_falsacion_observabilidad': 1,
    '10_caso_finanzas': 5,
    '11_caso_justicia': 2,
    '12_caso_moderacion_adversarial': 1,
    '13_caso_movilidad': 2,
    '14_caso_paradigmas': 2,
    '15_caso_politicas_estrategicas': 1,
    '16_caso_postverdad': 2,
    '17_caso_rtb_publicidad': 1,
    '18_caso_wikipedia': 3,
    '19_caso_acidificacion_oceanica': 5,
    '21_caso_kessler_syndrome': 5,
    '22_caso_salinizacion': 4,
    '23_caso_fosforo': 3,
    '24_caso_erosion_dialectica': 2,
    '25_caso_microplasticos': 4,
    '26_caso_acuiferos': 5,
    '27_caso_starlink': 5,
    '28_caso_riesgo_biologico': 2,
    '29_caso_fuga_cerebros': 2,
    '30_caso_iot': 3,
}


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

    # Detectar caso tautológico: rmse_abm ≈ 0 indica que assimilation
    # domina completamente y el EDI no mide acoplamiento real
    tautological = (rmse_abm is not None and rmse_abm < 1e-6)

    edi = None
    if not tautological and rmse_reduced and rmse_abm is not None and rmse_reduced != 0:
        edi = (rmse_reduced - rmse_abm) / rmse_reduced
    internal = symploke.get('internal')
    external = symploke.get('external')
    cr = None
    if internal is not None and external not in (None, 0):
        cr = internal / external
    return {
        'edi': edi,
        'cr': cr,
        'overall_pass': False if tautological else ph.get('overall_pass'),
        'tautological': tautological,
    }


def fmt(x):
    if x is None:
        return 'n/a'
    return f"{x:.3f}"


def build_rows():
    rows = []
    for case_dir in sorted(CASES_ROOT.glob('*_caso_*')):
        metrics_obj = read_metrics(case_dir)
        m = compute_metrics(metrics_obj)
        case = case_dir.name
        report_link = f"`{case_dir.name}/report.md`"
        rows.append((case, m, report_link))
    return rows


def build_table(rows):
    lines = []
    lines.append("| Caso | LoE | EDI | CR | Estado | Reporte |")
    lines.append("| :--- | :--- | ---: | ---: | :--- | :--- |")
    for case, m, report_link in rows:
        loe = LOE_MAP.get(case, 'n/a')
        if m and m.get('tautological'):
            edi = 'TAUT'
            state = 'False'
        elif m:
            edi = fmt(m['edi'])
            state = str(m['overall_pass'])
        else:
            edi = 'n/a'
            state = 'n/a'
        cr = fmt(m['cr']) if m else 'n/a'
        lines.append(f"| {case} | {loe} | {edi} | {cr} | {state} | {report_link} |")
    return "\n".join(lines)


def update_report(rows):
    table = build_table(rows)
    content = "# Reporte General de Simulaciones\n\n" + table + "\n"
    REPORT_DOC.write_text(content, encoding='utf-8')


def update_main(rows):
    table = build_table(rows)
    block = "\n".join([
        "## Resultados (Matriz de Validacion Tecnica)",
        "",
        table,
        "",
        "Para recalcular este reporte de forma automatica, usar:",
        "`python3 scripts/actualizar_tablas_002.py`",
        "",
    ])
    text = MAIN_DOC.read_text(encoding='utf-8', errors='ignore')
    text = re.sub(r"## Resultados \(Matriz de Validacion Tecnica\)[\s\S]*?(?=\n## |\Z)", block.rstrip(), text)
    MAIN_DOC.write_text(text.strip() + "\n", encoding='utf-8')


def main():
    rows = build_rows()
    update_report(rows)
    update_main(rows)


if __name__ == '__main__':
    main()
