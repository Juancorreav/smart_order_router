import pandas as pd
from typing import List, Dict

def load_snapshots_from_csv(filepath: str) -> List[List[Dict]]:
    """
    Lee el archivo CSV de mensajes de mercado y devuelve una lista de snapshots.
    Cada snapshot contiene la mejor oferta (ask) de cada venue (publisher_id) en un momento dado (ts_event).
    """
    print("Cargando datos...")
    df = pd.read_csv(filepath)

    print("Ordenando por ts_event...")
    df.sort_values("ts_event", inplace=True)

    print("Eliminando duplicados por ts_event y publisher_id...")
    df = df.drop_duplicates(subset=["ts_event", "publisher_id"], keep="first")

    print("Agrupando por ts_event para construir snapshots...")
    snapshots = []
    grouped = df.groupby("ts_event")

    for ts_event, group in grouped:
        snapshot = []
        for _, row in group.iterrows():
            # Validar que los datos estén completos
            if pd.notnull(row["ask_px_00"]) and pd.notnull(row["ask_sz_00"]):
                snapshot.append({
                    "venue": int(row["publisher_id"]),
                    "ask": float(row["ask_px_00"]),
                    "ask_size": float(row["ask_sz_00"])
                })
        if snapshot:  # solo agregar snapshots que tengan al menos un venue válido
            snapshots.append(snapshot)

    print(f"Total de snapshots generados: {len(snapshots)}")
    return snapshots
