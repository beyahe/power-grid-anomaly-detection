import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import MLPRegressor

# =========================
# 1. اختيار القرية
# =========================
VILLAGE_ID = 0   # نبدأ بالقرية 0

# =========================
# 2. تحميل بيانات القرية
# =========================
df = pd.read_csv(f"data/villages/village_{VILLAGE_ID}.csv")

X = df[
    [
        "Voltage",
        "Global_active_power",
        "Global_reactive_power",
        "Global_intensity"
    ]
]

# =========================
# 3. تطبيع البيانات
# =========================
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 4. AutoEncoder
# =========================
autoencoder = MLPRegressor(
    hidden_layer_sizes=(8, 4, 8),
    max_iter=200,
    random_state=42
)

# =========================
# 5. تدريب محلي (Edge)
# =========================
autoencoder.fit(X_scaled, X_scaled)

# =========================
# 6. حفظ النموذج (ωᵢ)
# =========================
joblib.dump(autoencoder, f"edge/models/ae_village_{VILLAGE_ID}.pkl")
joblib.dump(scaler, f"edge/models/scaler_{VILLAGE_ID}.pkl")

print(f"✔ Edge training finished for village {VILLAGE_ID}")
