from pathlib import Path
import pandas as pd


def load_dataset(file_path: Path):
    """
    Reads CSV or Excel.

    Returns
    -------
    dict

    {
        "tables":{
            table_name: dataframe
        }
    }
    """

    suffix = file_path.suffix.lower()

    if suffix == ".csv":

        df = pd.read_csv(file_path)

        return {
            "tables": {
                file_path.stem: df
            }
        }

    elif suffix in [".xlsx", ".xls"]:

        sheets = pd.read_excel(
            file_path,
            sheet_name=None
        )

        return {
            "tables": sheets
        }

    else:

        raise ValueError("Unsupported file format")
    

def dataframe_metadata(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "memory": round(
            df.memory_usage(deep=True).sum() / 1024,
            2,
        ),
    }