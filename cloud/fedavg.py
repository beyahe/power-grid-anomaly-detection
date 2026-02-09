import joblib
import numpy as np

# =========================
# 1. تحميل نماذج القرى
# =========================
models = []

for village_id in [0]:  # يمكن إضافة 1,2,3 لاحقًا
    model = joblib.load(f"edge/models/ae_village_{village_id}.pkl")
    models.append(model)

# =========================
# 2. FedAvg (متوسط الأوزان)
# =========================
avg_weights = []

for layer in range(len(models[0].coefs_)):
    layer_weights = np.mean(
        [model.coefs_[layer] for model in models],
        axis=0
    )
    avg_weights.append(layer_weights)

# =========================
# 3. إنشاء النموذج العالمي
# =========================
global_model = models[0]
global_model.coefs_ = avg_weights

# =========================
# 4. حفظ النموذج العالمي
# =========================
joblib.dump(global_model, "cloud/global_model.pkl")

print("✔ Global model created using FedAvg")
