import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# Cargar el archivo CSV
file_path = r"C:\Users\luisf\Desktop\project1\AUD_CLP_Historical_Data.csv"
data = pd.read_csv(file_path)

# Convertir la columna Date a tipo datetime
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')

# Ordenar los datos por fecha
data = data.sort_values(by='Date')

# Extraer la columna Price y resetear el índice
prices = data[['Date', 'Price']].reset_index(drop=True)

# Crear características (X) y etiquetas (y)
prices['Price'] = prices['Price'].astype(float)
X = np.arange(len(prices)).reshape(-1, 1)  # Usar el índice del día como característica
y = prices['Price'].values  # Usar los precios como etiquetas

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Crear y entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Hacer predicciones
y_pred = model.predict(X_test)

# Mostrar los resultados
plt.figure(figsize=(10, 6))
plt.plot(prices['Date'], prices['Price'], label='Precio Real')
plt.plot(prices['Date'].iloc[len(X_train):], y_pred, label='Predicción', linestyle='--')
plt.xlabel('Fecha')
plt.ylabel('Precio AUD/CLP')
plt.legend()
plt.show()

# Extender el rango de fechas para la proyección
future_days = 30  # Número de días a proyectar en el futuro
last_index = len(prices)
future_indices = np.arange(last_index, last_index + future_days).reshape(-1, 1)

# Predecir los precios futuros
future_predictions = model.predict(future_indices)

# Crear un DataFrame con las fechas futuras y las predicciones
future_dates = pd.date_range(start=prices['Date'].iloc[-1] + pd.Timedelta(days=1), periods=future_days)
future_prices = pd.DataFrame({'Date': future_dates, 'Price': future_predictions})

# Mostrar los resultados
plt.figure(figsize=(10, 6))
plt.plot(prices['Date'], prices['Price'], label='Precio Real')
plt.plot(prices['Date'].iloc[len(X_train):], y_pred, label='Predicción', linestyle='--')
plt.plot(future_prices['Date'], future_prices['Price'], label='Proyección Futura', linestyle='--')
plt.xlabel('Fecha')
plt.ylabel('Precio AUD/CLP')
plt.legend()
plt.show()
