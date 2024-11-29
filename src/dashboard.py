# File: stock_dashboard/dashboard.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .data_fetcher import StockDataFetcher
from .technical_analysis import TechnicalAnalyzer
from .config import THEME, COLORS, DEFAULT_TICKER

class StockDashboard:
    def __init__(self):
        self.app = dash.Dash(__name__, title='Stock Analysis Dashboard')
        self.data_fetcher = StockDataFetcher()
        self.tech_analyzer = TechnicalAnalyzer()
        self.setup_layout()
        self.setup_callbacks()
    
    def setup_layout(self):
        self.app.layout = html.Div([
            html.Div([
                html.H1("Interactive Stock Analysis Dashboard",
                        style={'color': COLORS['text']}),
                html.Div([
                    dcc.Input(
                        id='ticker-input',
                        value=DEFAULT_TICKER,
                        type='text',
                        placeholder='Enter stock ticker...',
                        style={'margin': '10px'}
                    ),
                    dcc.Dropdown(
                        id='timeframe-dropdown',
                        options=[
                            {'label': '1 Month', 'value': '1mo'},
                            {'label': '3 Months', 'value': '3mo'},
                            {'label': '6 Months', 'value': '6mo'},
                            {'label': '1 Year', 'value': '1y'},
                            {'label': '5 Years', 'value': '5y'}
                        ],
                        value='1y',
                        style={'width': '200px', 'margin': '10px'}
                    ),
                    html.Button('Update', id='update-button', n_clicks=0)
                ]),
            ], style={'padding': '20px', 'background-color': COLORS['background']}),
            html.Div([
                dcc.Loading(
                    id="loading-1",
                    children=[
                        dcc.Graph(id='price-chart'),
                        dcc.Graph(id='technical-chart'),
                        dcc.Graph(id='volume-chart')
                    ],
                    type="circle",
                )
            ], style={'padding': '20px'})
        ])
    
    def setup_callbacks(self):
        @self.app.callback(
            [Output('price-chart', 'figure'),
             Output('technical-chart', 'figure'),
             Output('volume-chart', 'figure')],
            [Input('update-button', 'n_clicks')],
            [State('ticker-input', 'value'),
             State('timeframe-dropdown', 'value')]
        )
        def update_charts(n_clicks, ticker, timeframe):
            try:
                df = self.data_fetcher.get_stock_data(ticker, timeframe)
                
                # use TechnicalAnalyzer for all calculations
                df = self.tech_analyzer.add_moving_averages(df)
                df = self.tech_analyzer.add_bollinger_bands(df)
                df = self.tech_analyzer.add_rsi(df)
                
                # create price chart
                price_fig = go.Figure()
                price_fig.add_trace(go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name='Price'
                ))
                
                # add SMAs
                sma_periods = [20, 50, 200]
                for period in sma_periods:
                    price_fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df[f'SMA_{period}'],
                        name=f'{period}-day SMA',
                        line=dict(width=1)
                    ))
                
                price_fig.update_layout(
                    title=f'{ticker} Stock Price',
                    template=THEME,
                    height=600
                )
                
                # create technical indicators chart
                tech_fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
                tech_fig.add_trace(
                    go.Scatter(x=df.index, y=df['RSI'], name='RSI'),
                    row=1, col=1
                )
                
                tech_fig.add_trace(
                    go.Scatter(x=df.index, y=df['BB_upper'], name='BB Upper'),
                    row=2, col=1
                )
                tech_fig.add_trace(
                    go.Scatter(x=df.index, y=df['BB_middle'], name='BB Middle'),
                    row=2, col=1
                )
                tech_fig.add_trace(
                    go.Scatter(x=df.index, y=df['BB_lower'], name='BB Lower'),
                    row=2, col=1
                )
                
                tech_fig.update_layout(
                    title='Technical Indicators',
                    template=THEME,
                    height=600
                )
                
                # create volume chart
                volume_fig = go.Figure()
                volume_fig.add_trace(go.Bar(
                    x=df.index,
                    y=df['Volume'],
                    name='Volume'
                ))
                
                volume_fig.update_layout(
                    title='Trading Volume',
                    template=THEME,
                    height=400
                )
                
                return price_fig, tech_fig, volume_fig
                
            except Exception as e:
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    title=f'Error: {str(e)}',
                    template=THEME
                )
                return empty_fig, empty_fig, empty_fig
    
    def run(self, debug=True):
        self.app.run_server(debug=debug)