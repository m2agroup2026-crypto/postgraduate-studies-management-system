from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

FILES = [
    BASE_DIR / "data" / "legacy" / "Digitalization_Data.xlsx",
    BASE_DIR / "data" / "legacy" / "222222.xlsx",
]


for file in FILES:
    path = Path(file)

    if not path.exists():
        print(f"Missing: {file}")
        continue

    print("\n" + "=" * 80)
    print(f"FILE: {file}")
    print("=" * 80)

    excel = pd.ExcelFile(path)

    for sheet in excel.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)

        print(f"\nSHEET: {sheet}")
        print(f"Rows: {len(df)}")
        print(f"Columns: {len(df.columns)}")

        print("\nColumns:")
        for col in df.columns:
            empty = df[col].isna().sum()
            print(f"- {col} | Empty: {empty}")
