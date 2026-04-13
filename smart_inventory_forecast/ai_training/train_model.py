import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score


# 1. LOAD DATA
print("🔄 Đang load dữ liệu...")

df = pd.read_csv("dataset_banh_mi.csv")

# 2. FEATURE ENGINEERING
# Tạo cột weekday, month (nếu chưa có)
df['Ngày'] = pd.to_datetime(df['Ngày'])
df['weekday'] = df['Ngày'].dt.weekday
df['month'] = df['Ngày'].dt.month

# Cuối tuần (Chủ nhật = 6)
df['is_weekend'] = df['weekday'].apply(lambda x: 1 if x == 6 else 0)

# 3. TẠO LABEL (A/B/C)

# Tổng số lượng bán theo ngày
daily_sales = df.groupby('Ngày')['Số_Lượng_Bán'].sum().reset_index()

# Xác định ngưỡng
low_threshold = daily_sales['Số_Lượng_Bán'].quantile(0.33)
high_threshold = daily_sales['Số_Lượng_Bán'].quantile(0.66)

def classify_demand(qty):
    if qty <= low_threshold:
        return 'Nhom_A'
    elif qty <= high_threshold:
        return 'Nhom_B'
    else:
        return 'Nhom_C'

daily_sales['label'] = daily_sales['Số_Lượng_Bán'].apply(classify_demand)

# Merge lại với feature
df_model = daily_sales.copy()
df_model['weekday'] = pd.to_datetime(df_model['Ngày']).dt.weekday
df_model['month'] = pd.to_datetime(df_model['Ngày']).dt.month
df_model['is_weekend'] = df_model['weekday'].apply(lambda x: 1 if x == 6 else 0)

# 4. CHUẨN BỊ DATA

X = df_model[['weekday', 'month', 'is_weekend']]
y = df_model['label']

# Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. TRAIN MODEL

print("🤖 Đang train model...")

model = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=5,           # tránh overfitting
    random_state=42
)

model.fit(X_train, y_train)

# 6. EVALUATE

y_pred = model.predict(X_test)

print("\n📊 Kết quả đánh giá:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 7. SAVE MODEL

joblib.dump(model, "ai_model_universal.pkl")

print("\nĐã lưu model: ai_model_universal.pkl")