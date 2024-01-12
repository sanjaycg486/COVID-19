import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' start.
data_set_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
covid19_data_frame = pd.read_csv(data_set_url)
covid19_data_frame = covid19_data_frame.loc[
    covid19_data_frame['continent'] == 'Europe']  # Filter out data based on Europe continent.
# Reading the csv data file via Github URL and filtering the data based on the continent 'Europe' End.

# CSS stylesheet for dash start.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'COVID-19 Analysis in Europe.'

#Overwrite your CSS setting by including style locally
colors = {
    'background': '#2D2D2D',
    'text': '#E1E2E5',
    'figure_text': '#ffffff',
    'confirmed_text':'#3CA4FF',
    'deaths_text':'#f44336',
    'recovered_text':'#5A9E6F',
    'highest_case_bg':'#393939',
    
}

#Creating custom style for local use
divBorderStyle = {
    'backgroundColor' : '#393939',
    'borderRadius': '12px',
    'lineHeight': 0.9,
}

#Creating custom style for local use
boxBorderStyle = {
    'borderColor' : '#393939',
    'borderStyle': 'solid',
    'borderRadius': '10px',
    'borderWidth':2,
}
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
app.layout = html.Div(
    html.Div([
        
        # Header display
        html.Div(
            [
                html.H1(children='Analysis and Visualization of COVID-19 Impact and Response in Europe.',
                        style={
                            'textAlign': 'left',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                        },
                        className='ten columns',
                        ),

                html.Div([
                    html.Button(html.I(className="fa fa-info-circle"),
                        id='info-button',
                        style={
                             'color': colors['text'],
                             'fontSize':'36px'

                         },)

                ],className='two columns',),

                # Preload Modal windows and set "display": "none" to hide it first
                html.Div([  # modal div
                    html.Div([  # content div

                        dcc.Markdown('''
                            ##### Dataset provided by Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE):
                            https://systems.jhu.edu/
                           
                            Data Sources:
                            * World Health Organization (WHO): https://www.who.int/
                            * DXY.cn. Pneumonia. 2020. http://3g.dxy.cn/newh5/view/pneumonia.
                            * BNO News: https://bnonews.com/index.php/2020/02/the-latest-coronavirus-cases/
                            * National Health Commission of the People’s Republic of China (NHC):
                            http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml
                            * China CDC (CCDC): http://weekly.chinacdc.cn/news/TrackingtheEpidemic.htm
                            * Hong Kong Department of Health: https://www.chp.gov.hk/en/features/102465.html
                            * Macau Government: https://www.ssm.gov.mo/portal/
                            * Taiwan CDC: https://sites.google.com/cdc.gov.tw/2019ncov/taiwan?authuser=0
                            * US CDC: https://www.cdc.gov/coronavirus/2019-ncov/index.html
                            * Government of Canada: https://www.canada.ca/en/public-health/services/diseases/coronavirus.html
                            * Australia Government Department of Health: https://www.health.gov.au/news/coronavirus-update-at-a-glance
                            * European Centre for Disease Prevention and Control (ECDC): https://www.ecdc.europa.eu/en/geographical-distribution-2019-ncov-cases 
                            * Ministry of Health Singapore (MOH): https://www.moh.gov.sg/covid-19
                            * Italy Ministry of Health: http://www.salute.gov.it/nuovocoronavirus
                            * 1Point3Arces: https://coronavirus.1point3acres.com/en
                            * WorldoMeters: https://www.worldometers.info/coronavirus/
                            '''),
                        html.Hr(),
                        html.Button('Close', id='modal-close-button',
                        style={
                             'color': colors['text'],
                         },)
                    ],
                        style={
                            'fontSize': 10,
                            'lineHeight': 0.9,
                        },
                        className='modal-content',
                    ),
                ],
                    id='modal',
                    className='modal',
                    style={"display": "none"},
                ),
            ], className="row"
        ),

        # Top column display of confirmed, death and recovered total numbers
        html.Div([
            html.Div([
                html.H4(children='Total Cases: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['confirmed_text'],
                       }
                       ),
                html.P(f"{df_confirmed_total[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                    'fontSize': 30,
                }
                ),
                html.P('Past 24hrs increase: +' + f"{df_confirmed_total[-1] - df_confirmed_total[-2]:,d}"
                       + ' (' + str(round(((df_confirmed_total[-1] - df_confirmed_total[-2])/df_confirmed_total[-1])*100, 2)) + '%)',
                       style={
                    'textAlign': 'center',
                    'color': colors['confirmed_text'],
                }
                ),
            ],
                style=divBorderStyle,
                className='four columns',
            ),
            html.Div([
                html.H4(children='Total Deceased: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['deaths_text'],
                       }
                       ),
                html.P(f"{df_deaths_total[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                    'fontSize': 30,
                }
                ),
                html.P('Mortality Rate: ' + str(round(df_deaths_total[-1]/df_confirmed_total[-1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': colors['deaths_text'],
                }
                ),
            ],
                style=divBorderStyle,
                className='four columns'),
            html.Div([
                html.H4(children='Total Recovered: ',
                       style={
                           'textAlign': 'center',
                           'color': colors['recovered_text'],
                       }
                       ),
                html.P(f"{df_recovered_total[-1]:,d}",
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                    'fontSize': 30,
                }
                ),
                html.P('Recovery Rate: ' + str(round(df_recovered_total[-1]/df_confirmed_total[-1] * 100, 3)) + '%',
                       style={
                    'textAlign': 'center',
                    'color': colors['recovered_text'],
                }
                ),
            ],
                style=divBorderStyle,
                className='four columns'),
        ], className='row'),

        # place the line graph and the parallel coordinates plot side by side
        html.Div(
            [
                # html.H4(children='Global Covid-19 cases',
                #          style={
                #              'textAlign': 'center',
                #              'color': colors['text'],
                #              'backgroundColor': colors['background'],

                #          },
                #          className='twelve columns'
                #          ),
                
                html.Div([
                    # add a dropdown for selecting the country                    

                    # dcc.RadioItems(
                    #     id='graph-type',
                    #     options=[{'label': i, 'value': i}
                    #              for i in ['Total Cases', 'Daily Cases']],
                    #     value='Total Cases',
                    #     labelStyle={'display': 'inline-block'},
                    #     style={
                    #         'fontSize': 20,
                    #      },
                        
                    # )
                ],className='six columns'
                ),
                
                html.Div([
                    # add a DatePickerRange for selecting the date range

                    # dcc.RadioItems(
                    #     id='graph-high10-type',
                    #     options=[{'label': i, 'value': i}
                    #              for i in ['Confirmed Cases', 'Deceased Cases']],
                    #     value='Confirmed Cases',
                    #     labelStyle={'display': 'inline-block'},
                    #     style={
                    #         'fontSize': 20,
                    #      },
                        
                    # )
                ],className='five columns'
                ),
                
                html.Div([
                    dcc.Graph(
                        id='line-graph',

                    )
                ], className='six columns'
                ),
                
                html.Div([
                    dcc.Graph(
                        id='parallel-coordinates-plot',

                    )
                ], className='five columns'
                ),

            ], className="row",
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'backgroundColor': colors['background'],
            },
        ),

        # place the pie chart and the choropleth map side by side
        html.Div(
            [
                html.Div([
                    dcc.Graph(
                        id='pie-chart',

                    )
                ], className='six columns'
                ),
                
                html.Div([
                    dcc.Graph(
                        id='map',

                    )
                ], className='five columns'
                ),
            ], className="row",
            style={
                'textAlign': 'left',
                'color': colors['text'],
                'backgroundColor': colors['background'],
            },
        ),
     ], className='ten columns offset-by-one'
    ), 
    style={
        'textAlign': 'left',
        'color': colors['text'],
        'backgroundColor': colors['background'],
    },                 
    # html.H1(
    #     children='COVID-19 Data Visualization',
    #     style={
    #         'textAlign': 'center'}
    # ),
    # dcc.Tabs(id="tabs", value="tab-4", children=[
    #     dcc.Tab(label='Dashboard (Task 4)', value='tab-4'),
    #     dcc.Tab(label='Task 1', value='tab-1'),
    #     dcc.Tab(label='Task 2', value='tab-2'),
    #     dcc.Tab(label='Task 3', value='tab-3')
    # ]),
    # html.Div(id="tabs-content")
)
# Dash code end.


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
