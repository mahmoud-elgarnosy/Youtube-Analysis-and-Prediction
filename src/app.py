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
from  plots import plots

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

category_name = [
    {"label": str(category), "value": str(category)}
    for category in category_names
]

country_name = [
    {"label": str(country), "value": str(country)}
    for country in country_names
]



# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        html.Div(id="output-clientside"),
        
        html.Div(
            [
                html.Div(
                    [

                        html.H2("Youtube Trending Statistics", className="app__header__title",style = {"text-align": "center"}),
                        html.H5(
                            "This app Summarize our finding in 2017-2018 Youtube Trending in several Countries",
                            className="app__header__title--grey",
                        ),

                        html.H3(
                            "Control Board",
                            className="control_label",
                            style = {"text-align": "center"}
                        ),
                        
                        
                        html.H6("Filter by Categories:", className="control_label"),
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
                        
                        html.H6("Filter by well type:", className="control_label"),
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
                                    [html.H3(id="Videostext",style = {"font-weight": "bold"}), html.H5("No. of Videos",style = {"font-weight": "bold"})],
                                    id="wells",
                                    className="control__panal",
                                    style = {"text-align": "center" , "vertical-align" : "middle"}
                                ),
                                html.Div(
                                    [html.H3(id="ViewsText",style = {"font-weight": "bold"}), html.H5("No. of Views",style = {"font-weight": "bold"})],
                                    id="gas",
                                    className="control__panal",
                                    style = {"text-align": "center" , "vertical-align" : "middle"}
                                ),
                                html.Div(
                                    [html.H3(id="LikesText",style = {"font-weight": "bold"}), html.H5("No. of Likes",style = {"font-weight": "bold"})],
                                    id="oil",
                                    className="control__panal",
                                    style = {"text-align": "center" , "vertical-align" : "middle"}
                                ),
                                html.Div(
                                    [html.H3(id="DislikesText",style = {"font-weight": "bold"}), html.H5("No. of Dislikes",style = {"font-weight": "bold"})],
                                    id="water",
                                    className="control__panal",
                                    style = {"text-align": "center" , "vertical-align" : "middle"}
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


@app.callback(
    
    Output("Videostext", "children"),
    Output("ViewsText", "children"),
    Output("LikesText", "children"),
    Output("DislikesText", "children"),

    
    Input(component_id='well_statuses',component_property='value'),
    Input(component_id='well_types',component_property='value'),
)
def update_text(categories,countries):
    videos, views, likes, dislikes = plotts.update_text(categories,countries) 
    return str(videos), str(views), str(likes), str(dislikes)

# my_slider

# Main
if __name__ == "__main__":
    app.run_server(debug=True)
