import json
from kafka import KafkaProducer

# نرسل نموذج القرية 0 كمثال
VILLAGE_ID = 0

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

message = {
    "village_id": VILLAGE_ID,
    "model_name": f"ae_village_{VILLAGE_ID}.pkl"
}

producer.send("model-updates", message)
producer.flush()

print("✔ ωᵢ envoyé au Fog via Kafka")
