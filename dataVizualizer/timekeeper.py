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
        self.collection = self.db["timeKeeper"]
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
            html.H1(children='Time Keeper',
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
                    style={'width': '70%', 'float': 'left', 'margin': '0', 'color': 'rgba(255, 255, 255, 0.9)'}
                ),
                dcc.Graph(
                    id='Average Activity Pie Chart',
                    style={'width': '30%', 'float': 'right', 'margin': '0', 'color': 'rgba(255, 255, 255, 0.9)'}
                )
            ], style={'width': '100%', 'display': 'flex', 'flexWrap': 'wrap'}),

            html.Div(id='word_cloud', children=[], style={'width': '100%', 'height': '100%', 'margin': 'auto', 'textAlign': 'center'})

        ], style={'width': '100%', 'height': '100%', 'backgroundColor': 'rgba(30, 30, 30, 0.9)', 'margin': '0'}, id='main_div')

    def update_graph(self, option_slctd):
        # print(option_slctd)
        # print(type(option_slctd))

        container = "The time frame chosen by user was: {}".format(option_slctd)

        days = self.time_frame[option_slctd - 1]
        if option_slctd == 7:
            query = {}
        else:
            query = {"date": {"$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)}}
        projection = {"_id": 0}
        df = pd.DataFrame(self.get(query, projection))
        # print(df)
        df['date'] = pd.to_datetime(df['date'])
        df['category'] = pd.Categorical(df['category'], categories=self.categories, ordered=True)
        daily_time_by_category = df.groupby(['date', 'category'])['time'].sum().reset_index()
        average_time_per_day = daily_time_by_category.groupby('category')['time'].mean().reset_index()
        df['description'] = df['description'].apply(lambda x: re.sub(r'\([^)]*\)', '', x))
        text = ' '.join(df['description'])
        wordcloud = WordCloud(width=self.screen_width, height=400, background_color=None, mode='RGBA').generate(text)

        background_color = (30, 30, 30, 204)
        background = Image.new("RGBA", (self.screen_width, 400), background_color)

        wordcloud_rgba = wordcloud.to_image()
        combined_image = Image.alpha_composite(background.convert("RGBA"), wordcloud_rgba)

        img_buf = BytesIO()
        combined_image.save(img_buf, format='PNG')
        img_str = "data:image/png;base64," + base64.b64encode(img_buf.getvalue()).decode()

        fig1 = px.bar(daily_time_by_category,
                      x='date',
                      y='time',
                      color='category',
                      title='Time Spent Per Day',
                      labels={'time': 'minutes'},
                      barmode='stack',
                      color_discrete_sequence=px.colors.sequential.Turbo,
                      category_orders={'category': self.categories}
                      )

        fig2 = px.pie(average_time_per_day,
                      names='category',
                      values='time',
                      title='Average Time Spent Per Day by Category',
                      labels={'time': 'minutes'},
                      color_discrete_sequence=px.colors.sequential.Turbo,
                      category_orders={'category': self.categories}
                      )



        fig1.update_layout(
        plot_bgcolor='rgba(30, 30, 30, 0.4)',
        paper_bgcolor='rgba(30, 30, 30, 0.4)',
        font_color='rgba(255, 255, 255, 0.9)',
        legend_title_text='',
        )
        fig2.update_layout(
        plot_bgcolor='rgba(30, 30, 30, 0.4)',
        paper_bgcolor='rgba(30, 30, 30, 0.4)',
        font_color='rgba(255, 255, 255, 0.9)',
        showlegend=False
        )

        return fig1, fig2, html.Img(src=img_str)


if __name__ == '__main__':
    timeKeeper = TimeKeeper()

    app.layout = timeKeeper.layout()
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css"})


    @app.callback(
        [Output('Daily Activity Bar Graph', 'figure'), Output('Average Activity Pie Chart', 'figure'), Output('word_cloud', 'children')],
        [Input('slct_year', 'value')])
    def callback_update_graph(option_slctd):
        return timeKeeper.update_graph(option_slctd)

    app.run(debug=True, port=8050)
