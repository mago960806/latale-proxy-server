from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent.parent
CSV_DIR = BASE_DIR / "DATA/CSV"


def load_actions() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_DIR / "ACTION_INTERFACE.csv")
    df = df[field_names]
    return df


def load_skills() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
    ]
    df: pd.DataFrame = pd.read_csv(CSV_DIR / "SKILL.csv")
    df = df.loc[df["ID"] != 0]
    df = df[field_names]
    return df


def load_items() -> pd.DataFrame:
    field_names = [
        "ID",
        "_Name",
    ]
    df = pd.concat([pd.read_csv(item_file, low_memory=False) for item_file in CSV_DIR.glob("ITEM_?.csv")])
    df = df[field_names]
    return df
