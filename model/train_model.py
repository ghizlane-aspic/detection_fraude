# model/train_model.py (Version Finale - Correction du NameError)

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None
try:
    from lightgbm import LGBMClassifier
except ImportError:
    LGBMClassifier = None

# --- ÉTAPE 1: Chargement et préparation ---
print("1. Chargement et préparation des données...")
df = pd.read_csv('data/fraudTrain_processed.csv')
target_col = 'is_fraud'
X = df.drop(columns=[target_col])
y = df[target_col]
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- ÉTAPE 2: Définition des stratégies de prétraitement ---
low_cardinality_features = ['category', 'gender', 'state']
high_cardinality_features = ['merchant', 'city', 'job']

preprocessor_sklearn = ColumnTransformer(
    transformers=[
        ('cat_low', OneHotEncoder(handle_unknown='ignore', sparse_output=False), low_cardinality_features)
    ],
    remainder='passthrough'
)

# --- ÉTAPE 3: Entraînement et comparaison des modèles ---
print("\n2. Entraînement et comparaison des modèles...")
models_to_compare = {}
pos = (y_train == 1).sum()
neg = (y_train == 0).sum()
scale_pos_weight = float(neg) / float(pos) if pos > 0 else 1.0

# Pipeline 1: Régression Logistique
pipeline_log_reg = Pipeline(steps=[
    ('preprocessor', preprocessor_sklearn),
    ('classifier', LogisticRegression(max_iter=2000, class_weight='balanced', solver='lbfgs'))
])
models_to_compare["Régression Logistique"] = pipeline_log_reg

# Pipeline 2: Random Forest
pipeline_rf = Pipeline(steps=[
    ('preprocessor', preprocessor_sklearn),
    ('classifier', RandomForestClassifier(n_estimators=600, max_features='sqrt', class_weight='balanced', random_state=42, n_jobs=-1))
])
models_to_compare["Random Forest"] = pipeline_rf

# Pipeline 3: XGBoost
if XGBClassifier:
    pipeline_xgb = Pipeline(steps=[
        ('preprocessor', preprocessor_sklearn),
        ('classifier', XGBClassifier(n_estimators=800, max_depth=5, learning_rate=0.08, scale_pos_weight=scale_pos_weight, random_state=42, n_jobs=-1))
    ])
    models_to_compare["XGBoost"] = pipeline_xgb

# Modèle 4: LightGBM
# <-- LA CORRECTION EST ICI -->
if LGBMClassifier:
    lgbm_model = LGBMClassifier(n_estimators=1000, learning_rate=0.08, scale_pos_weight=scale_pos_weight, random_state=42, n_jobs=-1)
    models_to_compare["LightGBM"] = lgbm_model

# Entraînement et évaluation
f1_scores = {}
X_train_sklearn = X_train.drop(columns=high_cardinality_features)
X_val_sklearn = X_val.drop(columns=high_cardinality_features)

for name, model in models_to_compare.items():
    print(f"\n--- Entraînement et Évaluation de {name} ---")
    if name == "LightGBM":
        X_train_lgbm, X_val_lgbm = X_train.copy(), X_val.copy()
        for col in high_cardinality_features + low_cardinality_features:
            X_train_lgbm[col] = X_train_lgbm[col].astype('category')
            X_val_lgbm[col] = X_val_lgbm[col].astype('category')
        model.fit(X_train_lgbm, y_train)
        predictions = model.predict(X_val_lgbm)
    else:
        model.fit(X_train_sklearn, y_train)
        predictions = model.predict(X_val_sklearn)
        
    score = f1_score(y_val, predictions)
    f1_scores[name] = score
    print(classification_report(y_val, predictions))
    print(f"F1-Score: {score:.4f}")

# --- ÉTAPE 4: Sélection et Sauvegarde ---
best_model_name = max(f1_scores, key=f1_scores.get)
best_model = models_to_compare[best_model_name]

print("-" * 50)
print(f"\nMeilleur modèle choisi : {best_model_name} (F1-Score: {f1_scores[best_model_name]:.4f})")
print("\n5. Sauvegarde du meilleur modèle...")
joblib.dump(best_model, 'model/best_model.pk1')
with open('model/best_model_name.txt', 'w') as f:
    f.write(best_model_name)
print("Meilleur modèle sauvegardé avec succès.")