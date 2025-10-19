import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

TRAIN_PATH = DATA_DIR / 'fraudTrain.csv'
TEST_PATH = DATA_DIR / 'fraudTest.csv'

OUTPUT_TRAIN_PATH = DATA_DIR / 'fraudTrain_processed.csv'
OUTPUT_TEST_PATH = DATA_DIR / 'fraudTest_processed.csv'
OUTPUT_TRAIN_SAMPLE_PATH = DATA_DIR / 'fraudTrain_sample10.csv'

# Columns to drop (include common index artifact)
TO_DROP = ['index', 'Unnamed: 0', 'first', 'last', 'street', 'zip', 'trans_num']


def haversine(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points on Earth (km)."""
    R = 6371.0  # Earth radius in km
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def extract_datetime_features(df: pd.DataFrame, col: str = 'trans_date_trans_time') -> None:
    df[col] = pd.to_datetime(df[col], errors='coerce', infer_datetime_format=True)
    df['trans_hour'] = df[col].dt.hour
    df['trans_day'] = df[col].dt.day
    df['trans_month'] = df[col].dt.month
    df['trans_weekday'] = df[col].dt.weekday
    df['is_weekend'] = df['trans_weekday'].isin([5, 6]).astype(int)
    df.drop(columns=[col], inplace=True)


def process(df_train: pd.DataFrame, df_test: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Drop selected columns if present
    df_train = df_train.drop(columns=[c for c in TO_DROP if c in df_train.columns])
    df_test = df_test.drop(columns=[c for c in TO_DROP if c in df_test.columns])

    # Age from DOB
    for df in (df_train, df_test):
        if 'dob' in df.columns:
            df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
            df['age'] = (pd.Timestamp('now') - df['dob']).dt.days // 365
            df.drop(columns=['dob'], inplace=True)

    # Distance home -> merchant (if columns exist in both)
    required = {'lat', 'long', 'merch_lat', 'merch_long'}
    if required.issubset(df_train.columns) and required.issubset(df_test.columns):
        for df in (df_train, df_test):
            df['dist_home_merch'] = haversine(df['lat'], df['long'], df['merch_lat'], df['merch_long'])
            df.drop(columns=['lat', 'long', 'merch_lat', 'merch_long'], inplace=True, errors='ignore')

    # Encode categorical columns (fit on combined to avoid unseen labels)
    candidate_cat = ['gender', 'city', 'state', 'job', 'merchant', 'category']
    cat_cols = [c for c in candidate_cat if c in df_train.columns and c in df_test.columns]
    for col in cat_cols:
        le = LabelEncoder()
        combined = pd.concat([df_train[col], df_test[col]], axis=0).astype(str)
        le.fit(combined)
        df_train[col] = le.transform(df_train[col].astype(str))
        df_test[col] = le.transform(df_test[col].astype(str))

    # Datetime features from transaction timestamp
    for df in (df_train, df_test):
        if 'trans_date_trans_time' in df.columns:
            extract_datetime_features(df)

    # Amount log transform (guard negative values)
    for df in (df_train, df_test):
        if 'amt' in df.columns:
            df['amt_log'] = np.log1p(df['amt'].clip(lower=0))
            df.drop(columns=['amt'], inplace=True)

    return df_train, df_test


def main() -> None:
    # Load
    df_train = pd.read_csv(TRAIN_PATH)
    df_test = pd.read_csv(TEST_PATH)

    # Process
    df_train_p, df_test_p = process(df_train, df_test)

    # Check missing values
    print("Missing values (train):", df_train_p.isna().sum().sum())
    print("Missing values (test):", df_test_p.isna().sum().sum())

    # Save
    df_train_p.to_csv(OUTPUT_TRAIN_PATH, index=False)
    df_test_p.to_csv(OUTPUT_TEST_PATH, index=False)
    # Save 10-row clean sample for dev team
    sample_n = min(10, len(df_train_p))
    df_train_p.sample(n=sample_n, random_state=42).to_csv(OUTPUT_TRAIN_SAMPLE_PATH, index=False)


if __name__ == '__main__':
    main()
