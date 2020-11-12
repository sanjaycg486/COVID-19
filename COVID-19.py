import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' start.
data_set_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
covid19_data_frame = pd.read_csv(data_set_url)
covid19_data_frame = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'Europe']  # Filter out data based on Europe continent.
# Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' End.

# CSS stylesheet for dash start.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# CSS stylesheet for dash end.

# Task 1 from the concept paper start.
# Coded by Varun Nandkumar Golani

countries_in_europe = covid19_data_frame['location'].unique().tolist()

# Creating color dictionary by combining different discrete plotly maps
color_list = px.colors.qualitative.Alphabet + px.colors.qualitative.Dark24 + px.colors.qualitative.Dark2
color_dict = {countries_in_europe[index]: color_list[index]
              for index in range(len(countries_in_europe))}

fig1 = px.line(covid19_data_frame, x='date', y='stringency_index',
               labels={'date': 'Date', 'stringency_index': 'Government stringency index (0-100)',
                       'location': 'European country', 'total_cases': 'Total confirmed cases',
                       'total_deaths': 'Total deaths', 'new_cases': 'New confirmed cases',
                       'new_deaths': 'New deaths'},
               color='location', color_discrete_map=color_dict,
               hover_data=['total_cases', 'total_deaths', 'new_cases', 'new_deaths'],
               title='Line Graphs for Multivariate Data', height=700)
# Task 1 from the concept paper End.

# Task 2 from the concept paper start.
# Coded by Lalith Sagar Devagudi

# creating a data frame from the actual europe data frame
recent_deaths_data_frame = pd.DataFrame(columns=['location', 'total_cases', 'total_deaths', 'date', 'population',
                                                 'hospital_beds_per_thousand', 'median_age', 'life_expectancy'])

for country in countries_in_europe:
    recent_data = covid19_data_frame.loc[(covid19_data_frame['location'] == country)
                                         & pd.notnull(covid19_data_frame['total_deaths']) & pd.notnull(
        covid19_data_frame['total_cases']),
                                         ['location', 'total_cases', 'total_deaths', 'date', 'population',
                                          'hospital_beds_per_thousand', 'median_age', 'life_expectancy']]
    if not recent_data.empty:
        recent_deaths_data_frame = pd.concat([recent_deaths_data_frame, recent_data.iloc[[-1]]])

# adding death rates to the data frame 'recent_deaths_data_frame'
covid19_death_rate = []
for i in range(0, len(recent_deaths_data_frame)):
    covid19_death_rate.append(
        (recent_deaths_data_frame['total_deaths'].iloc[i] / recent_deaths_data_frame['total_cases'].iloc[i]) * 100)

recent_deaths_data_frame['covid19_death_rate'] = covid19_death_rate
recent_deaths_data_frame.fillna(0)

# getting number of countries for color
c = []
for i in range(0, len(countries_in_europe)):
    c.append(i)

# Allocating the countries unique numbers
lookup = dict(zip(countries_in_europe, c))
num = []
for i in recent_deaths_data_frame['location']:
    if i in lookup.keys():
        num.append(lookup[i])

# plotting Parallel Coordinates for the data frame
fig2 = go.Figure(data=go.Parcoords(
    line=dict(color=num,
              colorscale='HSV',
              showscale=False,
              cmin=0,
              cmax=len(countries_in_europe)),
    dimensions=list([
        dict(range=[0, len(countries_in_europe)],
             tickvals=c, ticktext=countries_in_europe,
             label="countries", values=num),
        dict(range=[0, max(recent_deaths_data_frame['hospital_beds_per_thousand'])],
             label="Hospitals beds per 1000", values=recent_deaths_data_frame['hospital_beds_per_thousand']),
        dict(range=[0, max(recent_deaths_data_frame['median_age'])],
             label='Median Age', values=recent_deaths_data_frame['median_age']),
        dict(range=[0, max(recent_deaths_data_frame['population'])],
             label='Population', values=recent_deaths_data_frame['population']),
        dict(range=[0, max(recent_deaths_data_frame['life_expectancy'])],
             label='Life expectancy', values=covid19_data_frame['life_expectancy']),
        dict(range=[0, max(recent_deaths_data_frame['covid19_death_rate'])],
             label='COVID-19 Death rate', values=recent_deaths_data_frame['covid19_death_rate']),
    ])
), layout=go.Layout(
    autosize=True,
    height=800,
    hovermode='closest',
    margin=dict(l=170, r=85, t=75)))

# updating margin of the plot
fig2.update_layout(
    title={
        'text': "Parallel Coordinates",
        'y': 0.99,
        'x': 0.2,
        'xanchor': 'center',
        'yanchor': 'top'}, font=dict(
        size=15,
        color="#000000"
    ))
# Task 2 from the concept paper end.

# Task 3 from the concept paper start.
# Coded by Varun Nandkumar Golani

recent_tests_data_frame = pd.DataFrame(columns=['location', 'total_tests', 'date'])
for country in countries_in_europe:
    country_recent_data = covid19_data_frame.loc[(covid19_data_frame['location'] == country)
                                                 & pd.notnull(covid19_data_frame['total_tests']),
                                                 ['location', 'total_tests', 'date']]
    if not country_recent_data.empty:
        recent_tests_data_frame = pd.concat([recent_tests_data_frame, country_recent_data.iloc[[-1]]])

fig3 = px.pie(recent_tests_data_frame, values='total_tests', names='location', title='Pie Chart'
              , color='location', color_discrete_map=color_dict, hover_data=['date']
              , labels={'location': 'European country', 'date': 'Recent data available date',
                        'total_tests': 'Total tests'}, height=700)

fig3.update_traces(textposition='inside', textinfo='percent+label'
                   , hovertemplate='Total tests: %{value} <br>Recent data available date,' +
                                   'European country: %{customdata}</br>')
# Task 3 from the concept paper end.

# Task 4 from the concept paper Start.
# coded by Sanjay Gupta

iso_code_list = covid19_data_frame["iso_code"].unique().tolist()
iso_code_color_dict = {iso_code_list[index]: color_list[index] for index in range(len(iso_code_list))}


def calculate_covid19_death_rate(data_frame):
    death_rate_data = []
    for item in range(len(data_frame)):
        death_rate_data.append(
            round(((data_frame["total_deaths"].iloc[[item]] / data_frame["total_cases"].iloc[[item]]) * 100), 2))
    return death_rate_data


def select_recent_data_for_each_countries(data_frame, code_list):
    death_rate_data_frame = pd.DataFrame(columns=['iso_code', 'location', 'date', 'total_cases',
                                                  'new_cases', 'total_deaths', 'new_deaths'])
    for iso_code in code_list:
        recent_data_of_countries = data_frame.loc[(data_frame['iso_code'] == iso_code)
                                                  & pd.notnull(data_frame['total_deaths'])
                                                  & pd.notnull(data_frame['total_cases']),
                                                  ['iso_code', 'location', 'date', 'total_cases',
                                                   'new_cases', 'total_deaths', 'new_deaths']]

        if not recent_data_of_countries.empty:
            death_rate_data_frame = pd.concat([death_rate_data_frame, recent_data_of_countries.iloc[[-1]]])

    death_rate_data_frame['covid19_death_rate'] = calculate_covid19_death_rate(death_rate_data_frame)

    return death_rate_data_frame


recent_death_rate_data_frame = select_recent_data_for_each_countries(covid19_data_frame, iso_code_list)

fig4 = px.choropleth(recent_death_rate_data_frame, color='iso_code', locations='iso_code',
                     hover_name='location', hover_data=['date', 'covid19_death_rate', 'total_deaths', 'total_cases'],
                     labels={'iso_code': 'ISO code', 'date': 'Date', 'location': 'European country',
                             'total_cases': 'Total confirmed cases', 'total_deaths': 'Total deaths',
                             'covid19_death_rate': 'COVID-19 Death rate(%)'},
                     scope="europe", color_discrete_map=iso_code_color_dict)
fig4.update_geos(fitbounds="locations", lataxis_showgrid=True, lonaxis_showgrid=True)
fig4.update_layout(height=700, title='Choropleth map (Europe)')
# Task 4 from the concept paper End.

# Dash code start.
app.layout = html.Div([
    html.H1(
        children='COVID-19 Data Visualization',
        style={
            'textAlign': 'center'}
    ),
    dcc.Tabs(id="tabs", value="tab-4", children=[
        dcc.Tab(label='Dashboard (Task 4)', value='tab-4'),
        dcc.Tab(label='Task 1', value='tab-1'),
        dcc.Tab(label='Task 2', value='tab-2'),
        dcc.Tab(label='Task 3', value='tab-3')
    ]),
    html.Div(id="tabs-content")
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([dcc.Graph(id='line-graph', figure=fig1)])
    elif tab == 'tab-2':
        return html.Div([dcc.Graph(id='parallel-coordinates', figure=fig2)])
    elif tab == 'tab-3':
        return html.Div([dcc.Graph(id='pie-chart', figure=fig3)])
    else:
        return html.Div([dcc.Graph(id='choropleth-map', figure=fig4)])


if __name__ == '__main__':
    app.run_server(debug=True)

# To view the dash output just open the link http://127.0.0.1:8050/ in the browser
# Dash code end.
