import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import base64
import io
from sklearn.preprocessing import LabelEncoder

# Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([  
    # Header Section
    dbc.Row([ 
        # Logo
        dbc.Col(html.Img(src="https://iac.edu.pk/wp-content/uploads/2024/02/logo.png", height="80px"), width=2),

        # Title
        dbc.Col(html.H1("AI Traffic Congestion Analysis", className="text-center"), width=8),

        # Buttons
        dbc.Col([
            html.A(
                dbc.Button(
                    "Dashboard", 
                    className="mx-1 btn-hover", 
                    style={
                        "width": "100px",
                        "backgroundColor": "#ff0000",  
                        "color": "white",
                        "fontWeight": "600",
                        "border": "none"
                    }
                ),
                href="https://iac.edu.pk/",
                target="_blank"
            ),
            html.A(
                dbc.Button(
                    "Contact Us", 
                    color="success", 
                    className="mx-1 btn-hover", 
                    style={"width": "120px", "fontWeight": "600"}
                ),
                href="https://iac.edu.pk/contact-us/",
                target="_blank"
            ),
        ], width=2, className="d-flex align-items-center justify-content-end"),
    ], align="center"),

    # Horizontal Line (Three Colors)
    html.Div(style={
        "width": "100%",
        "height": "5px",
        "background": "linear-gradient(to right, red, yellow, green)",
        "marginBottom": "20px"
    }),

    # Team Members and Upload Section in a Single Row
    dbc.Row([
        # Team Members Section
        dbc.Col([
            html.H4("Project Team Members"),
            html.Ul([
                html.Li("1. Falak"),
                html.Li("2. Amber"),
                html.Li("3. Tazeem"),
                html.Li("4. Suleman")
            ])
        ], width=6, style={"paddingLeft": "60px"}),

        # Upload Section
        dbc.Col([
            html.H4("Upload Your CSV File", className="text-center", style={"paddingBottom": "25px"}),  
            dcc.Upload(
                id="upload-data",
                children=html.Div(["Drag and Drop or ", html.A("Select a CSV File")]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "marginBottom": "20px",
                },
            )
        ], width=6, style={"paddingRight": "60px"}),
    ], className="mb-4"),

    # CSV Requirements, Benefits, and Graph Details in One Row
    dbc.Row([
        dbc.Col([
            html.H4("CSV File Requirements", style={"color": "red", "paddingLeft": "30px"}),  
            html.Ul([
                html.Li("Timestamp - Datetime"),
                html.Li("Location - String"),
                html.Li("Vehicle_count - Integer"),
                html.Li("Country_city - String")
            ])
        ], width=4),
        dbc.Col([
            html.H4("Benefits of Using This Analysis", style={"color": "#ffeb00", "paddingLeft": "30px"}),  
            html.Ul([
                html.Li("Identifies high-congestion areas for better urban planning."),
                html.Li("Predicts traffic trends to optimize commute times."),
                html.Li("Helps reduce fuel consumption and emissions."),
                html.Li("Supports efficient emergency and logistics routing.")
            ])
        ], width=4),
        dbc.Col([
            html.H4("Traffic Graph Details", style={"color": "green", "paddingLeft": "30px"}),  
            html.Ul([
                html.Li("Scatter Map: Shows traffic locations and congestion levels across the city."),
                html.Li("Line Chart: Displays trends in vehicle counts over time at different locations."),
                html.Li("Bar Chart: Highlights average vehicle counts by location for identifying hotspots.")
            ])
        ], width=4),
    ], className="mb-4"),

    # Output Section
    html.Div(id="output-data-upload"),
], fluid=True)

# Helper Functions
def parse_data(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume CSV format
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            return df
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None
    return None

# Approximate location data for locations in London (lat, lon)
location_coordinates = {
    'Westminster': (51.4974, -0.1278),
    'Camden': (51.5292, -0.1426),
    'Islington': (51.5364, -0.1037),
    'Kensington': (51.4974, -0.1925),
    'Hackney': (51.5471, -0.0464),
    'Bromley': (51.4052, 0.0167),
    'Greenwich': (51.4769, 0.0005),
    'Croydon': (51.3760, -0.0980),
    'Brent': (51.5583, -0.2817),
    'Tower Hamlets': (51.5074, -0.0290)
}

# Callback to handle uploaded data
@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    Input("upload-data", "filename")
)
def update_output(contents, filename):
    if contents is None:
        return html.Div()

    # Parse the file
    df = parse_data(contents, filename)

    if df is None:
        return html.Div("Invalid file format. Please upload a valid CSV.")

    # Display summary table using describe() method
    field_details = html.Div([
        html.H4("Uploaded Data Summary", className="my-3"),
        dash_table.DataTable(
            data=df.describe().reset_index().to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.describe().reset_index().columns],
            style_table={"overflowX": "auto"},
            style_header={"backgroundColor": "rgb(30, 30, 30)", "color": "white"},
            style_cell={"textAlign": "center", "padding": "10px"}
        )
    ])

    # Handle missing values
    df.fillna(method="ffill", inplace=True)

    # Ensure timestamp is in datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)

    # Label encoding for categorical columns
    if "location" in df.columns:
        df["location_encoded"] = LabelEncoder().fit_transform(df["location"])

    # Get latitude and longitude from location names
    latitudes = []
    longitudes = []
    for location in df['location']:
        if location in location_coordinates:
            latitudes.append(location_coordinates[location][0])
            longitudes.append(location_coordinates[location][1])
        else:
            latitudes.append(51.5074)  # Default to central London
            longitudes.append(-0.1278)  # Default to central London

    # Add latitudes and longitudes to the DataFrame
    df['latitude'] = latitudes
    df['longitude'] = longitudes

    # Calculate the statistics for the first 50 rows
    df_top_50 = df.head(50)
    location_stats = df_top_50.groupby('location')['vehicle_count'].agg(['max', 'median']).reset_index()

    # Categorize the locations based on max vehicle count
    max_value = location_stats['max'].max()
    min_value = location_stats['max'].min()
    median_value = location_stats['max'].median()

    def categorize(row):
        if row['max'] == max_value:
            return 'High'
        elif row['max'] == median_value:
            return 'Medium'
        else:
            return 'Low'

    location_stats['category'] = location_stats.apply(categorize, axis=1)

    # Horizontal Bar Chart for Locations Categorized by Vehicle Count
    fig_location_category = px.bar(
        location_stats,
        x='max',
        y='location',
        color='category',
        orientation='h',
        title="Location Congestion Areas  ",
        labels={"max": "Max Vehicle Count", "location": "Location"},
        color_discrete_map={"High": "red", "Medium": "yellow", "Low": "green"}
    )

    # Visualizations
    try:
        fig_map = px.scatter_mapbox(
            df,
            lat="latitude",
            lon="longitude",
            size="vehicle_count",
            color="location",
            title="Traffic Locations",
            mapbox_style="open-street-map",
            zoom=10,
        )
        fig_map.update_layout(
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            height=500
        )

        fig_trend = px.line(
            df, x="timestamp", y="vehicle_count", color="location",
            title="Traffic Trends Over Time",
            markers=True
        )
        fig_trend.update_traces(line=dict(width=2.5))
        fig_trend.update_layout(hovermode="x unified", height=500)

        fig_bar = px.bar(
            df.groupby("location")["vehicle_count"].mean().reset_index(),
            x="location",
            y="vehicle_count",
            color="location",
            title="Average Vehicle Count per Location",
            text_auto=True
        )
        fig_bar.update_traces(marker=dict(line=dict(width=2, color="black")))

    except Exception as e:
        return html.Div(f"Error generating graphs: {e}")

    return html.Div([
        field_details,
        html.H4("Visualizations", className="my-4 text-center"),
        dcc.Graph(figure=fig_map),
        dcc.Graph(figure=fig_trend),
        dcc.Graph(figure=fig_bar),
        html.H4("Prediction of Traffic Trends", className="my-4 text-center"),
        dcc.Graph(figure=fig_location_category),
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
