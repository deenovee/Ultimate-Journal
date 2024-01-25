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

class TimeKeeper:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["MyDashboard"]
        self.collection = self.db["exercise"]
        self.df = pd.DataFrame(self.collection.find())
        self.categories = ["HEALTH", "WORK", "PROJECT", "EDUCATION", "READING", "HOBBY", "NETWORKING", "OTHER"]
        self.time_frame = [1, 7, 30, 90, 180, 365, 1000000]
        self.screen_width = self.get_screen_width()

    def get_screen_width(self):
        root = tk.Tk()
        width = root.winfo_screenwidth()
        root.destroy()
        return width

    def get(self, query, projection=None):
        try:
            return self.collection.find(query, projection)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def layout(self):
        return html.Div(children=[
            html.H1(children='Exercise',
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
                dcc.Graph(id='running', figure={})]),
            html.Div([
                dcc.Graph(id='stretching', figure={})]),
            html.Div([
                dcc.Graph(id='circuit', figure={})]),
            html.Div([
                dcc.Graph(id='duration', figure={})])

        ], style={'width': '100%', 'height': '100%', 'backgroundColor': 'rgba(30, 30, 30, 0.9)', 'margin': '0'}, id='main_div')

    def update_graph(self, option_slctd):
        # print(option_slctd)
        # print(type(option_slctd))

        container = "The time frame chosen by the user was: {}".format(option_slctd)

        days = self.time_frame[option_slctd - 1]
        if option_slctd == 7:
            query = {}
        else:
            query = {"date": {"$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)}}
        projection = {"_id": 0}
        df = pd.DataFrame(self.get(query, projection))

        df['date'] = pd.to_datetime(df['date'])

        running_data = df[df['exercise_type'] == 'RUNNING']
        stretching_data = df[df['exercise_type'] == 'STRETCHING']
        circuit_data = df[df['exercise_type'] == 'BODY/LIGHTWEIGHT CIRCUIT']

        fig1 = px.bar(running_data, x=running_data['date'], y='distance', title='Average Distance for Running')
        fig1.update_layout(showlegend=False)

        fig2 = px.bar(stretching_data, x=stretching_data['date'], y='duration', title='Average Distance for Stretching')
        fig2.update_layout(showlegend=False)

        fig3 = px.bar(circuit_data, x=circuit_data['date'], y='duration', title='Duration for Circuit Exercises')
        fig3.update_layout(showlegend=False)

        fig4 = px.bar(df, x=df.index, y='duration', title='Amount of Time Working Out for Each Date')
        fig4.update_layout(showlegend=False)

        return fig1, fig2, fig3, fig4
        


if __name__ == '__main__':
    timeKeeper = TimeKeeper()

    app.layout = timeKeeper.layout()
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css"})


    @app.callback(
        [Output(component_id='running', component_property='figure'), Output(component_id='stretching', component_property='figure'), Output(component_id='circuit', component_property='figure'), Output(component_id='duration', component_property='figure')],
        [Input('slct_year', 'value')])
    def callback_update_graph(option_slctd):
        return timeKeeper.update_graph(option_slctd)

    app.run(debug=True, port=8051)
