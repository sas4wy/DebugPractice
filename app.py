# %% [markdown]
# Objective: Practice adding callbacks to Dash apps.
# 
# Task:
# (1) Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. 
# 
# TASK 1 is the same as ASSIGNMENT 4. You are welcome to update your code. 
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# - The dropdown should allow the user to select multiple countries
# - The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# - The slider should allow the user to select a range of years
# - The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# - The graph should display the gdpPercap for each country as a line
# - Each country should have a unique color
# - The graph should have a title and axis labels in reader friendly format
# 
# 
# 
# 
# (2) Write Callback functions for the slider and dropdown to interact with the graph
# 
# This means that when a user updates a widget the graph should update accordingly.
# The widgets should be independent of each other. 
# 
# 
# Layout:
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# 
# Submission:
# - Deploy your app on Render. 
# - In Canvas, submit the URL to your public Github Repo (made specifically for this assignment)
# - The readme in your GitHub repo should contain the URL to your Render page. 
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# importing dependencies
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

# %%
# read in and view dataframe
df = pd.read_csv("gdp_pcap.csv")
df.head()

# %%
# transforming dataframe by creating a 'year' column
df = df.melt(id_vars='country', 
                    var_name='year', 
                    value_name='gdp_per_capita')
# getting rid of the "k" in the dataframe and placing in scientific notation
df['gdp_per_capita'] = df['gdp_per_capita'].replace({'k': '*1e3'}, regex=True)
# putting 'year' and 'gdp_per_capita' into integers and floats
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['gdp_per_capita'] = pd.to_numeric(df['gdp_per_capita'], errors='coerce')

# %%
# checking tranformed dataset
df.head()

# %%
# load the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# %%
# initialize the app
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

# %%
# creating layout 
app.layout = html.Div([
    #add title and description
    html.H2("Countries' GDP Per Capita by Year"),
    html.H5('This app allows users to select multiple countries and years of their choosing to see the indicated GDP capita graphically. The data shows current, past, and future estimated GDP per Capita values based on data from the World Bank, economic history researchers, and the IMF World Economic Outlook. It is important to remember that there are vast differences in currencies, inflation rates, and prices. Due to this, GDP is the standardizing constant used in the United States and is therefore, used here.'),
    # layout elements
    html.Div([
        html.Div([
            # create dropdown menu to select countries with preselected values to avoid error
            html.Label('Select Countries'),
            dcc.Dropdown(
                options=[{'label': country, 'value': country} for country in df['country'].unique()],
                id='country-dropdown',
                value=['Angola','Afghanistan'],
                multi=True
            ),
        ],
         #changing format so that it takes up half page and looks cohesive
          style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'}),
        
        html.Div([
            # create slider to select year with preselected values to avoid error & also dividing slider into increments
            dcc.RangeSlider(
                min=df['year'].min(),
                max=df['year'].max(),  
                step=None, 
                id='year-range-slider',
                marks = {str(year): str(year) for year in range(df['year'].min(), df['year'].max() + 1, 50)},
                value=[1950, 1970]
            ) , 
        ],
        # changing format
          style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'})
        ]),
        # gcp per capita graph
        dcc.Graph(id='gdp-per-capita-graph')
])
# define callbacks/update graph function        
@app.callback(
    Output('gdp-per-capita-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_graph(selected_countries, selected_years):

    # filtering dataframe
    filtered_df = df[(df['country'].isin(selected_countries)) & (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

    # making graph
    fig = px.line(filtered_df,
                       #x axis as year, y axis as gdp per capita, and set color to country
                       x='year', 
                       y='gdp_per_capita', 
                       title='GDP per Capita Over Time for Selected Countries',
                       color='country', 
                       markers=True)
    fig.update_layout(
                    title='GDP per Capita Over Time for Selected Countries',
                    xaxis_title='Year',
                    yaxis_title='GDP per Capita',
                )
    return fig        

#run app
if __name__ == '__main__':
    app.run_server(debug=True)


