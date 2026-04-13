import pandas as pd
import random
from datetime import datetime, timedelta

# ===== CONFIG =====
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)

data = []

current_date = start_date

while current_date <= end_date:
    weekday = current_date.weekday()  # 0 = T2
    month = current_date.month
    year = current_date.year

    is_weekend = 1 if weekday == 6 else 0  # CN

    # BASE DEMAND
    if is_weekend:
        bread = 140
        xoi = 150
    else:
        bread = 200
        xoi = 200

    # SEASON EFFECT
    if month in [3, 9]:
        factor = 1.2
    elif month in [2, 8]:
        factor = 0.5
    else:
        factor = 1.0

    bread = int(bread * factor)
    xoi = int(xoi * factor)

    # RANDOM NOISE
    bread += random.randint(-10, 10)
    xoi += random.randint(-10, 10)

    bread = max(bread, 50)
    xoi = max(xoi, 50)

    # DEMAND CLASS
    if bread < 150:
        demand = "Nhom_A"
    elif bread < 220:
        demand = "Nhom_B"
    else:
        demand = "Nhom_C"

    data.append([
        current_date.strftime("%Y-%m-%d"),
        weekday,
        month,
        year,
        is_weekend,
        bread,
        xoi,
        demand
    ])

    current_date += timedelta(days=1)


# SAVE
df = pd.DataFrame(data, columns=[
    "date", "weekday", "month", "year",
    "is_weekend", "total_bread", "total_xoi", "demand_class"
])

df.to_csv("dataset_3_years.csv", index=False)

print("Dataset 3 năm đã tạo xong!")