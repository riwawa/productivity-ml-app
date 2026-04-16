import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from db import init_db, save_data, load_data, safe_migrate, seed_data

# =========================
# CONFIG
# =========================
feature_order = ["sleep", "study", "exercise", "caffeine", "humor"]

# =========================
# INIT DB
# =========================
init_db()
safe_migrate()
seed_data();

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# SAFE CHECK
# =========================
if df.empty or len(df) < 2:
    st.warning("Not enough data to train the model. Please add more entries.")
    st.stop()

# =========================
# TRAIN MODEL
# =========================
X = df[feature_order]
y = df["productivity"]

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# =========================
# UI
# =========================
st.title("Productivity App")

tab1, tab2 = st.tabs(["> Predict", "> Dashboard"])

# =========================
# TAB 1 - PREDICT
# =========================
with tab1:
    st.subheader("Predict your productivity")

    name = st.text_input("Name")

    sleep_hours = st.slider("Sleep hours", 0, 12, 7)
    study = st.selectbox("Did you study?", ["No", "Yes"])
    exercise = st.selectbox("Did you exercise?", ["No", "Yes"])
    caffeine = st.slider("Caffeine (0/1)", 0, 1, 1)
    humor = st.slider("Humor (1-5)", 1, 5, 3)
    prod_real = st.slider("Real productivity", 0, 10, 5)

    study_val = 1 if study == "Yes" else 0
    exercise_val = 1 if exercise == "Yes" else 0

    if st.button("Predict"):
        novo_dia = pd.DataFrame(
            [[sleep_hours, study_val, exercise_val, caffeine, humor]],
            columns=feature_order
        )

        pred = model.predict(novo_dia)[0]

        st.subheader(f"Predicted productivity: {pred:.2f}")

        if name:
            st.write(f"{name}, this is your expected productivity today.")

    if st.button("Save data"):
        save_data(
            sleep_hours,
            study_val,
            exercise_val,
            caffeine,
            humor,
            prod_real
        )

        st.success("Saved to database")
        st.rerun()

# =========================
# TAB 2 - DASHBOARD
# =========================
with tab2:
    st.subheader("Productivity over time")

    if not df.empty:
        st.line_chart(df["productivity"])

        st.subheader("Stats")
        st.write("Average:", df["productivity"].mean())
        st.write("Max:", df["productivity"].max())
        st.write("Min:", df["productivity"].min())

        st.subheader("Insights")
        corr = df.corr(numeric_only=True)["productivity"].sort_values(ascending=False)
        st.write("📊 Correlation with productivity:")
        st.write(corr)

    else:
        st.info("No data to display yet.")