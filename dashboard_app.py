import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, Input, Output, State
import threading
import os
import time

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Environmental Impact of EV Adoption"

# ========== Layout ==========
app.layout = html.Div([
    html.Title("Exploratory Data Analysis Dashboard"),
    html.H1("Exploratory Data Analysis Dashboard", style={'textAlign': 'center'}),
    html.P(
    "Welcome to the Environmental Impact of EV Adoption Dashboard. "
    "This interactive platform is designed to help you explore and understand the relationship "
    "between electric vehicle (EV) adoption and environmental factors such as air quality across Ireland. "
    "Use the tabs to navigate between combined and individual dataset insights. "
    "Click on any visualization to view it in a larger format with detailed descriptions.",
    style={'textAlign': 'center', 'fontSize': '18px'}
),
html.P(
    "This dashboard presents visualizations and analyses for different datasets, "
    "including air quality, electric vehicle registrations, and EV stations. "
    "Explore the visualizations by navigating through the tabs and selecting the dataset of interest.",
    style={'textAlign': 'center', 'fontSize': '18px'}
),

    dcc.Tabs(id='tabs', value='tab-merged', children=[
        dcc.Tab(label='Merged Dataset', value='tab-merged'),
        dcc.Tab(label='Individual Dataset', value='tab-individual')
    ]),

    html.Div(id='tabs-content')
])

# ========== Image Modal ==========
def create_image_modal(image_id, image_src, image_desc, header_text):
    return html.Div([
        html.Img(
            id=image_id,
            src=image_src,
            style={'width': '100%', 'cursor': 'pointer'}
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(header_text),
                dbc.ModalBody([
                    html.Img(src=image_src, style={'width': '100%'}),
                    html.P(image_desc, style={'marginTop': '15px'})
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id=f"close-{image_id}", className="ms-auto", n_clicks=0)
                ),
            ],
            id=f"modal-{image_id}",
            size="xl",
            is_open=False,
        ),
    ])

# ========== Modal Callback Registration ==========
def register_modal_callbacks(app, image_ids):
    for image_id in image_ids:
        modal_id = f"modal-{image_id}"
        close_id = f"close-{image_id}"

        def make_callback(modal_id=modal_id, image_id=image_id, close_id=close_id):
            @app.callback(
                Output(modal_id, "is_open"),
                [Input(image_id, "n_clicks"), Input(close_id, "n_clicks")],
                [State(modal_id, "is_open")]
            )
            def toggle_modal(n1, n2, is_open):
                if n1 or n2:
                    return not is_open
                return is_open
        make_callback()

# ========== Tab Content Callback ==========
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_tab(tab):
    if tab == 'tab-merged':
        return html.Div([
            html.H3("Merged Dataset EDA"),
            html.Div([
                html.Div([
                    create_image_modal("image-click-1", "/assets/ev_vehicle_types_by_county.png",
                                       "This chart shows the distribution of different EV vehicle types across counties.",
                                       "EV Vehicle Types by County"),
                ], style={'display': 'inline-block', 'width': '48%', 'padding': '1%'}),
                html.Div([
                    create_image_modal("image-click-2", "/assets/ev_vs_pm25_scatterplot.png",
                                       "This scatter plot visualizes the relationship between EV registrations and PM2.5 levels.",
                                       "EV vs PM2.5 Scatterplot"),
                ], style={'display': 'inline-block', 'width': '48%', 'padding': '1%'}),
                html.Div([
                    create_image_modal("image-click-3", "/assets/top10_counties_ev_pm25.png",
                                       "Top 10 counties with highest PM2.5 and EV registrations.",
                                       "Top 10 Counties EV vs PM2.5"),
                ], style={'display': 'inline-block', 'width': '48%', 'padding': '1%'}),
                html.Div([
                    create_image_modal("image-click-4", "/assets/Top Counties by Charging Stations with EV Registrations.jpeg",
                                       "Top 10 counties charging station vs EV registrations.",
                                       "Charging Stations vs EV Registration"),
                ], style={'display': 'inline-block', 'width': '48%', 'padding': '1%'}),
                html.Div([
                    create_image_modal("image-click-5", "/assets/heatmap.png",
                                       "Heatmap showing EV registration distribution.",
                                       "EV Registration Heatmap"),
                ], style={'display': 'block', 'margin': '0 auto', 'padding': '1%', 'width': '48%'}),
            ])
        ])
    elif tab == 'tab-individual':
        return html.Div([
            html.H3("Select a Dataset"),
            dcc.Dropdown(
                id='dataset-dropdown',
                options=[
                    {'label': 'Air Quality Index', 'value': 'air_quality'},
                    {'label': 'Ev Registration', 'value': 'ev_registration'},
                    {'label': 'Ev Station', 'value': 'ev_station'}
                ],
                value='air_quality'
            ),
            html.Div(id='individual-images')
        ])

# ========== Dropdown Image Callback ==========
@app.callback(
    Output('individual-images', 'children'),
    Input('dataset-dropdown', 'value')
)
def update_images(dataset):
    def image_grid(elements):
        return html.Div([
            html.Div(img, style={'display': 'inline-block', 'width': '48%', 'padding': '1%'})
            for img in elements
        ])

    if dataset == 'air_quality':
        return html.Div([
            html.P(
                "This dataset provides PM2.5 levels across various counties, helping identify pollution trends "
                "and the impact of environmental policies.",
                style={'color': 'red', 'fontWeight': 'bold'}
            ),
            image_grid([
                create_image_modal("image-click-6", "/assets/individual/air_quality/download.png",
                                   "This line chart illustrates the changes in PM2.5 concentrations over time across all counties. It helps identify long-term trends and seasonal spikes in air pollution levels.", "Air Quality Trends"),
                create_image_modal("image-click-7", "/assets/individual/air_quality/download-1.png",
                                   "A correlation heatmap that explores the relationships between different air quality variables. It highlights which pollutants or factors tend to rise and fall together, aiding in multivariate analysis.", "Air Quality Factors Correlation"),
                create_image_modal("image-click-8", "/assets/individual/air_quality/download-2.png",
                                   "A comparative bar chart showing average PM2.5 levels across different counties. This helps identify regions with consistently high or low pollution levels.", "Air Quality by County"),
                create_image_modal("image-click-9", "/assets/individual/air_quality/download-3.png",
                                   "Displays pollution levels by specific measurement sites, offering a more localized view of air quality that can reveal hotspot areas.", "Air Quality by Sites"),
                create_image_modal("image-click-10", "/assets/individual/air_quality/download-4.png",
                                   "This chart breaks down PM2.5 levels by hour of the day, revealing daily patterns and peak pollution times—useful for planning pollution control measures.", "Hourly Trends"),
                create_image_modal("image-click-11", "/assets/individual/air_quality/download-5.png",
                                   "A multi-year comparison of PM2.5 levels, showing how air quality has evolved annually. Useful for evaluating the impact of environmental regulations or policies.", "Yearly Comparison"),
                create_image_modal("image-click-12", "/assets/individual/air_quality/download-6.png",
                                   "A boxplot summarizing the distribution of PM2.5 levels in each county. It shows the median, spread, and outliers, making it easier to compare variability between regions.", "Boxplot Analysis"),
                create_image_modal("image-click-13", "/assets/individual/air_quality/download-7.png",
                                   "Displays the average PM2.5 concentration for each month, capturing seasonal effects such as winter spikes due to heating or traffic.", "Monthly PM2.5 Variation"),
            ]),
            html.Div(
                create_image_modal("image-click-14", "/assets/individual/air_quality/download-8.png",
                                   "A geographical visualization mapping PM2.5 levels across counties. This spatial perspective quickly highlights regional disparities and pollution hotspots.", "Air Quality by County"),
                style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'padding': '1%'
                }
            )
        ])


    elif dataset == 'ev_registration':
        return html.Div([
            html.P(
                "This dataset tracks electric vehicle registrations across regions and time, giving insights into "
                "adoption patterns and usage types.",
                style={'color': 'red', 'fontWeight': 'bold'}
            ),
            image_grid([
                create_image_modal("image-click-15", "/assets/individual/ev_registration/Counts Distribution by Primary Use Class (Log Scale).png",
                                   "This chart shows the distribution of electric vehicle registrations by primary use class (like private, commercial, etc.), using a logarithmic scale to accommodate a wide range of values. It highlights which categories dominate and which are emerging.", "EV Use Class (Log Scale)"),
                create_image_modal("image-click-16", "/assets/individual/ev_registration/Registration by primary use class.png",
                                   "A line or bar chart tracking the trend of EV registrations over time, providing insights into growth patterns, policy impact, and adoption rates across different time periods.", "EV Registration Trend"),
                create_image_modal("image-click-17", "/assets/individual/ev_registration/Top 10 counties by their total EV registration.png",
                                   "A bar chart displaying the top 10 counties with the highest total number of EV registrations. It highlights regional disparities in EV adoption and helps identify areas leading the transition to electric mobility.", "Top 10 Counties"),
                create_image_modal("image-click-18", "/assets/individual/ev_registration/Total number of EV Registrations during the time of year 2023-2025.png",
                                   "This time-based chart shows how EV registrations evolved specifically from 2023 to 2025, helping to assess recent trends and possibly correlate them with incentives, infrastructure developments, or policy changes during those years.", "Registrations 2023–2025")
            ])
        ])

    elif dataset == 'ev_station':
        return html.Div([
            html.P(
                "This dataset shows the growth, status, and distribution of EV charging stations over time and "
                "across different counties.",
                style={'color': 'red', 'fontWeight': 'bold'}
            ),
            image_grid([
                create_image_modal("image-click-19", "/assets/individual/ev_stations/EV_Station_Status_Distribution.png",
                                   "Displays the distribution of charging station statuses (e.g., active, inactive), helping assess infrastructure readiness.", "EV Station Status Distribution"),
                create_image_modal("image-click-20", "/assets/individual/ev_stations/number_of_ev_stations_per_county.png",
                                   "Shows how EV charging stations are geographically distributed across counties.", "EV Stations per County"),
                create_image_modal("image-click-21", "/assets/individual/ev_stations/Stations_Opened _Over_Time_(Top 5 Cities).png",
                                   "Tracks how the top 5 cities in EV infrastructure have grown over time based on station openings.", "Openings Over Time"),
                create_image_modal("image-click-22", "/assets/individual/ev_stations/stations_opened_by_month(all_years).png",
                                   "Analyzes seasonal trends in EV station launches by aggregating monthly data across all years.", "Monthly Openings"),
                create_image_modal("image-click-23", "/assets/individual/ev_stations/stations_opened_per_year.png",
                                   "Visualizes year-over-year growth in new EV charging station deployments.", "Stations Per Year"),
                create_image_modal("image-click-24", "/assets/individual/ev_stations/Status_Distribution_in_Top_and_Bottom_5_Cities.png",
                                   "Compares station status distribution between the top and bottom five cities in terms of EV infrastructure.", "Status in Top vs Bottom Cities")
            ]),
            html.Div(
                create_image_modal("image-click-25", "/assets/individual/ev_stations/top_5_vs_bottom_5_station_count.png",
                                   "Highlights disparities by comparing total station counts in top and bottom 5 cities.", "Top vs Bottom Cities"),
                style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'padding': '1%'
                }
            )
        ])


# ========== Register All Modal Callbacks ==========
image_ids = [
    "image-click-1", "image-click-2", "image-click-3", "image-click-4", "image-click-5",
    "image-click-6", "image-click-7", "image-click-8","image-click-9","image-click-10",
    "image-click-11", "image-click-12","image-click-13","image-click-14","image-click-15",
    "image-click-16", "image-click-17","image-click-18","image-click-19","image-click-20","image-click-21",
    "image-click-22","image-click-23","image-click-24","image-click-25"
]
register_modal_callbacks(app, image_ids)

# ========== Run App ==========
def stop_app_after_timer(seconds):
    time.sleep(seconds)
    print("Timer expired, stopping the app.")
    os._exit(0)

if __name__ == '__main__':
    threading.Thread(target=stop_app_after_timer, args=(600,)).start()
    app.run(debug=False, use_reloader=False)
