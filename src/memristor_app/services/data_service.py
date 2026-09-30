from pathlib import Path

import pandas as pd


class DataService:
    """Handle loading and basic inspection of dataset files."""

    SUPPORTED_EXTENSIONS = {".xlsx", ".xls", ".csv"}

    def load_file(self, file_path: str | Path) -> pd.DataFrame:
        """
        Load an Excel or CSV file into a pandas DataFrame.

        Parameters
        ----------
        file_path:
            Path to the dataset.

        Returns
        -------
        pandas.DataFrame
            Loaded dataset.

        Raises
        ------
        FileNotFoundError
            If the selected file does not exist.

        ValueError
            If the file type is not supported.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"The selected path is not a file: {path}"
            )

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".csv":
            return pd.read_csv(path)

        return pd.read_excel(path)

    def get_dataset_info(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Return basic information about a loaded dataset.
        """

        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "column_names": list(dataframe.columns),
        }


def get_dataset_preview(self, file_path: str, rows: int = 10):
    """
    Return the first few rows of the dataset for GUI preview.
    """

    from pathlib import Path
    import pandas as pd

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    if path.suffix.lower() == ".csv":
        dataframe = pd.read_csv(path)

    elif path.suffix.lower() in {".xlsx", ".xls"}:
        dataframe = pd.read_excel(path)

    else:
        raise ValueError(
            "Unsupported file format. "
            "Please select an Excel or CSV file."
        )

    return dataframe.head(rows)