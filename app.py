
import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import data_processing as dp
import plotly.graph_objs as go


####################
# Dash App
####################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

####################
# Navbar Component
####################
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
navbar = dbc.Navbar(
    [
        # Use row and col to control vertical alignment of logo / brand
        dbc.Row(
            [
                dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px"), className = "logo"),
                dbc.Col(dbc.NavbarBrand("Airline Safety Dashboard", className = "ml-2 header-title")),
            ],
            align="center"
        )
    ],
    color="dark",
    dark=True,
)

####################
# Helper Functions
####################
def multiple_string_lines(title, threshold):
    if (len(title) > threshold):
        words_arr = title.split(' ')
        interval = int(len(words_arr) / 2)
        return ' '.join(words_arr[0:interval]) + '<br>' + ' '.join(words_arr[interval:len(words_arr)])
    else:
        return title

####################
# Get Data
####################
df = dp.get_data()
df_long = dp.get_long_data()
period_mean = dp.get_period_mean_data()
period_total_perc = dp.get_period_total_perc_data()
df_incidents = dp.get_formatted_incident_rate_perc_changed_by_airline_data()
df_fatal = dp.get_formatted_fatal_rate_perc_changed_by_airline_data()

####################
# Color Theme for Graphs
####################
period_colors = {
    '1985-1999': '#33626C',
    '2000-2014': '#C1D6E2'
}

other_colors = ['#5F5B6E', '#312932', '#458CA5', '#F6A941']


####################
# Static Graphs
####################
# Create indicator graph for incident rate with percent change from 85-99 to 00-14
incident_rate_perc_change_indicator = dcc.Graph(
    id = 'incident_rate_perc_change_indicator',
    figure = {
        'data': [
            go.Indicator(
                mode = "number+delta",
                value = period_mean.loc[period_mean.period == '2000-2014', 'incident_rate'].max(),
                delta = {
                    'position': 'bottom',
                    'relative': True,
                    'reference': period_mean.loc[period_mean.period == '1985-1999', 'incident_rate'].max()
                }
            )
        ],
        'layout': go.Layout(
            title = multiple_string_lines('2000-2014 Incidents Rate and % Change from 1985-1999', 10),
            height = 250
        )
    }
)

# Create indicator graph for fatal accidents rate with percent change from 85-99 to 00-14
fatal_accidents_rate_perc_change_indicator = dcc.Graph(
    id = 'fatal_accidents_rate_perc_change_indicator',
    figure = {
        'data': [
            go.Indicator(
                mode = "number+delta",
                value = period_mean.loc[period_mean.period == '2000-2014', 'fatal_accidents_rate'].max(),
                delta = {
                    'position': 'bottom',
                    'relative': True,
                    'reference': period_mean.loc[period_mean.period == '1985-1999', 'fatal_accidents_rate'].max()
                }
            )
        ],
        'layout': go.Layout(
            title = multiple_string_lines('2000-2014 Fatal Accidents Rate and % Change from 1985-1999', 10),
            height = 250
        )
    }
)

# Shows % of total stacked bar graph for two different accident types (incident & fatal)
period_total_perc_stacked_bar_graph = dcc.Graph( \
    id = 'period_total_perc',
    figure = {
        'data': [
            go.Bar(
                x = period_total_perc['period']
                , y = period_total_perc['incidents']
                , text = period_total_perc['display_incidents']
                , textposition = 'auto'
                , name = 'Non-fatal Accidents'
                , marker_color = other_colors[2]
            ),
            go.Bar(
                x = period_total_perc['period']
                , y = period_total_perc['fatal_accidents']
                , text = period_total_perc['display_fatal_accidents']
                , textposition = 'auto'
                , name = 'Fatal Accidents'
                , marker_color = other_colors[3]
            )
        ],
        'layout': go.Layout (
            title = multiple_string_lines('Number of Fatal Accidents vs Non-Fatal Incidents Between Two Periods', 15),
            xaxis = dict (
                title = "Time Periods"
            ),
            yaxis = dict(
                title = "Incidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest',
            barmode = 'stack'
        )
    }
)

# Bar graph comparing the mean accident rate between 85-99 and 00-14
period_accident_rate_bar_graph = dcc.Graph( \
    id = 'period_incident_rate',
    figure = {
        'data': [
            go.Bar(
                x = period_mean.loc[period_mean.period == '1985-1999', 'period'],
                y = period_mean.loc[period_mean.period == '1985-1999', 'incident_rate'],
                text= "{:.2f}".format(period_mean.loc[period_mean.period == '1985-1999', 'incident_rate'].max()),
                textposition='auto',
                name = '1985-1999',
                marker_color = period_colors['1985-1999'],
                showlegend = False
            ),
            go.Bar(
                x = period_mean.loc[period_mean.period == '2000-2014', 'period'],
                y = period_mean.loc[period_mean.period == '2000-2014', 'incident_rate'],
                text= "{:.2f}".format(period_mean.loc[period_mean.period == '2000-2014', 'incident_rate'].max()),
                textposition='auto',
                name = '2000-2014',
                marker_color = period_colors['2000-2014'],
                showlegend = False
            )
        ],
        'layout': go.Layout (
            title = 'Incidents Rate 1985-1999 vs 2000-2014',
            xaxis = dict (
                title = "Time Periods"
            ),
            yaxis = dict(
                title = "Incidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest'
        )
    }
)

# Bar graph comparing the mean fatal accidents rate between 85-99 and 00-14
period_fatal_accidents_rate_bar_graph =   dcc.Graph( \
      id = 'period_fatal_accidents_rate',
      figure = {
        'data': [
            go.Bar(
                x = period_mean.loc[period_mean.period == '1985-1999', 'period'],
                y = period_mean.loc[period_mean.period == '1985-1999', 'fatal_accidents_rate'],
                text= "{:.2f}".format(period_mean.loc[period_mean.period == '1985-1999', 'fatal_accidents_rate'].max()),
                textposition='auto',
                name = '1985-1999',
                marker_color = period_colors['1985-1999'],
                showlegend = False
            ),
            go.Bar(
                x = period_mean.loc[period_mean.period == '2000-2014', 'period'],
                y = period_mean.loc[period_mean.period == '2000-2014', 'fatal_accidents_rate'],
                text= "{:.2f}".format(period_mean.loc[period_mean.period == '2000-2014', 'fatal_accidents_rate'].max()),
                textposition='auto',
                name = '2000-2014',
                marker_color = period_colors['2000-2014'],
                showlegend = False
            )
        ],
        'layout': go.Layout(
            title = 'Fatal Accidents Rate 1985-1999 vs 2000-2014',
            xaxis = dict (
                title = "Time Periods"
            ),
            yaxis = dict(
                title = "Fatal Accidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest'
        )
    }
)

# Tabular data showing a list of airlines & the corresponding percent change in its incident rate from 85-99 to 00-14 (sorted desc)
airline_incident_perc_change_table = dcc.Graph(
    id = 'airline_incident_perc_change_table',
    figure = {
        'data': [
            go.Table(
                header = dict(
                    values = ['Airline', 'Incident Rate (85-99)', 'Incident Rate (00-14)', 'Incident Rate % Change'],
                    line = dict(color='rgb(50,50,50)'),
                    align = ['left'] * 2,
                    font = dict( color = 'white', size=14),
                    fill_color = 'royalblue'
                ),
                cells = dict(
                    values = [df_incidents.airline, df_incidents.incident_rate_85_99.round(2)
                    , df_incidents.incident_rate_00_14.round(2), df_incidents['Incident Rate % Change']],
                    align = ['left'] * 5,
                    fill = dict(color='rgb(245,245,245)')
                )
            )
        ],
        'layout': go.Layout(
            title = 'Airline Incident Rate % Change Between Time Periods'
        )
    }
)

# Tabular data showing a list of airlines & the corresponding percent change in its fatal accident rate from 85-99 to 00-14 (sorted desc)
airline_fatal_perc_change_table = dcc.Graph(
    id = 'airline_fatal_perc_change_table',
    figure = {
        'data': [
            go.Table(
                header = dict(
                    values = ['Airline', 'Fatal Accidents Rate (85-99)', 'Fatal Accidents Rate (00-14)', 'Fatal Accidents Rate % Change'],
                    line = dict(color='rgb(50,50,50)'),
                    align = ['left'] * 2,
                    font = dict( color = 'white', size=14),
                    fill_color = 'royalblue'
                ),
                cells = dict(
                    values = [df_fatal .airline, df_fatal .fatal_accidents_rate_85_99.round(2)
                    , df_fatal .fatal_accidents_rate_00_14.round(2), df_fatal ['Fatal Accidents Rate % Change']],
                    align = ['left'] * 5,
                    fill = dict(color='rgb(245,245,245)')
                )
            )
        ],
        'layout': go.Layout(
            title = 'Airline Fatal Accidents Rate % Change Between Time Periods'
        )
    }
)

# Scatterplot to capture if 85-99's fatal accident rates has a strong linear relationship with 00-14's fatal accident rates
fatal_rate_scatterplot = dcc.Graph(
    id = 'fatal_rate_scatterplot',
    figure = {
        'data': [
            go.Scatter(
                x = df['fatal_accidents_rate_85_99'],
                y = df['fatal_accidents_rate_00_14'],
                text = df['airline'],
                mode = 'markers',
                marker_color = '#458CA5'
            )
        ],
        'layout': go.Layout(
            title = 'Fatal Accidents Rate Scatterplot 85-99 vs 00-14',
            xaxis = dict (
                title = "Fatal Accidents Rate 85-99 (per trillion ASK)"
            ),
            yaxis = dict(
                title = "Fatal Accidents Rate Rate 00-14 (per trillion ASK)"
            ),
            hovermode = 'closest'
        )
    }
)

# Pearson correlation between 85-99 fatal accident rate & 00-14 fatal accident rate
fatal_rate_corr_indicator =  dcc.Graph(
    id = 'fatal_rate_corr_indicator',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = df.loc[:, ['fatal_accidents_rate_00_14', 'fatal_accidents_rate_85_99']].corr()['fatal_accidents_rate_00_14']['fatal_accidents_rate_85_99']
            )
        ],
        'layout': go.Layout(
            title = multiple_string_lines('Fatal Accident Rate Pearson Correlation', 10),
            height = 250
        )
    }
)

# Scatterplot to capture if 85-99's incident rates has a strong linear relationship with 00-14's incident rates
incident_rate_scatterplot = dcc.Graph(
    id = 'incident_rate_scatterplot',
    figure = {
        'data': [
            go.Scatter(
                x = df['incident_rate_85_99'],
                y = df['incident_rate_00_14'],
                text = df['airline'],
                mode = 'markers',
                marker_color = period_colors['1985-1999']
            )
        ],
        'layout': go.Layout(
            title = 'Incident Rate Scatterplot 85-99 vs 00-14',
            xaxis = dict (
                title = "Incident Rate 85-99 (per trillion ASK)"
            ),
            yaxis = dict(
                title = "Incidents Rate 00-14 (per trillion ASK)"
            ),
            hovermode = 'closest'
        )
    }
)

# Pearson correlation between 85-99 incident rate & 00-14 incident rate
incident_rate_corr_indicator =  dcc.Graph(
    id = 'incident_rate_corr_indicator',
    figure = {
        'data': [
            go.Indicator(
                mode = "number",
                value = df.loc[:, ['incident_rate_00_14', 'incident_rate_85_99']].corr()['incident_rate_00_14']['incident_rate_85_99']
            )
        ],
        'layout': go.Layout(
            title = multiple_string_lines('Fatal Accident Rate Pearson Correlation', 10),
            height = 250
        )
    }
)

####################
## Filterable Graphs
####################

# These graphs generate bar graphs for user's chosen airlines and three most comparable airlines based on ASK
# Includes dash callbacks to update graphs based on user's airline choice
# Defaulted to Southwest Airlines
@app.callback(
    Output('airline_incident_rate_bar_graph', 'figure'),
    [Input('airline_picker', 'value')]
)
def update_incident_rate_airline_comp_graphs(airline):
    fig = {
        'data': generate_incident_rate_airline_comp_graph(airline)
        , 'layout': go.Layout(
            title = 'Airline Comparisons Incident Rate',
            yaxis = dict(
                title = "Incidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest',
            barmode='group'
        )
    }

    return fig

def generate_incident_rate_airline_comp_graph(airline):
    comp = dp.get_comp_airline(airline)
    traces = []
    traces.append(
        go.Bar(
            x = df.loc[df['airline'] == airline, 'airline'],
            y = df.loc[df['airline'] == airline, 'incident_rate_85_99'],
            text= "{:.2f}".format(df.loc[df['airline'] == airline, 'incident_rate_85_99'].max()),
            textposition='auto',
            marker_color = period_colors['1985-1999'],
            offsetgroup = 0,
            name = '1985-1999',
            showlegend = True
        )
    )
    # Add 00-14 data
    traces.append(
        go.Bar(
            x = df.loc[df['airline'] == airline, 'airline'],
            y = df.loc[df['airline'] == airline, 'incident_rate_00_14'],
            text= "{:.2f}".format(df.loc[df['airline'] == airline, 'incident_rate_00_14'].max()),
            textposition='auto',
            marker_color = period_colors['2000-2014'],
            offsetgroup = 1,
            name = '2000-2014',
            showlegend = True
        )
    )

    for al in comp:
        # Add 85-99 data
        traces.append(
            go.Bar(
                x = df.loc[df['airline'] == al, 'airline'],
                y = df.loc[df['airline'] == al, 'incident_rate_85_99'],
                text= "{:.2f}".format(df.loc[df['airline'] == al, 'incident_rate_85_99'].max()),
                textposition='auto',
                marker_color = period_colors['1985-1999'],
                offsetgroup = 0,
                showlegend = False
            )
        )
        # Add 00-14 data
        traces.append(
            go.Bar(
                x = df.loc[df['airline'] == al, 'airline'],
                y = df.loc[df['airline'] == al, 'incident_rate_00_14'],
                text= "{:.2f}".format(df.loc[df['airline'] == al, 'incident_rate_00_14'].max()),
                textposition='auto',
                marker_color = period_colors['2000-2014'],
                offsetgroup = 1,
                showlegend = False
            )
        )

    return traces

airline_incident_rate_bar_graph = dcc.Graph(
    id = 'airline_incident_rate_bar_graph',
    figure = {
        'data': generate_incident_rate_airline_comp_graph("Southwest Airlines"),
        'layout': go.Layout(
            title = 'Airline Comparisons Incident Rate',
            yaxis = dict(
                title = "Incidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest',
            barmode='group'
        )
    }
)

@app.callback(
    Output('airline_fatal_accidents_rate_bar_graph', 'figure'),
    [Input('airline_picker', 'value')]
)
def update_fatal_rate_airline_comp_graphs(airline):
    fig = {
        'data': generate_fatal_rate_airline_comp_graph(airline)
        , 'layout': go.Layout(
            title = 'Airline Comparisons Fatal Accidents Rate',
            yaxis = dict(
                title = "Fatal Accidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest',
            barmode='group'
        )
    }

    return fig

def generate_fatal_rate_airline_comp_graph(airline):
    comp = dp.get_comp_airline(airline)
    traces = []
    traces.append(
        go.Bar(
            x = df.loc[df['airline'] == airline, 'airline'],
            y = df.loc[df['airline'] == airline, 'fatal_accidents_rate_85_99'],
            text= "{:.2f}".format(df.loc[df['airline'] == airline, 'fatal_accidents_85_99'].max()),
            textposition='auto',
            marker_color = period_colors['1985-1999'],
            offsetgroup = 0,
            name = '1985-1999',
            showlegend = True
        )
    )
    # Add 00-14 data
    traces.append(
        go.Bar(
            x = df.loc[df['airline'] == airline, 'airline'],
            y = df.loc[df['airline'] == airline, 'fatal_accidents_00_14'],
            text= "{:.2f}".format(df.loc[df['airline'] == airline, 'fatal_accidents_00_14'].max()),
            textposition='auto',
            marker_color = period_colors['2000-2014'],
            offsetgroup = 1,
            name = '2000-2014',
            showlegend = True
        )
    )

    for al in comp:
        # Add 85-99 data
        traces.append(
            go.Bar(
                x = df.loc[df['airline'] == al, 'airline'],
                y = df.loc[df['airline'] == al, 'incident_rate_85_99'],
                text= "{:.2f}".format(df.loc[df['airline'] == al, 'fatal_accidents_85_99'].max()),
                textposition='auto',
                marker_color = period_colors['1985-1999'],
                offsetgroup = 0,
                showlegend = False
            )
        )
        # Add 00-14 data
        traces.append(
            go.Bar(
                x = df.loc[df['airline'] == al, 'airline'],
                y = df.loc[df['airline'] == al, 'incident_rate_00_14'],
                text= "{:.2f}".format(df.loc[df['airline'] == al, 'fatal_accidents_00_14'].max()),
                textposition='auto',
                marker_color = period_colors['2000-2014'],
                offsetgroup = 1,
                showlegend = False
            )
        )

    return traces

airline_fatal_accidents_rate_bar_graph = dcc.Graph(
    id = 'airline_fatal_accidents_rate_bar_graph',
    figure = {
        'data': generate_fatal_rate_airline_comp_graph("Southwest Airlines"),
        'layout': go.Layout(
            title = 'Airline Comparisons Fatal Accidents Rate',
            yaxis = dict(
                title = "Fatal Accidents Rate (per trillion ASK)"
            ),
            hovermode = 'closest',
            barmode='group'
        )
    }
)

####################
## Dropdown Options
####################
options = []
for airline in list(df.airline.unique()):
    mydict = {}
    mydict['label'] = airline
    mydict['value'] = airline
    options.append(mydict)

####################
## Main Layout
####################
app.layout = html.Div([
    navbar,

    # Overall fatal accidents and incidents trends
    html.H1("General Trends Between Time Periods", className="section-title"),
    period_total_perc_stacked_bar_graph,

    # Incident Rate & Fatal Accident Rate trends
    html.H1("Incident & Fatal Accident Rate Time Period Trends", className="section-title"),
    dbc.Row(
        [
            dbc.Col(html.Div(incident_rate_perc_change_indicator), lg = 4),
            dbc.Col(html.Div(fatal_accidents_rate_perc_change_indicator), lg = 4)
        ],
        justify = "center"
    ),
    dbc.Row(
        [
            dbc.Col(period_accident_rate_bar_graph, lg = 6),
            dbc.Col(period_fatal_accidents_rate_bar_graph, lg = 6)
        ]
    ),

    # Airline % change between time periods - cross tab
    html.H1("Airline Incident & Fatal Accidents Rate % Change Between Time Periods", className="section-title"),
    airline_incident_perc_change_table,
    airline_fatal_perc_change_table,

    # Scatterplots & Corr indicator graphs
    html.H1("Airline Incident & Fatal Accidents Rate Correlation Between Time Periods", className="section-title"),
    dbc.Container(html.P("There is low positive pearson correlation between fatal accidents rate & incidents rate between two periods (i.e. do airlines with bad fatal accidents rate in 1985-1999 continue to have bad fatal accidents rate in 2000-2014?)")),
    dbc.Row(
        [dbc.Col(fatal_rate_corr_indicator , lg = 3)]
        , justify = "center"
    ),
    fatal_rate_scatterplot,
    dbc.Row(
        [dbc.Col(incident_rate_corr_indicator , lg = 3)]
        , justify = "center"
    ),
    incident_rate_scatterplot,

    # Airline Comparisons
    html.H1("Airline Comparisons", className="section-title"),
    dbc.Container(html.P("Select an airline to compare incident rate and fatal accident rate against the chosen airline's three closest competitors in terms of Available Seats Kilometers (captures the total flight passenger capacity of an ailrine in kilometers). ")),
    dbc.Row(
        [
            dbc.Col(
                html.Label(
                    [
                        "Choose an Airline",
                        dcc.Dropdown(
                            id = 'airline_picker',
                            options = options,
                            value = 'Southwest Airlines',
                            multi = False
                        )
                    ]
                    , className = "small-margin-left"
                )
                ,
                sm = 4
            )
        ]
    ),
    airline_incident_rate_bar_graph,
    airline_fatal_accidents_rate_bar_graph
])

# Run the Dash App
if __name__ == '__main__':
  app.run_server(debug=True)
