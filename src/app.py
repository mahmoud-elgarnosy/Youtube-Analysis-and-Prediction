# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
from  dash import  dcc,html
import plotly.express as px
from pytz import country_names
from  plots import plots

# Multi-dropdown options
from controls import COUNTIES, WELL_STATUSES, WELL_TYPES, WELL_COLORS

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


plotts = plots()
category_names = plotts.get_category_names()
country_names = plotts.get_country_name()


# Create controls
county_options = [
    {"label": str(COUNTIES[county]), "value": str(county)} for county in COUNTIES
]

category_name = [
    {"label": str(category), "value": str(category)}
    for category in category_names
]

country_name = [
    {"label": str(country), "value": str(country)}
    for country in country_names
]


# Load data
df = pd.read_csv(DATA_PATH.joinpath("wellspublic.csv"), low_memory=False)
df["Date_Well_Completed"] = pd.to_datetime(df["Date_Well_Completed"])
df = df[df["Date_Well_Completed"] > dt.datetime(1960, 1, 1)]

trim = df[["API_WellNo", "Well_Type", "Well_Name"]]
trim.index = trim["API_WellNo"]
dataset = trim.to_dict(orient="index")

points = pickle.load(open(DATA_PATH.joinpath("points.pkl"), "rb"))


# Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)
# df2 = pd.read_csv('../data/processed/df_duration_prepared.csv',index_col=0)



# category_views_plot = plotts.category_views(['Travel & Events','Sports'])
# days_views_plot = plotts.days_views(['Sports'],['US'])
# views_country_plot = plotts.views_country(country_names[:4])
# Views_vs_VideoLength_plot = plotts.Views_vs_VideoLength(category_names[:3],country_names[:2])

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        # html.Div(
        #             [
        #                 html.H2("WIND SPEED STREAMING", className="app__header__title"),
        #                 html.P(
        #                     "This app continually queries a SQL database and displays live charts of wind speed and wind direction.",
        #                     className="app__header__title--grey",
        #                 ),
        #             ],
        #             className="app__header__desc",
        #         ),
        html.Div(
            [
                html.Div(
                    [

                        html.H2("Youtube Trending Statistics", className="app__header__title",style = {"text-align": "center"}),
                        html.P(
                            "This app Summarize our finding in 2017-2018 Youtube Trending in several Countries",
                            className="app__header__title--grey",
                        ),

                        html.H3(
                            "Countrol Panal",
                            className="control_label",
                            style = {"text-align": "center"}
                        ),
                        
                        # html.P("Filter Countries Views on each Category", className="control_label"),
                        # dcc.Slider(0,14,None, marks={i: str(c) for i,c in enumerate(category_names)} ,value=0,id='my_slider'),


                        html.P("Filter by Categories:", className="control_label"),
                        dcc.RadioItems(
                            id="well_status_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Music", "value": "Music"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="Music",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                            
                        ),

                        
                        dcc.Dropdown(
                            id="well_statuses",
                            options=category_name,
                            multi=True,
                            value=category_names,
                            className="dcc_control",
                            style = {"color": "#fff","background_color":"#151515"}
                        ),
                        
                        html.P("Filter by well type:", className="control_label"),
                        dcc.RadioItems(
                            id="well_type_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "US", "value": "US"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="US",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="well_types",
                            options=country_name,
                            multi=True,
                            value=country_names,
                            className="dcc_control",
                        ),
                    ],
                    className="four.columns control__panal",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="well_text"), html.P("No. of Wells")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="gasText"), html.P("Gas")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="oilText"), html.P("Oil")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="waterText"), html.P("Water")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                        [dcc.Graph(id="category_views_plot")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="ten columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="days_views_plot")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="views_country_plot")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="most_trending_videos")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="Views_vs_VideoLength_plot")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)




# Radio -> multi
@app.callback(
    Output("well_statuses", "value"), [Input("well_status_selector", "value")]
)
def display_status(selector):
    if selector == "all":
        return list(category_names)
    else:
        return ["Music"]
    # return []


# Radio -> multi
@app.callback(Output("well_types", "value"), [Input("well_type_selector", "value")])
def display_type(selector):
    if selector == "all":
        return country_names
    else :
        return ["US"]
    # return ['US']


@app.callback(
    Output(component_id='category_views_plot',component_property='figure'),
    Output(component_id='days_views_plot',component_property='figure'),

    Output(component_id='views_country_plot',component_property='figure'),

    Output(component_id='most_trending_videos',component_property='figure'),
    Output(component_id='Views_vs_VideoLength_plot',component_property='figure'),


    Input(component_id='well_statuses',component_property='value'),
    Input(component_id='well_types',component_property='value'),

)
def update_graph(categories,countries):
    category_views_plot = plotts.category_views(categories,countries)
    days_views_plot = plotts.days_views(categories,countries)
    most_trending_videos = plotts.most_trending_videos(categories,countries)
    views_country_plot = plotts.views_country(countries)
    Views_vs_VideoLength_plot = plotts.Views_vs_VideoLength(categories,countries)

    
    return category_views_plot,days_views_plot,views_country_plot,most_trending_videos,Views_vs_VideoLength_plot


# @app.callback(
#     # Output(component_id='category_views_plot',component_property='figure'),
#     # Output(component_id='days_views_plot',component_property='figure'),

#     # Output(component_id='Views_vs_VideoLength_plot',component_property='figure'),
#     Output(component_id='views_country_plot',component_property='figure'),
#     # Output(component_id='Views_vs_VideoLength_plot2',component_property='figure'),


#     # Input(component_id='well_statuses',component_property='value'),
#     Input(component_id='well_types',component_property='value'),
#     Input(component_id='my_slider',component_property='value'),


# )
def update_graph2(countries,categorie):

    print([category_names[categorie]])
    
    views_country_plot = plotts.views_country(countries,[category_names[categorie]])

    
    return views_country_plot

# my_slider

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
