import unittest
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash.testing.application_runners import import_app
import yfinance as yf
import pandas as pd
from app import app, update_data, stock_price, indicators, forecast, forecast_open

class TestStockApp(unittest.TestCase):

    def test_update_data_no_click(self):
        output = update_data(None, None)
        self.assertEqual(
            output,
            ("", "https://usp-ltd.org/wp-content/uploads/2022/01/kak_nahodit_akcii_dlya_vnutridnevnoy_torgovli._rabota_s_filtrami_finviz._chast_4.jpg", "Прогноз і візуалізатор акцій", None, None, None, None)
        )

    def test_update_data_no_value(self):
        with self.assertRaises(PreventUpdate):
            update_data(1, None)

    def test_stock_price_no_click(self):
        with self.assertRaises(PreventUpdate):
            stock_price(None, None, None, None)

    def test_stock_price_no_value(self):
        with self.assertRaises(PreventUpdate):
            stock_price(1, None, None, None)

    def test_indicators_no_click(self):
        with self.assertRaises(PreventUpdate):
            indicators(None, None, None, None)

    def test_indicators_no_value(self):
        with self.assertRaises(PreventUpdate):
            indicators(1, None, None, None)

    def test_forecast_no_click(self):
        with self.assertRaises(PreventUpdate):
            forecast(None, None, None)

    def test_forecast_no_value(self):
        with self.assertRaises(PreventUpdate):
            forecast(1, None, None)

    def test_forecast_open_no_click(self):
        with self.assertRaises(PreventUpdate):
            forecast_open(None, None, None)

    def test_forecast_open_no_value(self):
        with self.assertRaises(PreventUpdate):
            forecast_open(1, None, None)

if __name__ == '__main__':
    unittest.main()
