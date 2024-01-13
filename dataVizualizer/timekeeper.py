from dash import Dash, html, dcc
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

app = Dash(__name__)

class TimeKeeper:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["MyDashboard"]
        self.collection = self.db["timeKeeper"]

    def get(self, query, projection=None):
        try:
            return self.collection.find(query, projection)
        except pymongo.errors.PyMongoError as e:
            print(f"MongoDB query failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def bar_chart(self, query, categories, projection=None):
        try:
            records = self.collection.find(query, projection)
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df['category'] = pd.Categorical(df['category'], categories=categories, ordered=True)
            print(df['category'])
            daily_time_by_category = df.groupby(['date', 'category'])['time'].sum().reset_index()
            fig = px.bar(daily_time_by_category, 
                         x='date', 
                         y='time', 
                         color='category', 
                         title='Time Spent Per Day',
                         labels={'time': 'minutes'},
                         barmode='stack',
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         category_orders={'category': categories}  
                        )
            return fig
        except Exception as e:
            print(e)
            print("Error displaying data")

    def average_pie_chart(self, query, categories, projection=None):
        try:
            records = self.collection.find(query, projection)
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df['category'] = pd.Categorical(df['category'], categories=categories, ordered=True)
            daily_time_by_category = df.groupby(['date', 'category'])['time'].sum().reset_index()
            
            # Use the specified order of categories for grouping
            average_time_per_day = daily_time_by_category.groupby('category')['time'].mean().reset_index()

            fig = px.pie(average_time_per_day, 
                        names='category', 
                        values='time', 
                        title='Average Time Spent Per Day by Category',
                        labels={'time': 'hours'},
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        category_orders={'category': categories}
                        )
            return fig
        except Exception as e:
            print(e)
            print("Error displaying data")


    def work_line_chart(self, query, projection=None):
        try:
            records = self.collection.find(query, projection)
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df['time'] = df['time'] / 60.0
            daily_work_time = df.groupby('date')['time'].sum().reset_index()
            fig = px.line(daily_work_time, 
                        x='date', 
                        y='time', 
                        title='Time Spent Working Per Day',
                        labels={'time': 'hours'}
                        )
            return fig
        except Exception as e:
            print(e)
            print("Error displaying data")

    def reading_heatmap(self, query, projection=None):
        try:
            records = self.collection.find(query, projection)
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'])
            df['time'] = df['time'] / 60.0
            df['heat_weight'] = (df['time'] - df['time'].min()) / (df['time'].max() - df['time'].min())


            fig = go.Figure(data=go.Heatmap(
                x=df['date'],
                y=df['heat_weight'],
                 z=df['time'],
                colorscale='Viridis',
                colorbar=dict(title='Time (hours)'),
            ))

            fig.update_layout(title='Reading Time Heatmap')
            
            return fig
        except Exception as e:
            print(e)
            print("Error displaying data")

    def word_cloud(self, query, projection=None):
        try:
            records = self.collection.find(query, projection)
            df = pd.DataFrame(records)
            df['description'] = df['description'].apply(lambda x: re.sub(r'\([^)]*\)', '', x))
            text = ' '.join(df['description'])
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            return html.Img(src=wordcloud.to_image())

        except Exception as e:
            print(e)
            print("Error displaying data")


    def layout(self, bar_chart_fig, pie_chart_fig, work_line_chart_fig, reading_heatmap_fig, word_cloud_component):
        return html.Div(children=[
            html.H1(children='Hello Dash'),

            html.Div(children='''
                Dash: A web application framework for your data.
            '''),

            dcc.Graph(
                id='Daily Activity Bar Graph',
                figure=bar_chart_fig
            ),

            dcc.Graph(
                id='Average Activity Pie Chart',
                figure=pie_chart_fig
            ),

            dcc.Graph(
                id='Work Line Chart',
                figure=work_line_chart_fig
            ),

            dcc.Graph(
                id='Reading Heatmap',
                figure=reading_heatmap_fig
            ),

            html.Div(
                id='Word Cloud',
                children=word_cloud_component
            )
        ])


if __name__ == '__main__':
    timeKeeper = TimeKeeper()
    categories = ["HEALTH", "WORK", "PROJECT", "EDUCATION", "READING", "HOBBY", "NETWORKING", "OTHER"]
    query = {"date": {
        "$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=125),
    }, "category": {"$ne": "WORK"}}
    projection = {"_id": 0}

    bar_chart_fig = timeKeeper.bar_chart(query, categories, projection)
    pie_chart_fig = timeKeeper.average_pie_chart(query, categories, projection)

    work_query = {"category": "WORK"}
    work_line_chart_fig = timeKeeper.work_line_chart(work_query, projection)

    reading_query = {"category": "READING"}
    reading_heatmap_fig = timeKeeper.reading_heatmap(reading_query, projection)

    word_cloud_component = timeKeeper.word_cloud(query, projection)

    app.layout = timeKeeper.layout(bar_chart_fig, pie_chart_fig, work_line_chart_fig, reading_heatmap_fig, word_cloud_component)
    app.run(debug=True)

