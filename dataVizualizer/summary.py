from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
import pymongo
from pymongo import MongoClient
import datetime
from datetime import timedelta
import tkinter as tk
import dash

app = Dash(__name__)

class Journal:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["MyDashboard"]
        self.collection = self.db["journal"]
        self.df = pd.DataFrame(self.collection.find())
        self.time_frame = [1, 7, 30, 90, 180, 365, 1000000]
        self.screen_width = self.get_screen_width()
        self.current_entry_index = 0

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
            html.H1(children='Journal',
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
                    id='Daily Rating Bar Graph',
                    style={'width': '100%', 'float': 'left', 'margin': '0', 'color': 'rgba(255, 255, 255, 0.9)'}
                )
            ]),
            html.Div(children=[
                html.Div(id='journal-text', style={'textAlign': 'center', 'color': 'rgba(255, 255, 255, 0.9)', 'margin': '20px', 'fontSize': '20px'}),
                html.Button('previous', id='prev-button', n_clicks=0, style={'width': '50%', 'height': '50px', 'margin': 'auto'}),
                html.Button('next', id='next-button', n_clicks=0, style={'width': '50%', 'height': '50px', 'margin': 'auto'}),
            ])
            ], style={'width': '100%', 'height': '100%', 'backgroundColor': 'rgba(30, 30, 30, 0.9)', 'margin': '0'}, id='main_div')

    def update_graph(self, option_slctd):
        container = "The time frame chosen by the user was: {}".format(option_slctd)

        days = self.time_frame[option_slctd-1]
        if option_slctd == 7:
            query = {}
        else:
            query = {"date": {"$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)}}

        projection = {"_id": 0}
        df = pd.DataFrame(self.get(query, projection))
        avg_rating = df.groupby('date')['rating'].mean().reset_index()

        color = px.colors.sequential.Turbo[3]

        fig = px.bar(avg_rating, x="date", y="rating", title="Average Rating Per Day", color_discrete_sequence=[color])

        fig.update_layout(
            plot_bgcolor='rgba(30, 30, 30, 0.9)',
            paper_bgcolor='rgba(30, 30, 30, 0.9)',
            font_color='rgba(255, 255, 255, 0.9)',
            legend_title_text='',
        )

        return fig

    def update_journal_text(self, option_slctd):
        # Get the currently displayed journal entry index
        current_index = self.current_entry_index
        days = self.time_frame[option_slctd-1]
        if option_slctd == 7:
            query = {}
        elif option_slctd == 1:
            query = {"date": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)}
        else:
            query = {"date": {"$gte": datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)}}

        projection = {"_id": 0}
        df = pd.DataFrame(self.get(query, projection))

        # If there are entries, display the journal text for the current entry index
        if not df.empty:
            current_journal_text = df.iloc[current_index]['journal']
            return current_journal_text
        else:
            return "No entries found"


if __name__ == '__main__':
    journal = Journal()
    app.layout = journal.layout()
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css"})

    @app.callback(
        Output(component_id='Daily Rating Bar Graph', component_property='figure'),
        [Input(component_id='slct_year', component_property='value')]
    )
    def callback_update_graph(option_slctd):
        return journal.update_graph(option_slctd)

    @app.callback(
        [Output(component_id='journal-text', component_property='children'),
        Output(component_id='prev-button', component_property='n_clicks'),
        Output(component_id='next-button', component_property='n_clicks')],
        [Input(component_id='slct_year', component_property='value'),
        Input(component_id='prev-button', component_property='n_clicks'),
        Input(component_id='next-button', component_property='n_clicks')]
    )
    def callback_update_journal_text(option_slctd, prev_clicks, next_clicks):
        # Update the current entry index based on button clicks
        ctx = dash.callback_context

        if ctx.triggered_id == 'prev-button' and prev_clicks > 0:
            journal.current_entry_index = max(0, journal.current_entry_index - 1)
        elif ctx.triggered_id == 'next-button' and next_clicks > 0:
            journal.current_entry_index = min(len(journal.df) - 1, journal.current_entry_index + 1)

        return journal.update_journal_text(option_slctd), 0, 0



    app.run_server(debug=True, port=8051)
