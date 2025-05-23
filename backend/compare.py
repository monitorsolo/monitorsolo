import pandas as pd

def comparar_crf_vs_ehr(crf_path, ehr_path):
    crf = pd.read_csv(crf_path)
    ehr = pd.read_csv(ehr_path)

    claves = ['paciente_id', 'visita']
    if all(c in crf.columns for c in claves) and all(c in ehr.columns for c in claves):
        merged = pd.merge(crf, ehr, on=claves, suffixes=('_crf', '_ehr'), how='outer', indicator=True)
    else:
        return "⚠️ Las columnas clave (paciente_id, visita) no están en ambos archivos."

    discrepancias = []

    for idx, row in merged.iterrows():
        for col in crf.columns:
            if col in claves:
                continue
            col_crf = f"{col}_crf"
            col_ehr = f"{col}_ehr"
            if col_crf in merged.columns and col_ehr in merged.columns:
                val_crf = row.get(col_crf)
                val_ehr = row.get(col_ehr)
                if pd.isna(val_crf) or pd.isna(val_ehr):
                    continue
                if val_crf != val_ehr:
                    discrepancias.append({
                        'paciente_id': row.get('paciente_id'),
                        'visita': row.get('visita'),
                        'campo': col,
                        'valor_crf': val_crf,
                        'valor_ehr': val_ehr
                    })

    return discrepancias