"""
generate_dataset.py
====================
Generates a realistic synthetic housing dataset modelled after the
Ames, Iowa "House Prices -- Advanced Regression" Kaggle competition.

This ensures the project runs out-of-the-box without a Kaggle account.
"""

import os
import numpy as np
import pandas as pd


def generate_housing_dataset(
    n_samples: int = 1460,
    seed: int = 42,
    output_path: str = "data/raw/house_prices.csv",
) -> pd.DataFrame:
    """
    Create a synthetic housing dataset with realistic feature distributions.

    Parameters
    ----------
    n_samples : int
        Number of rows to generate.
    seed : int
        Random seed for reproducibility.
    output_path : str
        Path to save the CSV file.

    Returns
    -------
    pd.DataFrame
        Generated dataset.
    """
    rng = np.random.default_rng(seed)

    # -- Numeric features ----------------------------------------------
    overall_qual = rng.integers(1, 11, size=n_samples)          # 1-10
    gr_liv_area = rng.normal(1500, 400, n_samples).clip(400, 5000).astype(int)
    total_bsmt_sf = rng.normal(1000, 300, n_samples).clip(0, 3000).astype(int)
    first_flr_sf = rng.normal(1100, 300, n_samples).clip(400, 3000).astype(int)
    second_flr_sf = rng.choice(
        [0] * 5 + list(range(300, 1800, 50)), size=n_samples
    )
    lot_area = rng.normal(10500, 4000, n_samples).clip(1300, 50000).astype(int)
    lot_frontage = rng.normal(70, 20, n_samples).clip(20, 200).astype(float)
    year_built = rng.integers(1900, 2024, size=n_samples)
    year_remod_add = np.maximum(year_built, rng.integers(1950, 2024, size=n_samples))
    yr_sold = rng.integers(2006, 2024, size=n_samples)
    garage_cars = rng.choice([0, 1, 2, 3], size=n_samples, p=[0.05, 0.25, 0.55, 0.15])
    garage_area = (garage_cars * rng.normal(220, 40, n_samples)).clip(0, 1200).astype(int)
    full_bath = rng.choice([1, 2, 3], size=n_samples, p=[0.35, 0.55, 0.10])
    half_bath = rng.choice([0, 1, 2], size=n_samples, p=[0.55, 0.40, 0.05])
    bedrooms = rng.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.03, 0.15, 0.45, 0.30, 0.07])
    kitchen_abv_gr = rng.choice([1, 2], size=n_samples, p=[0.90, 0.10])
    kitchen_qual_num = rng.choice([2, 3, 4, 5], size=n_samples, p=[0.05, 0.35, 0.45, 0.15])
    fireplaces = rng.choice([0, 1, 2, 3], size=n_samples, p=[0.45, 0.40, 0.12, 0.03])
    wood_deck_sf = rng.exponential(80, n_samples).clip(0, 800).astype(int)
    open_porch_sf = rng.exponential(40, n_samples).clip(0, 400).astype(int)
    enclosed_porch = rng.exponential(15, n_samples).clip(0, 300).astype(int)
    pool_area = rng.choice(
        [0] * 50 + list(range(200, 800, 50)), size=n_samples
    )
    misc_val = rng.choice([0] * 20 + [500, 1000, 2000, 4000], size=n_samples)
    mo_sold = rng.integers(1, 13, size=n_samples)

    # -- Categorical features -----------------------------------------
    neighborhoods = [
        "CollgCr", "Veenker", "Crawfor", "NoRidge", "Mitchel",
        "Somerst", "NWAmes", "OldTown", "BrkSide", "Sawyer",
        "NridgHt", "NAmes", "SawyerW", "IDOTRR", "MeadowV",
        "Edwards", "Timber", "Gilbert", "StoneBr", "ClearCr",
    ]
    neighborhood = rng.choice(neighborhoods, size=n_samples)

    ms_zoning = rng.choice(
        ["RL", "RM", "FV", "RH", "C (all)"],
        size=n_samples,
        p=[0.60, 0.15, 0.10, 0.10, 0.05],
    )

    bldg_type = rng.choice(
        ["1Fam", "2fmCon", "Duplex", "TwnhsE", "Twnhs"],
        size=n_samples,
        p=[0.70, 0.05, 0.08, 0.12, 0.05],
    )

    house_style = rng.choice(
        ["1Story", "2Story", "1.5Fin", "SLvl", "SFoyer"],
        size=n_samples,
        p=[0.40, 0.35, 0.10, 0.10, 0.05],
    )

    exterior = rng.choice(
        ["VinylSd", "HdBoard", "MetalSd", "Wd Sdng", "Plywood", "CemntBd", "BrkFace"],
        size=n_samples,
    )

    foundation = rng.choice(
        ["PConc", "CBlock", "BrkTil", "Slab"],
        size=n_samples,
        p=[0.45, 0.35, 0.12, 0.08],
    )

    heating_qc = rng.choice(["Ex", "Gd", "TA", "Fa", "Po"], size=n_samples, p=[0.25, 0.35, 0.30, 0.08, 0.02])
    central_air = rng.choice(["Y", "N"], size=n_samples, p=[0.93, 0.07])

    garage_type = rng.choice(
        ["Attchd", "Detchd", "BuiltIn", "CarPort", "None"],
        size=n_samples,
        p=[0.55, 0.25, 0.10, 0.03, 0.07],
    )

    sale_type = rng.choice(
        ["WD", "New", "COD", "Con", "Oth"],
        size=n_samples,
        p=[0.75, 0.10, 0.08, 0.04, 0.03],
    )

    sale_condition = rng.choice(
        ["Normal", "Abnorml", "Partial", "AdjLand", "Family"],
        size=n_samples,
        p=[0.67, 0.10, 0.13, 0.05, 0.05],
    )

    condition1 = rng.choice(
        ["Norm", "Feedr", "Artery", "PosN", "PosA"],
        size=n_samples,
        p=[0.75, 0.10, 0.07, 0.05, 0.03],
    )

    # -- Map kitchen quality to label ----------------------------------
    kq_map = {2: "Fa", 3: "TA", 4: "Gd", 5: "Ex"}
    kitchen_qual = np.array([kq_map[v] for v in kitchen_qual_num])

    # -- Target: SalePrice (realistic formula + noise) -----------------
    neighborhood_premium = {n: rng.uniform(0.85, 1.25) for n in neighborhoods}
    nb_factor = np.array([neighborhood_premium[n] for n in neighborhood])

    base_price = (
        overall_qual * 12000
        + gr_liv_area * 55
        + total_bsmt_sf * 30
        + garage_cars * 8000
        + (2024 - np.abs(2024 - year_built)) * 150
        + fireplaces * 5000
        + kitchen_qual_num * 4000
        + full_bath * 6000
        + lot_area * 1.5
    )
    noise = rng.normal(1.0, 0.08, n_samples)
    sale_price = (base_price * nb_factor * noise).clip(30000, 800000).astype(int)

    # -- Inject ~5 % missing values in selected columns ----------------
    def inject_na(arr, frac=0.05):
        mask = rng.random(len(arr)) < frac
        arr = arr.astype(float)
        arr[mask] = np.nan
        return arr

    lot_frontage = inject_na(lot_frontage, 0.17)  # realistic ~17 % missing
    garage_area_f = inject_na(garage_area.astype(float), 0.03)
    total_bsmt_sf_f = inject_na(total_bsmt_sf.astype(float), 0.02)

    # -- Assemble DataFrame --------------------------------------------
    df = pd.DataFrame(
        {
            "MSZoning": ms_zoning,
            "LotFrontage": lot_frontage,
            "LotArea": lot_area,
            "Neighborhood": neighborhood,
            "BldgType": bldg_type,
            "HouseStyle": house_style,
            "OverallQual": overall_qual,
            "OverallCond": rng.integers(1, 10, size=n_samples),
            "YearBuilt": year_built,
            "YearRemodAdd": year_remod_add,
            "Exterior1st": exterior,
            "Foundation": foundation,
            "TotalBsmtSF": total_bsmt_sf_f,
            "HeatingQC": heating_qc,
            "CentralAir": central_air,
            "1stFlrSF": first_flr_sf,
            "2ndFlrSF": second_flr_sf,
            "GrLivArea": gr_liv_area,
            "FullBath": full_bath,
            "HalfBath": half_bath,
            "BedroomAbvGr": bedrooms,
            "KitchenAbvGr": kitchen_abv_gr,
            "KitchenQual": kitchen_qual,
            "Fireplaces": fireplaces,
            "GarageType": garage_type,
            "GarageCars": garage_cars,
            "GarageArea": garage_area_f,
            "WoodDeckSF": wood_deck_sf,
            "OpenPorchSF": open_porch_sf,
            "EnclosedPorch": enclosed_porch,
            "PoolArea": pool_area,
            "MiscVal": misc_val,
            "MoSold": mo_sold,
            "YrSold": yr_sold,
            "SaleType": sale_type,
            "SaleCondition": sale_condition,
            "Condition1": condition1,
            "SalePrice": sale_price,
        }
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[OK] Generated {len(df)} rows -> {output_path}")
    return df


if __name__ == "__main__":
    generate_housing_dataset()
