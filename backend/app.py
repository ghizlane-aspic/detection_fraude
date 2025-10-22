# on va charger le model avec joblib
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Charger le modèle ML
model = joblib.load("model/fraud_detection_model.pkl")

#definir la structure du transaction voir le model + le frontend
class Transaction(BaseModel):
    amt_log: float               # montant transformé (log)
    gender: int                  # encodé (0/1)
    city: int                    # encodé
    state: int                   # encodé
    job: int                     # encodé
    merchant: int                # encodé
    category: int                # encodé
    trans_hour: int
    trans_day: int
    trans_month: int
    trans_weekday: int
    is_weekend: int
    dist_home_merch: float
    age: int

#créer le endpoint /predict 
@app.post("/predict")
def predict(transaction: Transaction):
    # Convertir les données en DataFrame pour le modèle
    data = pd.DataFrame([transaction.dict()])

    # Prédiction
    prediction = model.predict(data)[0]              # 0 = non fraude, 1 = fraude
    probability = model.predict_proba(data)[0][1]    # probabilité de fraude

    # Retourner le résultat
    return {
        "fraudulent": bool(prediction),
        "probability": round(probability, 3)
    }

