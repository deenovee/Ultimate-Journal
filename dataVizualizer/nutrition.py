from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
from wordcloud import WordCloud
import re
import base64
from io import BytesIO
from PIL import Image
import numpy as np
import tkinter as tk

app = Dash(__name__)

class Nutrition:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["MyDashboard"]
        self.collection = self.db["nutrition"]
        self.df = pd.DataFrame(self.collection.find())
        self.categories = ["SMALL MEAL", "LARGE MEAL", "SNACK", "DESSERT", "DRINK"]
        self.time_frame = [1, 7, 30, 90, 180, 365, 1000000]
        self.screen_width = self.get_screen_width()

    def get_screen_width(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        return screen_width

    def get(self, query, projection=None):
        try:
            return self.collection.find(query, projection)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def layout(self):
            return html.Div(children=[
                html.H1(children='Nutrition',
                        style={'textAlign': 'center', 'color': 'rgba(255, 255, 255, 0.9)', 'margin': '20px', 'fontSize': '50px'}
                        ),

                html.Div([
                    dcc.Slider(
                        id="slct_year",
                        min=1,
                        max=7,
                        step=1,
                        marks={1: {'label': '1', 'style': {'font-size': '25px'}},
                            2: {'label': '7', 'style': {'font-size': '25px'}},
                            3: {'label': '30', 'style': {'font-size': '25px'}},
                            4: {'label': '90', 'style': {'font-size': '25px'}},
                            5: {'label': '180', 'style': {'font-size': '25px'}},
                            6: {'label': '365', 'style': {'font-size': '25px'}},
                            7: {'label': 'ALL', 'style': {'font-size': '25px'}}
                            },
                        value=3
                    )
                ], style={'width': '90%', 'height': '50px', 'margin': 'auto'}),

                html.Div([
                    dcc.Graph(
                        id='Daily Activity Bar Graph',
                        style={'width': '100%', 'float': 'left', 'margin': '0', 'color': 'rgba(255, 255, 255, 0.9)'}
                    )])
                ])


    def update_graph(self, option_slctd):
        container = "The time frame chosen by user was: {}".format(option_slctd)

        days = self.time_frame[option_slctd-1]
        if option_slctd == 7:
            query = {}
        else:
            query = {"date": {"$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)}}

        projection = {"_id": 0}
        df = pd.DataFrame(self.get(query, projection))
        water = df["water"]
        water = water.dropna()
        avg_water_intake = water.mean()

        fig1 = px.bar(df, x="date", y="water", color='water', title="Water Intake Per Day", color_continuous_scale=px.colors.sequential.Turbo)

        fig1.add_shape(
            type='line',
            x0=df['date'].min(),
            x1=df['date'].max(),
            y0=avg_water_intake,
            y1=avg_water_intake,
            line=dict(color='red', width=2, dash='dash'),
            name='Average Intake'
        )

        fig1.update_layout(
        plot_bgcolor='rgba(30, 30, 30, 0.4)',
        paper_bgcolor='rgba(30, 30, 30, 0.4)',
        font_color='rgba(255, 255, 255, 0.9)',
        legend_title_text='',
        )

        return fig1


if __name__ == '__main__':
    nutrition = Nutrition()
    app.layout = nutrition.layout()
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css"})

    @app.callback(
        Output(component_id='Daily Activity Bar Graph', component_property='figure'),
        [Input(component_id='slct_year', component_property='value')]
    )
    def callback_update_graph(option_slctd):
        return nutrition.update_graph(option_slctd)
    app.run_server(debug=True)