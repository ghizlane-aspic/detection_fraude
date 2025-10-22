# prediction_example.py (Version Finale et Définitive - Gère tous les cas de figure)

import joblib
import pandas as pd

# --- CONFIGURATION ---
MODEL_PATH = 'model/best_model.pk1'
MODEL_NAME_PATH = 'model/best_model_name.txt'

# --- CHARGEMENT DU MODÈLE ET DE SON NOM ---
print(f"Chargement du modèle depuis : {MODEL_PATH}")
try:
    model = joblib.load(MODEL_PATH)
    with open(MODEL_NAME_PATH, 'r') as f:
        # .strip() est important pour enlever les espaces ou sauts de ligne accidentels
        model_name = f.read().strip()
    print(f"Modèle '{model_name}' chargé avec succès.")
except FileNotFoundError:
    print(f"ERREUR: Le fichier du modèle '{MODEL_PATH}' ou '{MODEL_NAME_PATH}' est introuvable.")
    print("Veuillez d'abord lancer le script 'model/train_model.py'.")
    exit()

def make_prediction(transaction_data: dict):
    """
    Prédit la fraude en utilisant le meilleur modèle sauvegardé.
    Applique le prétraitement approprié en fonction du type de modèle.
    """
    try:
        df = pd.DataFrame(transaction_data, index=[0])

        # --- LOGIQUE DE PRÉTRAITEMENT CONDITIONNELLE ---
        # Applique le bon traitement en fonction du modèle qui a été sauvegardé.
        if model_name == 'LightGBM':
            # Pour LightGBM, on convertit toutes les colonnes catégorielles
            categorical_features = ['merchant', 'category', 'gender', 'city', 'state', 'job']
            for col in categorical_features:
                if col in df.columns:
                    df[col] = df[col].astype('category')
        else:
            # Pour les autres modèles (RandomForest, etc.), on SUPPRIME les colonnes
            # à haute cardinalité qu'ils ne savent pas gérer.
            high_cardinality_features = ['merchant', 'city', 'job']
            df = df.drop(columns=high_cardinality_features, errors='ignore')

        # Le modèle (qu'il soit un pipeline ou un modèle simple) est maintenant prêt
        prediction = model.predict(df)
        probability = model.predict_proba(df)[0][1]

        result = {
            'prediction': int(prediction[0]),
            'fraud_probability': float(probability)
        }
        return result
    except Exception as e:
        return {'error': str(e)}

# --- EXEMPLE D'UTILISATION (ne change pas) ---
if __name__ == '__main__':
    # Cet exemple contient TOUTES les colonnes originales, simulant une entrée réelle.
    example_transaction = {
        'cc_num': 4212345678901234,
        'merchant': 'fraud_Rath, Heaney and Vandervort',
        'category': 'shopping_pos',
        'gender': 'M',
        'city': 'New York',
        'state': 'NY',
        'job': 'Software engineer',
        'city_pop': 8400000,
        'unix_time': 1371816895,
        'age': 35,
        'dist_home_merch': 2.5,
        'trans_hour': 14,
        'trans_day': 3,
        'trans_month': 7,
        'trans_weekday': 3,
        'is_weekend': 0,
        'amt_log': 4.83
    }

    print("\n--- Test de prédiction sur une transaction exemple ---")
    prediction_result = make_prediction(example_transaction)
    
    print("\n--- Résultat ---")
    if 'error' in prediction_result:
        print(f"Une erreur est survenue : {prediction_result['error']}")
    else:
        is_fraud = "FRAUDE DÉTECTÉE" if prediction_result['prediction'] == 1 else "Transaction légitime"
        prob_percent = prediction_result['fraud_probability'] * 100
        print(f"Prédiction : {is_fraud}")
        print(f"Probabilité de fraude : {prob_percent:.2f}%")