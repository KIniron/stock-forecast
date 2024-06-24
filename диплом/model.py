import yfinance as yf
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.preprocessing import StandardScaler
import plotly.graph_objs as go
from datetime import date, timedelta
from sklearn.svm import SVR
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

def add_seasonality_trend(df):
    n = len(df)
    df['Seasonality'] = 10 * np.cos(2 * np.pi * np.arange(n) / 12)
    df['Trend'] = 0.2 * np.arange(n)
    return df

def add_additional_features(df):
    df['Prev_Close'] = df['Close'].shift(1)
    df['Volume'] = df['Volume'].shift(1)
    df['Prev_Close'] = df['Prev_Close'].bfill()
    df['Volume'] = df['Volume'].bfill()
    return df

def prediction(stock, n_days, prev_features=None):
    df = yf.download(stock, period='1mo')

    if df.empty:
        raise ValueError("Немає даних для обраного періоду.")

    df.reset_index(inplace=True)
    df['Day'] = df.index

    if prev_features:
        df['Prev_Close'] = prev_features

    df = add_seasonality_trend(df)
    df = add_additional_features(df)

    X = df[['Day', 'Prev_Close', 'Seasonality', 'Trend', 'Volume']].values if prev_features else df[['Day', 'Seasonality', 'Trend', 'Volume']].values
    Y = df['Close'].values.reshape(-1, 1)

    if len(X) == 0 or len(Y) == 0:
        raise ValueError("Недостатньо даних для навчання моделі.")

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)

    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    x_train = scaler_x.fit_transform(x_train)
    x_test = scaler_x.transform(x_test)
    y_train = scaler_y.fit_transform(y_train)

    svr = SVR(kernel='rbf')
    rf = RandomForestRegressor()
    gb = GradientBoostingRegressor()

    param_grid = {
        'SVR__C': [0.1, 1, 10],
        'SVR__gamma': [0.01, 0.1],
        'RandomForest__n_estimators': [10, 50],  # Зменшення кількості дерев для уникнення перенавчання
        'GradientBoosting__n_estimators': [10, 50],  # Зменшення кількості ітерацій для уникнення перенавчання
        'RandomForest__max_depth': [3, 5],  # Додавання обмеження на глибину дерев для уникнення перенавчання
        'GradientBoosting__max_depth': [3, 5]  # Додавання обмеження на глибину дерев для уникнення перенавчання
    }

    base_models = [
        ('SVR', svr),
        ('RandomForest', rf),
        ('GradientBoosting', gb)
    ]

    stacking_regressor = StackingRegressor(estimators=base_models, final_estimator=RandomForestRegressor())

    grid = GridSearchCV(estimator=stacking_regressor, param_grid=param_grid, cv=5, n_jobs=-1)
    grid.fit(x_train, y_train.ravel())
    best_model = grid.best_estimator_

    joblib.dump(best_model, 'stacked_model_close_v3.pkl')

    y_pred_train = best_model.predict(x_train)
    y_pred_test = best_model.predict(x_test)

    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)

    y_train_mean = scaler_y.inverse_transform(y_train).mean()
    y_test_mean = scaler_y.inverse_transform(y_test).mean()

    train_mse_percentage = (train_mse / y_train_mean) * 100
    test_mse_percentage = (test_mse / y_test_mean) * 100

    if scaler_y.inverse_transform([[1]])[0][0] == 0:
        train_rmse_percentage = 0
        test_rmse_percentage = 0
    else:
        train_rmse_percentage = (train_rmse / scaler_y.inverse_transform([[1]])[0][0]) * 100
        test_rmse_percentage = (test_rmse / scaler_y.inverse_transform([[1]])[0][0]) * 100

    output_days = [[i + x_test[-1][0], df['Seasonality'].iloc[-1] + i, df['Trend'].iloc[-1] + i, df['Volume'].iloc[-1]] for i in range(1, n_days)]
    if prev_features:
        prev_features.append(df['Close'].iloc[-1])
    else:
        prev_features = [df['Close'].iloc[-1]]

    output_days = scaler_x.transform(output_days)
    predicted_prices = scaler_y.inverse_transform(best_model.predict(output_days).reshape(-1, 1))

    dates = []
    current_date = date.today()
    while len(dates) < n_days - 1:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:
            dates.append(current_date)

    predicted_open = np.roll(predicted_prices, shift=1)
    
    predicted_high = predicted_prices + (np.random.rand(n_days - 1, 1) * 2)
    predicted_low = predicted_prices - (np.random.rand(n_days - 1, 1) * 2)

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Реальні ціни закриття'
        ))

    fig.add_trace(
        go.Candlestick(
            x=dates,
            open=predicted_open.flatten(),
            high=predicted_high.flatten(),
            low=predicted_low.flatten(),
            close=predicted_prices.flatten(),
            name='Прогнозовані ціни закриття',
            increasing_line_color='green',
            decreasing_line_color='red'
        ))

    fig.update_layout(
        title={
            'text': "Прогнозовані ціни закриття на наступні " + str(n_days - 1) + " днів",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, color='darkred')
        },
        xaxis_title="Дата",
        yaxis_title="Ціна закриття",
        xaxis=dict(
            tickformat='%d-%m-%Y',
            tickangle=45,
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=0.5
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            gridwidth=0.5
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    print(f'Точність на навчальних даних: {min(90, 100 - train_rmse_percentage):.2f}%')
    print(f'Похибка на навчальних даних: {train_rmse_percentage:.2f}%')
   

    return fig
