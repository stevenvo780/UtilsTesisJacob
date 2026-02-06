#!/usr/bin/env python3
"""Audita consistencia documental y metrica de simulaciones sin modificar resultados."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
CASES_ROOT = ROOT / 'TesisDesarrollo' / '02_Modelado_Simulacion'
OUTPUT = CASES_ROOT / 'Auditoria_Simulaciones.md'


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


def report_has_results(report_path: Path):
    if not report_path.exists():
        return False
    text = report_path.read_text(encoding='utf-8', errors='ignore')
    return bool(re.search(r"resultado|result|metric|edi|cr", text, re.IGNORECASE))


def audit_case(case_dir: Path):
    issues = []
    metrics_obj = read_metrics(case_dir)
    m = compute_metrics(metrics_obj)

    # file completeness
    if not (case_dir / 'README.md').exists():
        issues.append('README.md faltante')
    if not (case_dir / 'report.md').exists():
        issues.append('report.md faltante')
    else:
        if not report_has_results(case_dir / 'report.md'):
            issues.append('report.md sin seccion de resultados clara')

    docs = case_dir / 'docs'
    required_docs = [
        'arquitectura.md',
        'protocolo_simulacion.md',
        'indicadores_metricas.md',
        'reproducibilidad.md',
        'validacion_c1_c5.md',
    ]
    for doc in required_docs:
        if not (docs / doc).exists():
            issues.append(f'docs/{doc} faltante')

    # metric sanity (no forcing)
    if m is None:
        issues.append('metrics.json faltante o ilegible')
    else:
        if m['edi'] is None:
            issues.append('EDI no disponible (n/a)')
        if m['cr'] is None:
            issues.append('CR no disponible (n/a)')
        if m['cr'] is not None and m['cr'] <= 0:
            issues.append('CR <= 0 (revisar)')
        if m['edi'] is not None and (m['edi'] < -5 or m['edi'] > 5):
            issues.append('EDI fuera de rango esperado (revisar)')
        if m['overall_pass'] is None:
            issues.append('overall_pass no registrado')

    return m, issues


def main():
    lines = []
    lines.append('# Auditoria de Simulaciones')
    lines.append('')
    lines.append('Criterios: consistencia documental, presencia de metricas y señales de posibles anomalías sin forzar resultados.')
    lines.append('')

    rows = []
    for case_dir in sorted(CASES_ROOT.glob('*_caso_*')):
        m, issues = audit_case(case_dir)
        case = case_dir.name
        rows.append((case, m, issues))

    lines.append('| Caso | EDI | CR | Estado | Hallazgos |')
    lines.append('| :--- | ---: | ---: | :--- | :--- |')
    for case, m, issues in rows:
        edi = fmt(m['edi']) if m else 'n/a'
        cr = fmt(m['cr']) if m else 'n/a'
        state = str(m['overall_pass']) if m else 'n/a'
        hall = '; '.join(issues) if issues else 'OK'
        lines.append(f'| {case} | {edi} | {cr} | {state} | {hall} |')

    lines.append('')
    lines.append('## Recomendaciones')
    lines.append('- Si EDI o CR es n/a, revisar el pipeline de calculo y los datos fuente.')
    lines.append('- Si CR <= 0 o EDI fuera de rango, revisar la etapa de normalizacion o parametros.')
    lines.append('- Si reportes carecen de resultados, completar con los hallazgos del metrics.json.')

    OUTPUT.write_text('\n'.join(lines).strip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
