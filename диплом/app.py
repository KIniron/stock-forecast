import dash
from dash import html, dcc
from datetime import datetime as dt
import yfinance as yf
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
from model import prediction
from model1 import prediction1
from deep_translator import GoogleTranslator

# Функція для створення свічкового графіку на основі даних про ціни акцій
def get_stock_price_fig(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'])])
    fig.update_layout(title="Ціни акцій відкритя та закритя",
                      xaxis_title="Дата",
                      yaxis_title="Ціна",
                      xaxis_rangeslider_visible=False)
    return fig

# Функція для створення графіка з додатковими індикаторами
def get_more(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Ціна закриття'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], mode='lines', name='Ціна відкриття'))
    fig.update_layout(title="Додаткові індикатори",
                      xaxis_title="Дата",
                      yaxis_title="Ціна")
    return fig

# Оголошення Dash додатку
app = dash.Dash(
    __name__,
    external_stylesheets=[
        "/assets/style.css"  
    ])
server = app.server

# Оголошення макету сторінки
app.layout = html.Div(
    [
        html.Div(
            [
                html.Nav([
                    html.A("Увійти", href="http://localhost:511/диплом/interface/log.php", className="login-button"),
                    html.A("Зареєструватись", href="http://localhost:511/диплом/interface/reg.php", className="reg-button"),
                    html.A("Прогнозування", href=""),
                    html.A("Зворотній звязок", href="http://localhost:511/диплом/interface/cont.php"),
                    html.A("Головна",href="http://localhost:511/диплом/interface/intro.php")
                ], className="navbar"),
                html.P("", className="start"),
                html.Div([
                    html.P("🔘 Введіть код акції: "),
                    html.Div([
                        dcc.Input(id="dropdown_tickers", type="text"),
                        html.Button("Відправити", id='submit'),
                    ],
                             className="form")
                ],
                         className="input-place"),
                html.Div([
                    dcc.DatePickerRange(id='my-date-picker-range',
                                        min_date_allowed=dt(1995, 8, 5),
                                        max_date_allowed=dt.now(),
                                        initial_visible_month=dt.now(),
                                        end_date=dt.now().date()),
                ],
                         className="date"),
                html.Div([
                    html.Button(
                        "📊 Ціна акцій", className="stock-btn", id="stock"),
                    html.Button("📈📉 Індикатори",
                                className="indicators-btn",
                                id="indicators"),
                    dcc.Input(id="n_days",
                              type="text",
                              placeholder="Введіть кількість днів"),
                    html.Button(
                        "🕵️‍♀️ Прогноз закриття", className="forecast-btn", id="forecast"),
                    html.Button(
                        "🕵️‍♀️ Прогноз відкриття", className="forecast-open-btn", id="forecast_open")
                ],
                         className="buttons"),
            ],
            className="nav"),

        # Вміст
        html.Div(
            [
                html.Div(
                    [  # Хедер
                        html.Img(id="logo"),
                        html.P(id="ticker")
                    ],
                    className="header"),
                html.Div(id="description", className="decription_ticker"),
                html.Div([], id="graphs-content"),
                html.Div([], id="main-content"),
                html.Div([], id="forecast-content"),
                html.Div([], id="forecast-open-content")
            ],
            className="content"),
    ],
    className="container")

# Callback для оновлення інформації про компанію
@app.callback([
    Output("description", "children"),
    Output("logo", "src"),
    Output("ticker", "children"),
    Output("stock", "n_clicks"),
    Output("indicators", "n_clicks"),
    Output("forecast", "n_clicks"),
    Output("forecast_open", "n_clicks")
], [Input("submit", "n_clicks")], [State("dropdown_tickers", "value")])
def update_data(n, val):
    if n is None:
        return ("", 
                "https://usp-ltd.org/wp-content/uploads/2022/01/kak_nahodit_akcii_dlya_vnutridnevnoy_torgovli._rabota_s_filtrami_finviz._chast_4.jpg", 
                "Прогноз і візуалізатор акцій", None, None, None, None)
    if val is None:
        raise PreventUpdate
    else:
        ticker = yf.Ticker(val)
        inf = ticker.info
        df = pd.DataFrame().from_dict(inf, orient="index").T
        
        # Витягнути тексти з датафрейму
        long_business_summary = df['longBusinessSummary'].values[0]
        logo_url = df['logo_url'].values[0] if 'logo_url' in df.columns else "https://usp-ltd.org/wp-content/uploads/2022/01/kak_nahodit_akcii_dlya_vnutridnevnoy_torgovli._rabota_s_filtrami_finviz._chast_4.jpg"
        short_name = df['shortName'].values[0]
        
        # Переклад тексту на українську за допомогою deep_translator
        translated_summary = GoogleTranslator(source='auto', target='uk').translate(long_business_summary)
        
        return translated_summary, logo_url, short_name, None, None, None, None

# Callback для графіків акцій у вигляді свічок
@app.callback([
    Output("graphs-content", "children"),
], [
    Input("stock", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def stock_price(n, start_date, end_date, val):
    if n is None or val is None:
        raise PreventUpdate
    try:
        df = yf.download(val, start=start_date, end=end_date) if start_date else yf.download(val)
        if df.empty:
            return [html.Div("Немає даних за вказаний період.")]
        df.reset_index(inplace=True)
        fig = get_stock_price_fig(df)
        return [dcc.Graph(figure=fig)]
    except yf.YFInvalidPeriodError as e:
        return [html.Div(f"Помилка: {str(e)}")]

# Callback для індикаторів
@app.callback([Output("main-content", "children")], [
    Input("indicators", "n_clicks"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
], [State("dropdown_tickers", "value")])
def indicators(n, start_date, end_date, val):
    if n is None or val is None:
        raise PreventUpdate
    try:
        df_more = yf.download(val, start=start_date, end=end_date) if start_date else yf.download(val)
        if df_more.empty:
            return [html.Div("Немає даних за вказаний період.")]
        df_more.reset_index(inplace=True)
        fig = get_more(df_more)
        return [dcc.Graph(figure=fig)]
    except yf.YFInvalidPeriodError as e:
        return [html.Div(f"Помилка: {str(e)}")]

# Callback для прогнозу закриття
@app.callback([Output("forecast-content", "children")],
              [Input("forecast", "n_clicks")],
              [State("n_days", "value"),
               State("dropdown_tickers", "value")])
def forecast(n, n_days, val):
    if n is None or val is None or not n_days.isdigit():
        raise PreventUpdate
    try:
        fig = prediction(val, int(n_days) + 1)
        if fig is None:
            return [html.Div("Помилка: Неможливо зробити прогноз.")]
        return [dcc.Graph(figure=fig)]
    except ValueError as e:
        return [html.Div(f"Помилка: {str(e)}")]
    except Exception as e:
        return [html.Div(f"Несподівана помилка: {str(e)}")]

# Callback для прогнозу відкриття
@app.callback([Output("forecast-open-content", "children")],
                            [Input("forecast_open", "n_clicks")],
              [State("n_days", "value"),
               State("dropdown_tickers", "value")])
def forecast_open(n, n_days, val):
    if n is None or val is None or not n_days.isdigit():
        raise PreventUpdate
    try:
        fig = prediction1(val, int(n_days) + 1)
        if fig is None:
            return [html.Div("Помилка: Неможливо зробити прогноз.")]
        return [dcc.Graph(figure=fig)]
    except ValueError as e:
        return [html.Div(f"Помилка: {str(e)}")]
    except Exception as e:
        return [html.Div(f"Несподівана помилка: {str(e)}")]

if __name__ == '__main__':
    app.run_server(port=8050, debug=True)
     
