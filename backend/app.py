# on va charger le model avec joblib
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Charger le modèle ML
MODEL_PATH = "../model/best_model.pk1"  
MODEL_NAME_PATH = "../model/best_model_name.txt"

try:
    model = joblib.load(MODEL_PATH)
    with open(MODEL_NAME_PATH, "r") as f:
        model_name = f.read().strip()
    print(f"[INFO] Modèle '{model_name}' chargé avec succès")
except Exception as e:
    print(f"[ERREUR] Impossible de charger le modèle : {e}")
    model = None
    model_name = None

#definir la structure du transaction voir le model + le frontend
class Transaction(BaseModel):
    cc_num: float
    merchant: str
    category: str
    gender: str
    city: str
    state: str
    city_pop: int
    job: str
    unix_time: int
    age: int
    dist_home_merch: float
    trans_hour: int
    trans_day: int
    trans_month: int
    trans_weekday: int
    is_weekend: int
    amt_log: float
# fonction de prediction

def make_prediction(transaction_data: dict):
    try:
        df = pd.DataFrame(transaction_data, index=[0])

        if model_name == "LightGBM":
            categorical_features = ["merchant", "category", "gender", "city", "state", "job"]
            for col in categorical_features:
                if col in df.columns:
                    df[col] = df[col].astype("category")
        else:
            high_cardinality_features = ["merchant", "city", "job"]
            df = df.drop(columns=high_cardinality_features, errors="ignore")

        prediction = model.predict(df)
        probability = model.predict_proba(df)[0][1]

        return {
            "prediction": int(prediction[0]),
            "fraud_probability": round(float(probability), 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction : {str(e)}")

#créer le endpoint /predict 
@app.post("/predict")
async def predict_transaction(data: dict):
    """
    Reçoit les données d'une transaction depuis le front-end
    et retourne la prédiction (fraude ou non).
    """
    if model is None:
        raise HTTPException(status_code=500, detail="Modèle non chargé.")
    result = make_prediction(data)
    return {
        "is_fraud": bool(result["prediction"]),
        "fraud_probability": result["fraud_probability"],
        "message": "FRAUDE DÉTECTÉE " if result["prediction"] == 1 else "Transaction légitime "
    }
