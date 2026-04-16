import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the dataset
data = pd.read_csv('data.csv')

print("Dataset loaded successfully.")

# separar entrada e saida
X = data.drop("produtividade", axis=1) # tudo que influencia
y = data["produtividade"] # o que queremos prever

# dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# criar o modelo de regressão linear
model = LinearRegression()

# treinar o modelo
model.fit(X_train, y_train)

# avaliacao do modelo
score = model.score(X_test, y_test)
print(f"R² score: {score}")

# fazer previsões
novo_dia = pd.DataFrame([[7, 1, 1, 1, 4]], columns=X.columns)
pred = model.predict(novo_dia)
print(f"Previsão de produtividade para o novo dia: {pred[0]}")
print(model.coef_)