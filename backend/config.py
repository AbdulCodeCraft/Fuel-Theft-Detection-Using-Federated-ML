# --- SYSTEM CONFIGURATION ---

# Tank Specifications
TANK_HEIGHT_CM = 11.0

# Theft Detection Sensitivity
THEFT_THRESHOLD = 2.0      # 2cm drop triggers potential theft
CONFIRMATION_LIMIT = 3     # Wait 3 readings to confirm (ignores shakes)

# Hardware Alarm Settings
ALARM_DURATION_CYCLES = 4  # Alarm stays ON for ~5 seconds after detection

# Machine Learning Settings
ML_CONTAMINATION = 0.1     # Expected anomaly rate (10%)
TRAINING_BATCH_SIZE = 50   # How many readings to keep in memory
RETRAIN_INTERVAL = 5       # How often to retrain the model