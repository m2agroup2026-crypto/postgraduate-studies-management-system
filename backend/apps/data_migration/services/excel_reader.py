from pathlib import Path

import pandas as pd


class ExcelReader:
    """
    Read and inspect legacy Excel sources.
    This service does not import data.
    It only extracts structure and metadata.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def inspect(self):
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Legacy file not found: {self.file_path}"
            )

        workbook = pd.ExcelFile(self.file_path)

        sheets = []

        for sheet_name in workbook.sheet_names:
            dataframe = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name
            )

            sheets.append(
                {
                    "name": sheet_name,
                    "rows": len(dataframe),
                    "columns": len(dataframe.columns),
                    "fields": list(dataframe.columns),
                }
            )

        return {
            "file_name": self.file_path.name,
            "sheet_count": len(sheets),
            "sheets": sheets,
        }
