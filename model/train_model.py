import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

print("1. Chargement des données...")
# Le chemin commence par ../ pour remonter du dossier 'model' au dossier racine
df = pd.read_csv('data/fraudTrain_processed.csv')

# Afficher un aperçu pour vérifier que tout est ok
print("Aperçu des données chargées :")
print(df.head())

print("\n2. Préparation des données pour l'entraînement...")
# Déterminer la colonne cible selon notre cas
# Par défaut 'is_fraud' issue du preprocessing. Sinon, essayer une alternative courante.
target_col = 'is_fraud'

# Séparer features et cible
X = df.drop(columns=[target_col])
y = df[target_col]

# Split train/validation avec stratification (important pour classes déséquilibrées)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Taille du set d'entraînement : {X_train.shape}")
print(f"Taille du set de validation : {X_val.shape}")





print("\n3. Entraînement des modèles...")

# Modèle 1: Régression Logistique (baseline interprétable)
print(" - Entraînement de la Régression Logistique...")
log_reg = LogisticRegression(max_iter=2000, class_weight='balanced', solver='lbfgs', n_jobs=None)
log_reg.fit(X_train, y_train)

# Modèle 2: Random Forest (baseline robuste)
print(" - Entraînement du Random Forest...")
random_forest = RandomForestClassifier(
    n_estimators=600,
    max_depth=None,
    max_features='sqrt',
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
random_forest.fit(X_train, y_train)

# Optionnel: Gradient Boosting type XGBoost/LightGBM si disponibles
xgb_model = None
lgbm_model = None
try:
    from xgboost import XGBClassifier
    print(" - Entraînement de XGBoost (si installé)...")
    # scale_pos_weight = n_neg / n_pos pour le déséquilibre
    pos = (y_train == 1).sum()
    neg = (y_train == 0).sum()
    scale_pos_weight = float(neg) / float(pos) if pos > 0 else 1.0
    xgb_model = XGBClassifier(
        n_estimators=800,
        max_depth=5,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        random_state=42,
        scale_pos_weight=scale_pos_weight,
        tree_method='hist',
        n_jobs=-1,
        objective='binary:logistic',
        eval_metric='aucpr'
    )
    xgb_model.fit(X_train, y_train)
except Exception as e:
    print(f"   XGBoost non utilisé: {e}")

try:
    from lightgbm import LGBMClassifier
    print(" - Entraînement de LightGBM (si installé)...")
    pos = (y_train == 1).sum()
    neg = (y_train == 0).sum()
    scale_pos_weight = float(neg) / float(pos) if pos > 0 else 1.0
    lgbm_model = LGBMClassifier(
        n_estimators=1000,
        num_leaves=63,
        learning_rate=0.08,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=0.0,
        random_state=42,
        scale_pos_weight=scale_pos_weight,
        objective='binary'
    )
    lgbm_model.fit(X_train, y_train)
except Exception as e:
    print(f"   LightGBM non utilisé: {e}")

print("Entraînement terminé !")




# Suite de train_model.py

print("\n4. Évaluation des modèles...")

# Dictionnaire pour stocker les modèles entraînés et leurs prédictions
models = {
    "Régression Logistique": log_reg,
    "Random Forest": random_forest
}
# Ajoute les modèles optionnels s'ils ont été entraînés avec succès
if xgb_model:
    models["XGBoost"] = xgb_model
if lgbm_model:
    models["LightGBM"] = lgbm_model

# Dictionnaire pour stocker les scores F1
f1_scores = {}

# Boucle pour évaluer chaque modèle
for name, model in models.items():
    print(f"\n--- Performances de {name} ---")
    predictions = model.predict(X_val)
    
    # Calculer et stocker le F1-score
    score = f1_score(y_val, predictions)
    f1_scores[name] = score
    
    # Afficher le rapport complet
    print(classification_report(y_val, predictions))
    print(f"F1-Score: {score:.4f}")

# Sélection du meilleur modèle basé sur le F1-score le plus élevé
best_model_name = max(f1_scores, key=f1_scores.get)
best_model = models[best_model_name]
best_score = f1_scores[best_model_name]

print("-" * 50)
print(f"\nMeilleur modèle choisi : {best_model_name} (F1-Score: {best_score:.4f})")
print("-" * 50)


# Sauvegarde du meilleur modèle
print("\n5. Sauvegarde du meilleur modèle...")
joblib.dump(best_model, 'model/modele.pk1')
print("Modèle sauvegardé avec succès dans 'model/modele.pk1'")




# Suite de train_model.py

print("\n4. Évaluation des modèles...")

# Dictionnaire pour stocker les modèles entraînés et leurs prédictions
models = {
    "Régression Logistique": log_reg,
    "Random Forest": random_forest
}
# Ajoute les modèles optionnels s'ils ont été entraînés avec succès
if xgb_model:
    models["XGBoost"] = xgb_model
if lgbm_model:
    models["LightGBM"] = lgbm_model

# Dictionnaire pour stocker les scores F1
f1_scores = {}

# Boucle pour évaluer chaque modèle
for name, model in models.items():
    print(f"\n--- Performances de {name} ---")
    predictions = model.predict(X_val)
    
    # Calculer et stocker le F1-score
    score = f1_score(y_val, predictions)
    f1_scores[name] = score
    
    # Afficher le rapport complet
    print(classification_report(y_val, predictions))
    print(f"F1-Score: {score:.4f}")

# Sélection du meilleur modèle basé sur le F1-score le plus élevé
best_model_name = max(f1_scores, key=f1_scores.get)
best_model = models[best_model_name]
best_score = f1_scores[best_model_name]

print("-" * 50)
print(f"\nMeilleur modèle choisi : {best_model_name} (F1-Score: {best_score:.4f})")
print("-" * 50)


# Sauvegarde du meilleur modèle
print("\n5. Sauvegarde du meilleur modèle...")
joblib.dump(best_model, 'model/modele.pk1')
print("Modèle sauvegardé avec succès dans 'model/modele.pk1'")