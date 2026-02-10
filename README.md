🧠 Power Grid Anomaly Detection using Federated Learning
📌 Project Overview

This project presents a distributed anomaly detection system for smart electrical grids based on Federated Learning and a hierarchical Edge–Fog–Cloud architecture.

The main objective is to detect abnormal electrical behaviors (such as voltage fluctuations or abnormal consumption patterns) in real time, without centralizing sensitive data. Instead of transferring raw measurements, the system relies on collaborative learning through model parameter aggregation, ensuring data privacy, scalability, and low latency.

🏗️ System Architecture

The proposed architecture follows a three-layer design:

Edge Layer
Local nodes (e.g., villages or substations) collect electrical measurements and train local AutoEncoder models in an unsupervised manner.
Raw data never leaves the Edge layer.

Fog Layer
Acts as an intermediate coordination and streaming layer.

Apache Kafka ensures real-time data streaming and message buffering

Spark Streaming performs intermediate aggregation and filtering

Cloud Layer
Responsible for global model aggregation using the Federated Averaging (FedAvg) algorithm.
The global model is redistributed back to Edge nodes to continuously improve local anomaly detection.

🧪 Methodology

Local anomaly detection is performed using AutoEncoder models implemented with scikit-learn (MLPRegressor)

Models are trained in an unsupervised manner to reconstruct normal electrical behavior

An anomaly is detected when the reconstruction error exceeds a predefined threshold

Only model parameters (weights) are shared with the Cloud, not raw data

This approach significantly reduces communication overhead while preserving data privacy.

⚙️ Technologies Used

Python

scikit-learn (AutoEncoder – MLPRegressor)

Apache Kafka (Real-time data streaming)

Apache Spark Streaming (Intermediate aggregation)

Docker & Docker Compose (Deployment and simulation)

Streamlit (Real-time dashboard visualization)

📁 Project Structure
power-grid-anomaly-detection/
│
├── data/
│   ├── raw/                # Original dataset
│   ├── clean/              # Preprocessed data
│   └── villages/           # Data split per Edge node
│
├── preprocessing/          # Data cleaning and splitting
├── edge/                   # Local training (AutoEncoder models)
│   └── models/
├── kafka/                  # Kafka producers (alerts, model updates)
├── fog/                    # Fog aggregation logic
├── cloud/                  # Federated aggregation (FedAvg)
├── dashboard/              # Streamlit monitoring dashboard
├── docker-compose.yml
└── README.md

▶️ How to Run the Project (Summary)

Start Kafka and Spark services:

docker-compose up -d


Train local models at the Edge:

python edge/train_autoencoder.py


Stream alerts and model updates:

python kafka/alert_producer.py


Launch the monitoring dashboard:

streamlit run dashboard/app.py

🎓 Academic Context

Degree: Master 2 – Artificial Intelligence & Data Science

Student: Abderrahmane Medabdellahi [C16023]

Supervisor: Dr. El Benany Med Mahmoud

University: University of Nouakchott

Date: February 10, 2026

This project was developed as part of an academic research-oriented master’s project focusing on distributed learning systems and smart grid monitoring.

🔮 Future Improvements

Integration of real sensor data

Improved explainability of anomaly detection results

Evaluation under non-IID data distributions

Deployment using Kubernetes for large-scale scenarios
