import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

from db import init_db, save_data, load_data

# =========================
# INIT DB
# =========================
init_db()

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# TRAIN MODEL
# =========================
X = df.drop(["id", "productivity"], axis=1)
y = df["productivity"]

model = LinearRegression()
model.fit(X, y)

# =========================
# UI
# =========================
st.title("📊 Productivity Analysis")

name = st.text_input("Name")

sleep_hours = st.slider("Sleep hours", 0, 12, 7)
study = st.selectbox("Did you study?", ["No", "Yes"])
exercise = st.selectbox("Did you exercise?", ["No", "Yes"])
caffeine = st.slider("Caffeine (0/1)", 0, 1, 1)
humor = st.slider("Humor (1-5)", 1, 5, 3)

prod_real = st.slider("Real productivity", 0, 10, 5)

# =========================
# CONVERT DATA
# =========================
study = 1 if study == "Yes" else 0
exercise = 1 if exercise == "Yes" else 0

# =========================
# PREDICTION
# =========================
if st.button("Predict"):
    novo_dia = pd.DataFrame(
        [[sleep_hours, study, exercise, caffeine, humor]],
        columns=X.columns
    )

    pred = model.predict(novo_dia)[0]

    st.subheader(f"🔮 Predicted productivity: {pred:.2f}")

    if name:
        st.write(f"{name}, this is your expected productivity today.")

# =========================
# SAVE DATA
# =========================
if st.button("Save today data"):
    save_data(sleep_hours, study, exercise, caffeine, humor, prod_real)
    st.success("Saved to database")

    # atualizar dados após salvar
    df = load_data()

# =========================
# DASHBOARD
# =========================
st.title("📊 Dashboard")

st.line_chart(df["productivity"])

st.subheader("Stats")
st.write("Average:", df["productivity"].mean())
st.write("Max:", df["productivity"].max())
st.write("Min:", df["productivity"].min())

st.subheader("Insights")

if df["exercise"].mean() > 0.5:
    st.write("Exercise habit is strong")

if df["study"].mean() > 0.5:
    st.write("Study habit is strong")

st.subheader("Correlations")
st.write(df.corr(numeric_only=True)["productivity"])