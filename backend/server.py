import numpy as np
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

# IMPORTING FROM OUR MODULES
import config
from models.anomaly_detector import AnomalyDetector
from models.federated_core import FederatedServer

app = Flask(__name__)
CORS(app) 

# --- GLOBAL STATE MANAGEMENT ---
local_data_buffer = []
warning_counter = 0        
last_stable_reading = None 
alarm_countdown = 0
locked_baseline = None
last_heartbeat_time = 0

# --- ACCURACY METRICS ---
total_predictions = 0
correct_predictions = 0
current_accuracy = 100.0 # Starts perfect

# --- INSTANTIATE SYSTEMS ---
fml_server = FederatedServer()
detector = AnomalyDetector(contamination=config.ML_CONTAMINATION)

@app.route('/update_sensor', methods=['POST'])
def receive_data():
    global local_data_buffer, warning_counter, last_stable_reading, alarm_countdown, locked_baseline, last_heartbeat_time
    global total_predictions, correct_predictions, current_accuracy
    
    last_heartbeat_time = time.time()
    
    content = request.json
    current_distance = float(content['distance'])

    content = request.json
    raw_distance = float(content['distance'])

    # FILTER: If sensor sends 0 (error), use the last known good value
    if raw_distance <= 0.0:
        if len(local_data_buffer) > 0:
            current_distance = local_data_buffer[-1] # Use previous reading
        else:
            current_distance = 0.0 # Start at 0 if no history
    else:
        current_distance = raw_distance
    
    
    local_data_buffer.append(current_distance)
    if len(local_data_buffer) > config.TRAINING_BATCH_SIZE: 
        local_data_buffer.pop(0)

    # 1. INITIALIZE STABLE READING
    if last_stable_reading is None:
        last_stable_reading = current_distance
        locked_baseline = current_distance

    # 2. LOGIC: CHECK FOR DROP (GROUND TRUTH)
    diff = current_distance - last_stable_reading
    is_theft_logic = False # Ground Truth
    
    if diff > config.THEFT_THRESHOLD:
        is_theft_logic = True
    elif diff < -1:
        last_stable_reading = current_distance
        locked_baseline = current_distance
        warning_counter = 0
        alarm_countdown = 0 
        
    # 3. ML PREDICTION CHECK (COMPARISON)
    # We compare what the Logic "Knows" vs what ML "Guessed"
    ml_pred, ml_score = detector.predict(current_distance)
    
    # ML returns -1 for anomaly (Theft), 1 for normal
    ml_says_theft = (ml_pred == -1)
    
    # Update Accuracy Stats
    if len(local_data_buffer) > 5: # Only count after warmup
        total_predictions += 1
        # It's correct if BOTH say theft OR BOTH say normal
        if is_theft_logic == ml_says_theft:
            correct_predictions += 1
            
        # Calculate Percentage
        if total_predictions > 0:
            current_accuracy = (correct_predictions / total_predictions) * 100.0

    # 4. ALARM LOGIC
    if is_theft_logic:
        warning_counter += 1
        if warning_counter == config.CONFIRMATION_LIMIT:
            print("!!! THEFT CONFIRMED - STARTING ALARM SEQUENCE !!!")
            alarm_countdown = config.ALARM_DURATION_CYCLES 
        elif warning_counter > config.CONFIRMATION_LIMIT:
            pass
    else:
        warning_counter = 0

    # 5. DETERMINE COMMAND
    command = 0
    if alarm_countdown > 0:
        command = 1
        alarm_countdown -= 1 
    else:
        command = 0 

    # 6. SIMULATIONS
    if len(local_data_buffer) % 10 == 0:
        if len(local_data_buffer) > 2:
            dummy_weights = [np.var(local_data_buffer[-10:]), np.var(local_data_buffer[-20:-10])]
            threading.Thread(target=fml_server.fed_avg, args=(dummy_weights,)).start()

    if len(local_data_buffer) > 15 and len(local_data_buffer) % config.RETRAIN_INTERVAL == 0:
        detector.train(local_data_buffer)

    return jsonify({"command": command})

@app.route('/status', methods=['GET'])
def get_status():
    global local_data_buffer, warning_counter, locked_baseline, alarm_countdown, last_heartbeat_time, current_accuracy
    
    current_level = local_data_buffer[-1] if local_data_buffer else 0
    status_text = "NORMAL"

    if time.time() - last_heartbeat_time > 5:
        status_text = "OFFLINE"
        alarm_countdown = 0
        warning_counter = 0
    else:
        if alarm_countdown > 0:
            status_text = "THEFT DETECTED"
        elif warning_counter > 0:
            status_text = "WARNING"
        
    return jsonify({
        "level": current_level,
        "status": status_text,
        "baseline": locked_baseline if locked_baseline else 0,
        "history": local_data_buffer[-20:],
        "accuracy": f"{current_accuracy:.1f}%" # <--- SEND ACCURACY TO FRONTEND
    })

if __name__ == '__main__':
    print("--- SECURE FUEL MONITORING SYSTEM STARTED ---")
    last_heartbeat_time = time.time() 
    app.run(host='0.0.0.0', port=5000)