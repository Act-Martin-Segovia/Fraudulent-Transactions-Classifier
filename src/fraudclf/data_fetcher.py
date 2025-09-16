from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import pandas as pd
from fraudclf.utils.common import logger


class DataFetcher:
    """
    Load a CSV into a DataFrame and split into features and target.

    Parameters
    ----------
    csv_path : str | Path
        Path to the CSV file.
    target_column_name : str | None
        Name of the target column. Required for get_features_and_target().
    id_column_name : str | None
        Optional ID column. If provided, it will be removed from features and
        (optionally) returned alongside the target.
    header : bool
        Whether the CSV has a header row (True -> header at row 0).
    """

    def __init__(
        self,
        csv_path: str | Path,
        target_column_name: Optional[str] = None,
        id_column_name: Optional[str] = None,
        header: bool = True,
    ) -> None:
        self.csv_path = Path(csv_path)
        self.has_header = header
        self.target_name = target_column_name
        self.id_column = id_column_name

    def _read_csv_file(self) -> pd.DataFrame:
        """Read the CSV file into a DataFrame."""
        header = 0 if self.has_header else None
        try:
            logger.info(f"Reading CSV file from {self.csv_path}")
            df = pd.read_csv(self.csv_path, header=header)
            logger.info(f"Loaded DataFrame with {len(df)} rows and {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            raise
        except Exception as exc:
            logger.exception(f"Unexpected error reading CSV file: {exc}")
            raise

    def get_features_and_target(
        self, include_id_in_target: bool = True
    ) -> Tuple[pd.DataFrame, pd.Series | pd.DataFrame]:
        """
        Split the loaded CSV into (X, y).

        Parameters
        ----------
        include_id_in_target : bool
            If True and an ID column is set, return target as a 2-column DataFrame [id, target].
            If False or no ID column, return y as a Series.

        Returns
        -------
        (features, target)
            features: DataFrame of predictors (target and ID removed if present)
            target: Series (or DataFrame if include_id_in_target=True and id_column is set)
        """
        if self.target_name is None:
            logger.error("Target column not specified in DataFetcher initialization.")
            raise ValueError("target_column_name must be provided to split features/target.")

        df = self._read_csv_file()

        # Validate required columns exist
        missing: list[str] = [
            c for c in [self.target_name, self.id_column] if c and c not in df.columns
        ]
        if missing:
            logger.error(f"Missing columns in CSV: {missing}")
            raise KeyError(f"Columns not found in CSV: {missing}. Available: {list(df.columns)}")

        # Build features by dropping target and ID
        drop_cols = [self.target_name]
        if self.id_column and self.id_column in df.columns:
            drop_cols.append(self.id_column)
        features = df.drop(columns=drop_cols)
        logger.info(f"Features shape: {features.shape}")

        # Build target
        if self.id_column and include_id_in_target:
            target: pd.DataFrame | pd.Series = df[[self.id_column, self.target_name]].copy()
        else:
            target = df[self.target_name].copy()
        logger.info(f"Target shape: {getattr(target, 'shape', None)}")

        return features, target
