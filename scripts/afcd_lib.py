"""
AFCD Library — Core functions for querying the Australian Food Composition Database (AFCD) Release 3.

Usage (as a library):
    from scripts.afcd_lib import AFCDDatabase

    db = AFCDDatabase()
    results = db.search("oats")
    profile = db.get_profile("Oats, rolled, uncooked")
    top = db.top_by_nutrient("Iron (mg)", n=10)
"""

import os
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
AFCD_FILE = REPO_ROOT / "AFCD Release 3 - Nutrient profiles.xlsx"
SHEET_NAME = "All solids & liquids per 100 g"

# ---------------------------------------------------------------------------
# Key nutrients for recipe-generation summaries (column name → display name)
# NOTE: Column names in AFCD R3 contain literal \n before the unit, e.g.
#       "Protein \n(g)" — these are the actual pandas column headers.
# ---------------------------------------------------------------------------
KEY_NUTRIENTS: dict[str, str] = {
    "Energy with dietary fibre, equated \n(kJ)": "Energy (kJ)",
    "Protein \n(g)": "Protein (g)",
    "Fat, total \n(g)": "Fat, total (g)",
    "Total dietary fibre \n(g)": "Dietary Fibre (g)",
    "Total sugars (g)": "Total Sugars (g)",
    "Available carbohydrate, without sugar alcohols \n(g)": "Carbohydrates (g)",
    "Sodium (Na) \n(mg)": "Sodium (mg)",
    "Calcium (Ca) \n(mg)": "Calcium (mg)",
    "Iron (Fe) \n(mg)": "Iron (mg)",
    "Magnesium (Mg) \n(mg)": "Magnesium (mg)",
    "Phosphorus (P) \n(mg)": "Phosphorus (mg)",
    "Potassium (K) \n(mg)": "Potassium (mg)",
    "Zinc (Zn) \n(mg)": "Zinc (mg)",
    "Selenium (Se) \n(ug)": "Selenium (ug)",
    "Iodine (I) \n(ug)": "Iodine (ug)",
    "Copper (Cu) \n(mg)": "Copper (mg)",
    "Manganese (Mn) \n(mg)": "Manganese (mg)",
    "Vitamin A retinol equivalents \n(ug)": "Vitamin A (ug RE)",
    "Beta-carotene \n(ug)": "Beta-Carotene (ug)",
    "Lycopene \n(ug)": "Lycopene (ug)",
    "Thiamin (B1) \n(mg)": "Vitamin B1 Thiamin (mg)",
    "Riboflavin (B2) \n(mg)": "Vitamin B2 Riboflavin (mg)",
    "Niacin derived equivalents \n(mg)": "Vitamin B3 Niacin (mg)",
    "Pantothenic acid (B5) \n(mg)": "Vitamin B5 Pantothenic Acid (mg)",
    "Pyridoxine (B6) \n(mg)": "Vitamin B6 Pyridoxine (mg)",
    "Biotin (B7) \n(ug)": "Vitamin B7 Biotin (ug)",
    "Total folates \n(ug)": "Vitamin B9 Folate (ug)",
    "Cobalamin (B12) \n(ug)": "Vitamin B12 Cobalamin (ug)",
    "Vitamin C \n(mg)": "Vitamin C (mg)",
    "Vitamin D3 equivalents \n(ug)": "Vitamin D (ug)",
    "Vitamin E \n(mg)": "Vitamin E (mg)",
    "Cholesterol \n(mg)": "Cholesterol (mg)",
    "Total long chain omega 3 fatty acids, equated \n(mg)": "Omega-3 LC (mg)",
}

# Australian NRVs (Nutrient Reference Values) for an adult male ~70 kg
# Sources: NHMRC Nutrient Reference Values for Australia and New Zealand
# Used for % RDI calculations. Values are per day.
NRV_MALE: dict[str, float] = {
    "Energy with dietary fibre, equated \n(kJ)": 8700,
    "Protein \n(g)": 64,
    "Fat, total \n(g)": 70,
    "Total dietary fibre \n(g)": 30,
    "Total sugars (g)": None,   # no RDI
    "Available carbohydrate, without sugar alcohols \n(g)": 310,
    "Sodium (Na) \n(mg)": 2000,
    "Calcium (Ca) \n(mg)": 1000,
    "Iron (Fe) \n(mg)": 8,
    "Magnesium (Mg) \n(mg)": 420,
    "Phosphorus (P) \n(mg)": 700,
    "Potassium (K) \n(mg)": 3800,
    "Zinc (Zn) \n(mg)": 14,
    "Selenium (Se) \n(ug)": 70,
    "Iodine (I) \n(ug)": 150,
    "Copper (Cu) \n(mg)": 1.7,
    "Manganese (Mn) \n(mg)": 5.5,
    "Vitamin A retinol equivalents \n(ug)": 900,
    "Thiamin (B1) \n(mg)": 1.2,
    "Riboflavin (B2) \n(mg)": 1.3,
    "Niacin derived equivalents \n(mg)": 16,
    "Pantothenic acid (B5) \n(mg)": 6.0,
    "Pyridoxine (B6) \n(mg)": 1.7,
    "Biotin (B7) \n(ug)": 30,
    "Total folates \n(ug)": 400,
    "Cobalamin (B12) \n(ug)": 2.4,
    "Vitamin C \n(mg)": 45,
    "Vitamin D3 equivalents \n(ug)": 5,
    "Vitamin E \n(mg)": 10,
    "Total long chain omega 3 fatty acids, equated \n(mg)": 610,
}


class AFCDDatabase:
    """
    Interface to the AFCD Release 3 Excel database.

    All queries operate on the "All solids & liquids per 100 g" sheet.
    Nutrient values are per 100g of edible portion.
    """

    def __init__(self, path: Path = AFCD_FILE):
        self._path = path
        self._df: Optional[pd.DataFrame] = None

    @property
    def df(self) -> pd.DataFrame:
        """Lazily load and cache the AFCD data."""
        if self._df is None:
            self._df = self._load()
        return self._df

    def _load(self) -> pd.DataFrame:
        """Load the AFCD spreadsheet. Header is on row 3 (0-indexed row 2)."""
        if not self._path.exists():
            raise FileNotFoundError(
                f"AFCD file not found at: {self._path}\n"
                "Ensure 'AFCD Release 3 - Nutrient profiles.xlsx' is in the repo root."
            )
        df = pd.read_excel(
            self._path,
            sheet_name=SHEET_NAME,
            header=2,          # row index 2 = 3rd row = the header row
            engine="openpyxl",
        )
        # Drop rows with no Food Name (blank spacer rows)
        df = df.dropna(subset=["Food Name"])
        df = df.reset_index(drop=True)
        return df

    @property
    def columns(self) -> list[str]:
        """All column names in the database."""
        return list(self.df.columns)

    @property
    def food_count(self) -> int:
        return len(self.df)

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str, max_results: int = 20) -> pd.DataFrame:
        """
        Full-text search on Food Name.  Case-insensitive, supports multiple
        space-separated keywords (all must be present).

        Returns a DataFrame of matching rows with identifier + key nutrient cols.
        """
        terms = [t.strip() for t in query.lower().split() if t.strip()]
        mask = pd.Series([True] * len(self.df), index=self.df.index)
        for term in terms:
            mask &= self.df["Food Name"].str.lower().str.contains(
                re.escape(term), na=False
            )
        results = self.df[mask].head(max_results)
        return results[["Public Food Key", "Food Name"] + self._available_key_cols()].copy()

    def search_by_key(self, public_key: str) -> Optional[pd.Series]:
        """Look up a food by its Public Food Key (e.g. 'F002258')."""
        matches = self.df[self.df["Public Food Key"] == public_key]
        if matches.empty:
            return None
        return matches.iloc[0]

    # ------------------------------------------------------------------
    # Full profile
    # ------------------------------------------------------------------

    def get_profile(
        self, food_name: str, exact: bool = False
    ) -> Optional[pd.Series]:
        """
        Return the full row for a food.

        Args:
            food_name: Name to look up (case-insensitive substring match by default).
            exact: If True, require exact match.

        Returns the first match, or None if not found.
        """
        if exact:
            matches = self.df[
                self.df["Food Name"].str.lower() == food_name.lower()
            ]
        else:
            matches = self.df[
                self.df["Food Name"].str.lower().str.contains(
                    re.escape(food_name.lower()), na=False
                )
            ]
        if matches.empty:
            return None
        return matches.iloc[0]

    def get_key_nutrients(self, food_name: str) -> Optional[dict]:
        """
        Return a condensed dict of key nutrients for a food — the nutrients
        most relevant for recipe generation, with % RDI where applicable.

        Returns None if food not found.
        """
        row = self.get_profile(food_name)
        if row is None:
            return None

        result = {
            "food_name": row["Food Name"],
            "public_food_key": row["Public Food Key"],
            "nutrients": {},
        }

        for col, display_name in KEY_NUTRIENTS.items():
            if col not in self.df.columns:
                continue
            val = row.get(col)
            if pd.isna(val):
                val = None
            nrv = NRV_MALE.get(col)
            pct_rdi = None
            if val is not None and nrv:
                pct_rdi = round(val / nrv * 100, 1)
            result["nutrients"][display_name] = {
                "value": val,
                "unit": _parse_unit(col),
                "pct_rdi_male": pct_rdi,
            }

        return result

    # ------------------------------------------------------------------
    # Rankings
    # ------------------------------------------------------------------

    def top_by_nutrient(
        self, nutrient_col: str, n: int = 10, min_value: float = 0
    ) -> pd.DataFrame:
        """
        Rank all foods by a specific nutrient (highest first).

        Args:
            nutrient_col: Exact column name (e.g. "Iron (mg)").
            n: Number of results to return.
            min_value: Filter foods with at least this value.

        Returns a DataFrame with Food Name, the nutrient value, and key IDs.
        """
        if nutrient_col not in self.df.columns:
            close = self.find_nutrient_column(nutrient_col)
            if not close:
                raise ValueError(
                    f"Column '{nutrient_col}' not found. "
                    f"Use db.find_nutrient_column() to search."
                )
            nutrient_col = close[0]

        subset = self.df[self.df[nutrient_col] >= min_value].copy()
        subset = subset.sort_values(nutrient_col, ascending=False).head(n)
        return subset[["Public Food Key", "Food Name", nutrient_col]].copy()

    def find_nutrient_column(self, query: str) -> list[str]:
        """
        Fuzzy search column names. Useful for discovering exact column names.

        Returns list of matching column names (case-insensitive substring match).
        """
        q = query.lower()
        return [c for c in self.df.columns if q in c.lower()]

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def compare(self, food_names: list[str]) -> pd.DataFrame:
        """
        Side-by-side comparison of key nutrients for multiple foods.

        Args:
            food_names: List of food name substrings to search.

        Returns a DataFrame with nutrients as rows, foods as columns.
        """
        rows = {}
        for name in food_names:
            row = self.get_profile(name)
            if row is not None:
                rows[row["Food Name"]] = row

        if not rows:
            return pd.DataFrame()

        available_cols = self._available_key_cols()
        data = {}
        for display_col in available_cols:
            data[display_col] = {
                food: row.get(display_col) for food, row in rows.items()
            }

        return pd.DataFrame(data).T

    # ------------------------------------------------------------------
    # Nutrient density per dollar
    # ------------------------------------------------------------------

    def nutrient_value_per_dollar(
        self,
        food_name: str,
        price_per_100g: float,
    ) -> Optional[dict]:
        """
        Calculate nutrient density per AUD dollar for a food at a given price.

        Args:
            food_name: Food name substring to look up.
            price_per_100g: Price in AUD per 100g of the food.

        Returns dict with nutrient values per dollar spent.
        """
        profile = self.get_key_nutrients(food_name)
        if profile is None or price_per_100g <= 0:
            return None

        result = {
            "food_name": profile["food_name"],
            "price_per_100g_aud": price_per_100g,
            "nutrients_per_dollar": {},
        }

        for nutrient, data in profile["nutrients"].items():
            val = data["value"]
            if val is not None and val > 0:
                per_dollar = round(val / price_per_100g, 3)
                result["nutrients_per_dollar"][nutrient] = {
                    "per_100g": val,
                    "per_dollar": per_dollar,
                    "unit": data["unit"],
                    "pct_rdi_per_dollar": (
                        round(data["pct_rdi_male"] / price_per_100g, 1)
                        if data["pct_rdi_male"] is not None
                        else None
                    ),
                }

        return result

    def rank_by_nutrient_per_dollar(
        self,
        nutrient_col: str,
        prices: dict[str, float],
        n: int = 10,
    ) -> list[dict]:
        """
        Rank foods by nutrient value per dollar, given a price dict.

        Args:
            nutrient_col: Exact column name for the nutrient.
            prices: Dict of {food_name_substring: price_per_100g_aud}.
            n: Max results.

        Returns list of dicts sorted by nutrient per dollar (best first).
        """
        results = []
        for food_name, price in prices.items():
            row = self.get_profile(food_name)
            if row is None:
                continue
            val = row.get(nutrient_col)
            if pd.isna(val) or val is None or price <= 0:
                continue
            results.append({
                "food_name": row["Food Name"],
                "price_per_100g": price,
                "nutrient_value": val,
                "nutrient_col": nutrient_col,
                "per_dollar": round(val / price, 3),
            })
        results.sort(key=lambda x: x["per_dollar"], reverse=True)
        return results[:n]

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _available_key_cols(self) -> list[str]:
        """Return KEY_NUTRIENTS columns that actually exist in the DataFrame."""
        return [c for c in KEY_NUTRIENTS if c in self.df.columns]

    def list_all_foods(self) -> list[str]:
        """Return all food names in the database."""
        return self.df["Food Name"].tolist()


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _parse_unit(col_name: str) -> str:
    """Extract unit from column name like 'Iron (mg)' → 'mg'."""
    m = re.search(r"\(([^)]+)\)$", col_name)
    return m.group(1) if m else ""


def kcal_from_kj(kj: float) -> float:
    return round(kj / 4.184, 1)
