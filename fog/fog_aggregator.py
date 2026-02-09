import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "model-updates",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("Fog en attente des modèles...")

for message in consumer:
    data = message.value
    print(f"✔ Modèle reçu depuis village {data['village_id']}")
    break
