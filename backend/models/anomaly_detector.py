import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """
    Uses Isolation Forest to detect fuel theft (anomalies) 
    based on unsupervised learning.
    """
    def __init__(self, contamination=0.1):
        # contamination means we expect roughly X% of data to be anomalies
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False

    def train(self, data):
        """
        Retrains the model on the latest batch of sensor data.
        """
        if len(data) < 2:
            return # Not enough data to train

       
        X = np.array(data).reshape(-1, 1)
        self.model.fit(X)
        self.is_trained = True
        print("[ML KERNEL] Isolation Forest Model Retrained on new batch.")

    def predict(self, value):
        """
        Returns:
            prediction: -1 (Theft) or 1 (Normal)
            score: The anomaly score (lower is more anomalous)
        """
        if not self.is_trained:
            return 0, 0.0 # Not enough data yet
        
        X_test = np.array([[value]])
        
        prediction = self.model.predict(X_test)
        score = self.model.decision_function(X_test)
        
        return prediction[0], score[0]