import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Define the launch site options
options_sites = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
]

# Create the layout of the application
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    # Dropdown for selecting launch site
    html.Div([
        html.Label("Select Launch Site:"),
        dcc.Dropdown(
            id='site-dropdown',
            options=options_sites,
            value='ALL',  # Set default value to 'ALL' so it shows all sites initially
            placeholder='Select a Launch Site',
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}
        )
    ]),
    html.Br(),
    # Pie chart for successful launches
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    # Payload mass range slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: f'{i}' for i in range(int(min_payload), int(max_payload), 10000)}, 
        value=[min_payload, max_payload],
    ),
    html.Br(),
    # Scatter plot for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for Pie Chart (Success vs Failure)
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
    
    # Create pie chart to show the success/failure distribution
    pie_fig = px.pie(filtered_df, names='class', title=f"Success vs Failure for {selected_site}")
    return pie_fig

# TASK 4: Callback for Scatter Plot (Payload vs Success)
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Create scatter plot to show payload vs launch success
    scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='class',
                             title=f"Payload vs Launch Success for {selected_site} (Payload Range: {low}kg - {high}kg)")
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
