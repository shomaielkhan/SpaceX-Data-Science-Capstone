# Import libraries
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the dataset
spacex_df = pd.read_csv("C:/Users/User-PC/Data Science Capestone/dataset_part_2.csv")

# Get min and max payload
min_payload = spacex_df['PayloadMass'].min()
max_payload = spacex_df['PayloadMass'].max()

# Create Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1('SpaceX Falcon 9 Launch Dashboard', style={'textAlign': 'center'}),
    
    # Dropdown for Launch Site
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['LaunchSite'].unique()],
        value='ALL',
        placeholder="Select Launch Site",
        searchable=True
    ),
    html.Br(),
    
    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    html.P("Payload range (Kg):"),
    
    # Payload range slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(min_payload): str(int(min_payload)),
               int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    
    # Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callbacks
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='LaunchSite', values='Class',
                     title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['LaunchSite'] == selected_site]
        fig = px.pie(filtered_df, names='Class', title=f'Total Success vs Failure for {selected_site}')
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['PayloadMass'] >= low) & (spacex_df['PayloadMass'] <= high)
    filtered_df = spacex_df[mask]
    
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['LaunchSite'] == selected_site]
    
    fig = px.scatter(filtered_df, x='PayloadMass', y='Class',
                     color='BoosterVersion', title='Payload vs Success',
                     hover_data=['LaunchSite'])
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
