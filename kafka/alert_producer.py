import json
import time
import random
import numpy as np
import joblib
from kafka import KafkaProducer
from collections import deque

# =============================
# Load AutoEncoder model
# =============================
model = joblib.load("edge/models/ae_village_0.pkl")

# =============================
# Kafka Producer
# =============================
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# =============================
# Logical villages (generic)
# =============================
VILLAGES = [
    "Village 1",
    "Village 2",
    "Village 3",
    "Village 4",
    "Village 5"
]

# =============================
# Feature names (for explainability)
# =============================
feature_names = [
    "voltage",
    "current",
    "reactive_power",
    "intensity"
]

# =============================
# Error history for dynamic threshold
# =============================
error_history = deque(maxlen=100)

print("🚀 Alert producer started (Dynamic Threshold + Explainability)")

# =============================
# Streaming loop
# =============================
while True:
    village = random.choice(VILLAGES)

    # =============================
    # Simulated measurements
    # 80% normal / 20% abnormal
    # =============================
    if random.random() < 0.2:  # Fault simulation
        voltage = random.randint(300, 380)   # Over-voltage
        current = random.randint(40, 80)     # Over-current
    else:
        voltage = random.randint(180, 260)
        current = random.randint(5, 30)

    reactive_power = 0.5
    intensity = 10

    # =============================
    # Feature vector (same structure as training)
    # =============================
    X = np.array([[voltage, current, reactive_power, intensity]], dtype=float)
    X_norm = X / X.max()

    # =============================
    # AutoEncoder inference
    # =============================
    recon = model.predict(X_norm)
    error = float(np.mean((X_norm - recon) ** 2))

    # =============================
    # Update error history
    # =============================
    error_history.append(error)

    # =============================
    # Dynamic threshold
    # =============================
    if len(error_history) > 20:
        threshold = float(np.percentile(error_history, 95))
    else:
        threshold = 0.001

    # =============================
    # Anomaly decision
    # =============================
    anomaly = bool(error > threshold)

    # =============================
    # Health Score (0–100)
    # =============================
    health_score = max(
        0,
        min(100, int(100 * (1 - error / (threshold + 1e-6))))
    )

    # =============================
    # Explainability (Root Cause)
    # =============================
    contributions = np.abs(X_norm - recon)[0]
    root_cause = feature_names[int(np.argmax(contributions))]

    # =============================
    # Alert message
    # =============================
    alert = {
        "village": village,
        "voltage": int(voltage),
        "current": int(current),
        "error": round(error, 6),
        "threshold": round(threshold, 6),
        "anomaly": anomaly,
        "health_score": health_score,
        "root_cause": root_cause,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # =============================
    # Send to Kafka
    # =============================
    producer.send("alerts", alert)
    producer.flush()

    print(
        f"[{village}] "
        f"error={error:.6f} | "
        f"threshold={threshold:.6f} | "
        f"health={health_score} | "
        f"cause={root_cause}"
    )

    time.sleep(2)
