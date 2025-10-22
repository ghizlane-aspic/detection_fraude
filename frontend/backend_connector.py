import os
import pickle
import requests
import json
from datetime import datetime

try:
    import numpy as np
except ImportError:
    np = None

class FraudDetector:
    def __init__(self):
        self.is_loaded = False
        self.model = None
        self.model_name = "Random Forest"
        self.backend_url = "http://localhost:5000/predict"
        self.timeout = 30
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_dir = os.path.join(project_root, 'model')
        
        self._load_model()
    
    def _load_model(self):
        """Charge le modèle ML depuis les fichiers locaux"""
        try:
            model_path = os.path.join(self.model_dir, 'best_model.pk1')
            model_name_path = os.path.join(self.model_dir, 'best_model_name.txt')
            
            print(f"🔍 Recherche du modèle dans: {self.model_dir}")
            
            if os.path.exists(model_path) and os.path.exists(model_name_path):
                print("✅ Fichiers de modèle trouvés, chargement...")
                
                with open(model_name_path, 'r') as f:
                    self.model_name = f.read().strip()
                    print(f"📝 Nom du modèle: {self.model_name}")
                
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                
                self.is_loaded = True
                print(f"✅ Modèle {self.model_name} chargé avec succès")
                
            else:
                print("🔄 Mode simulation activé - modèle non trouvé")
                if not os.path.exists(model_path):
                    print(f"❌ Fichier modèle manquant: {model_path}")
                if not os.path.exists(model_name_path):
                    print(f"❌ Fichier nom modèle manquant: {model_name_path}")
                
        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            self.is_loaded = False
    
    def _prepare_features(self, input_data):
        """Prépare les features pour la prédiction (identique au backend)"""
        # Mapping cohérent avec ce que le backend attend
        category_mapping = {
            "Supermarché": 0, "Restaurant": 1, "Essence": 2,
            "Shopping/Vêtements": 3, "Pharmacie": 4, "Transport": 5,
            "Loisirs": 6, "En ligne": 7, "Voyage": 8, "Autre": 9
        }
        
        job_mapping = {
            "Employé": 0, "Cadre": 1, "Commerçant": 2,
            "Retraité": 3, "Étudiant": 4, "Autre": 5
        }
        
        gender_mapping = {"Homme": 0, "Femme": 1}
        
        features = {
            'amount': float(input_data['amount']),
            'category': category_mapping.get(input_data['category'], 9),
            'gender': gender_mapping.get(input_data['gender'], 0),
            'age': int(input_data['age']),
            'job': job_mapping.get(input_data['job'], 5),
            'distance': float(input_data['distance']),
            'trans_hour': int(input_data['trans_hour']),
            'is_weekend': 1 if input_data['is_weekend'] else 0
        }
        
        return features
    
    def predict(self, input_data):
        """
        Fait une prédiction de fraude
        Priorité: 1. Backend API, 2. Modèle local, 3. Simulation
        """
        print(f"🎯 Début prédiction pour transaction: {input_data['amount']}€")
        
        # Essayer d'abord le backend API
        api_result = self._try_backend_prediction(input_data)
        if api_result['success']:
            print("✅ Prédiction réussie via backend API")
            return api_result
        
        # Essayer le modèle local
        local_result = self._try_local_prediction(input_data)
        if local_result['success']:
            print("✅ Prédiction réussie via modèle local")
            return local_result
        
        # Fallback vers la simulation
        print("🔄 Utilisation du mode simulation (fallback)")
        return self._simulate_prediction(input_data)
    
    def _try_backend_prediction(self, input_data):
        """Tente une prédiction via l'API backend - STRUCTURE CORRECTE"""
        try:
            # STRUCTURE CORRECTE pour le backend
            request_data = {
                'transaction': {
                    'amount': float(input_data['amount']),
                    'merchant': str(input_data['merchant']),
                    'category': str(input_data['category']),
                    'gender': str(input_data['gender']),
                    'age': int(input_data['age']),
                    'job': str(input_data['job']),
                    'city': str(input_data['city']),
                    'distance': float(input_data['distance']),
                    'trans_hour': int(input_data['trans_hour']),
                    'is_weekend': bool(input_data['is_weekend'])
                },
                'metadata': {
                    'request_id': f'req_{int(datetime.now().timestamp())}',
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0'
                }
            }
            
            print("📤 Envoi des données au backend...")
            response = requests.post(
                self.backend_url,
                json=request_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Backend response: {result}")
                return {
                    'success': True,
                    'is_fraud': result.get('is_fraud', False),
                    'fraud_probability': float(result.get('fraud_probability', 0.0)),
                    'risk_score': int(result.get('risk_score', 0)),
                    'model_used': result.get('model_used', 'Backend API'),
                    'risk_factors': result.get('risk_factors', [])
                }
            else:
                print(f"❌ Erreur backend HTTP {response.status_code}: {response.text}")
                return {'success': False, 'error': f"Backend error: {response.status_code}"}
                
        except requests.exceptions.ConnectionError:
            print("🔌 Backend non disponible - connexion refusée")
            return {'success': False, 'error': 'Backend non disponible'}
        except requests.exceptions.Timeout:
            print("⏱️ Timeout du backend")
            return {'success': False, 'error': 'Timeout du backend'}
        except Exception as e:
            print(f"❌ Erreur API: {e}")
            return {'success': False, 'error': f'Erreur API: {str(e)}'}
    
    def _try_local_prediction(self, input_data):
        """Tente une prédiction avec le modèle local - VÉRITABLE IMPLÉMENTATION"""
        if not self.is_loaded or self.model is None:
            return {'success': False, 'error': 'Modèle local non disponible'}
        
        try:
            # Préparer les features pour le modèle
            features = self._prepare_features(input_data)
            print(f"🔧 Features préparées: {features}")
            
            # Convertir en array numpy pour la prédiction
            feature_array = np.array([list(features.values())])
            print(f"🔢 Shape des features: {feature_array.shape}")
            
            # Faire la prédiction
            prediction = self.model.predict(feature_array)[0]
            print(f"🔮 Prédiction: {prediction}")
            
            # Obtenir les probabilités
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(feature_array)[0]
                probability = probabilities[1]  # Probabilité de fraude
                print(f"📊 Probabilités: {probabilities}")
            else:
                probability = 1.0 if prediction == 1 else 0.0
                print("⚠️ predict_proba non disponible, utilisation valeur par défaut")
            
            # Calculer le score de risque
            risk_score = int(probability * 100)
            is_fraud = bool(prediction == 1)
            
            # Identifier les facteurs de risque
            risk_factors = self._identify_risk_factors(input_data)
            
            result = {
                'success': True,
                'is_fraud': is_fraud,
                'fraud_probability': float(probability),
                'risk_score': risk_score,
                'model_used': self.model_name,
                'risk_factors': risk_factors
            }
            
            print(f"🎯 Résultat prédiction locale: {result}")
            return result
            
        except Exception as e:
            print(f"❌ Erreur prédiction locale: {e}")
            return {'success': False, 'error': f'Erreur modèle local: {str(e)}'}
    
    def _simulate_prediction(self, input_data):
        """Simulation de prédiction (fallback) - LOGIQUE AMÉLIORÉE"""
        print("🔄 Utilisation du mode simulation")
        
        risk_score = 0
        risk_factors = []
        
        amount = input_data['amount']
        trans_hour = input_data['trans_hour']
        distance = input_data['distance']
        category = input_data['category']
        is_weekend = input_data['is_weekend']
        
        # Logique de risque plus réaliste
        if amount > 2000:
            risk_score += 35
            risk_factors.append("💰 Montant très élevé (>2000€)")
        elif amount > 1000:
            risk_score += 20
            risk_factors.append("💸 Montant élevé (1000-2000€)")
        
        if trans_hour < 6 or trans_hour > 22:
            risk_score += 25
            risk_factors.append("🌙 Heure inhabituelle")
        
        if distance > 500:
            risk_score += 30
            risk_factors.append("✈️ Très loin du domicile")
        elif distance > 100:
            risk_score += 15
            risk_factors.append("🚗 Distance importante")
        
        if category in ["En ligne", "Voyage"]:
            risk_score += 15
            risk_factors.append(f"🎯 Catégorie à risque: {category}")
        
        # Calcul final
        probability = min(risk_score / 100, 0.99)
        is_fraud = probability > 0.5
        
        print(f"🎲 Simulation - Risque: {risk_score}%, Fraude: {is_fraud}")
        
        return {
            'success': True,
            'is_fraud': is_fraud,
            'fraud_probability': probability,
            'risk_score': risk_score,
            'model_used': 'Simulation',
            'risk_factors': risk_factors
        }
    
    def _identify_risk_factors(self, input_data):
        """Identifie les facteurs de risque pour l'affichage"""
        risk_factors = []
        amount = input_data['amount']
        trans_hour = input_data['trans_hour']
        distance = input_data['distance']
        category = input_data['category']
        
        if amount > 1000:
            risk_factors.append(f"💰 Montant élevé: {amount}€")
        if trans_hour < 6 or trans_hour > 22:
            risk_factors.append(f"🌙 Heure inhabituelle: {trans_hour}h")
        if distance > 100:
            risk_factors.append(f"🚗 Longue distance: {distance}km")
        if category in ["En ligne", "Voyage"]:
            risk_factors.append(f"🎯 Catégorie à risque: {category}")
        
        return risk_factors

# Instance globale
fraud_detector = FraudDetector()