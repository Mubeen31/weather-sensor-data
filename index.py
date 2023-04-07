from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import pandas as pd
from datetime import datetime
from app import app
from tabContent.content_tab_one import tab_one
from tabContent.content_tab_two import tab_two
from tabContent.content_tab_three import tab_three
from tabContent.content_tab_four import tab_four
import dash_bootstrap_components as dbc
import dash_daq as daq

server = app.server

tab_style = {
    'height': '35px',
    'width': 'auto',
    'padding': '7.5px',
    'border-top': 'none',
    'border-bottom': 'none',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)'
}

selected_tab_style = {
    'height': '35px',
    'width': 'auto',
    'padding': '7.5px',
    'border-top': 'none',
    'border-bottom': '2px solid blue',
    'border-left': 'none',
    'border-right': 'none',
    'backgroundColor': 'rgba(255, 255, 255, 0)',
    'fontWeight': 'bold'
}

tab_one_chart = html.Div([
    html.Div([
        dcc.Graph(id='line_chart1',
                  config={'displayModeBar': False}),
        html.Div([
            daq.BooleanSwitch(id='line_color',
                              on=True,
                              color="#9B51E0",
                              label='Line color',
                              labelPosition='top'
                              ),
            daq.BooleanSwitch(id='last_values',
                              on=True,
                              color="#FF5E5E",
                              label='Select last values',
                              labelPosition='top'
                              )
        ], className='button_row')
    ], className='tab_page'),
], className='tab_content_row')
tab_two_chart = html.Div([
    html.Div([
        dcc.Graph(id='line_chart2',
                  config={'displayModeBar': False})
    ], className='tab_page')
], className='tab_content_row')
tab_three_chart = html.Div([
    html.Div([
        dcc.Graph(id='line_chart3',
                  config={'displayModeBar': False})
    ], className='tab_page')
], className='tab_content_row')
tab_four_chart = html.Div([
    html.Div([
        dcc.Graph(id='line_chart4',
                  config={'displayModeBar': False})
    ], className='tab_page')
], className='tab_content_row')

app.layout = html.Div([

    dcc.Interval(id='update_value',
                 interval=1 * 16000,
                 n_intervals=0),

    html.Div([
        html.Div([

            html.Div([
                html.Img(src=app.get_asset_url('real-time.png'),
                         className='image'),
                html.Div('Real Time Data Visualizations and Analysis',
                         className='title_text')
            ], className='title_image_row'),

            html.Div([
                html.Div('Sensor location:'),
                html.Div('Walsall, England', className='location_name')
            ], className='location_row'),

            dbc.Spinner(html.Div(id='data_update_time'))

        ], className='title_background twelve columns')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div(id='temp', className='card_bg'),
            html.Div(id='hum', className='card_bg'),
            html.Div(id='light_intensity', className='card_bg'),
            html.Div(id='co2', className='card_bg'),
        ], className='temp_humidity')
    ], className='display_center_row'),

    html.Div([
        html.Div([
            dcc.Tabs(id='tabs', value='tab_content_one', children=[
                dcc.Tab(tab_one_chart,
                        label='Real Time',
                        value='tab_content_one',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(tab_two_chart,
                        label='Humidity',
                        value='tab_content_two',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(tab_three_chart,
                        label='Hourly',
                        value='tab_content_three',
                        style=tab_style,
                        selected_style=selected_tab_style),
                dcc.Tab(tab_four_chart,
                        label='Light Intensity',
                        value='tab_content_four',
                        style=tab_style,
                        selected_style=selected_tab_style)
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], className='tabs_container')
    ], className='display_center_row'),

    # html.Div(id='return_tab_content', children=[])

])


@app.callback(Output('data_update_time', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/1/last.csv'
    df = pd.read_csv(url)
    date_time = df['created_at'].iloc[0]
    get_date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ')
    last_date_time = get_date_time.strftime('%Y-%m-%d %H:%M:%S')

    return [
        html.Div([
            html.Div('Last data update time:'),
            html.Div(last_date_time, className='location_name')
        ], className='date_time_row')
    ]


@app.callback(Output('temp', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/2/last.csv'
    df = pd.read_csv(url)
    df_temp = df['field2'].iloc[0]

    return [
        html.Div([
            html.P('Temperature', style={'color': '#666666'}),
            html.Div([
                html.Img(src=app.get_asset_url('hot.png'),
                         style={'height': '50px'}),
                html.Div([
                    html.Div('°C', className='symbol'),
                    html.Div('{0:.1f}'.format(df_temp),
                             className='numeric_value')
                ], className='temp_symbol_column')
            ], className='temp_image_row')
        ], className='title_card_column')
    ]


@app.callback(Output('hum', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/1/last.csv'
    df = pd.read_csv(url)
    df_hum = df['field1'].iloc[0]

    return [
        html.Div([
            html.P('Humidity', style={'color': '#666666'}),
            html.Div([
                html.Img(src=app.get_asset_url('humidity.png'),
                         style={'height': '50px'}),
                html.Div([
                    html.Div('%', className='symbol'),
                    html.Div('{0:.1f}'.format(df_hum),
                             className='numeric_value')
                ], className='temp_symbol_column')
            ], className='temp_image_row'),

        ], className='title_card_column')
    ]


@app.callback(Output('light_intensity', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/3/last.csv'
    df = pd.read_csv(url)
    df_light_inten = df['field3'].iloc[0]

    return [
        html.Div([
            html.P('Light Intensity', style={'color': '#666666'}),
            html.Div([
                html.Img(src=app.get_asset_url('sunny.png'),
                         style={'height': '50px'}),
                html.Div([
                    html.Div('lux', className='symbol'),
                    html.Div('{0:.0f}'.format(df_light_inten),
                             className='numeric_value')
                ], className='temp_symbol_column')
            ], className='temp_image_row'),

        ], className='title_card_column')
    ]


@app.callback(Output('co2', 'children'),
              [Input('update_value', 'n_intervals')])
def update_value(n_intervals):
    url = 'https://api.thingspeak.com/channels/2007583/fields/4/last.csv'
    df = pd.read_csv(url)
    df_co2 = df['field4'].iloc[0]

    return [
        html.Div([
            html.P('CO2 Level in Air', style={'color': '#666666'}),
            html.Div([
                html.Img(src=app.get_asset_url('co2.png'),
                         style={'height': '50px'}),
                html.Div([
                    html.Div('ppm', className='symbol'),
                    html.Div('{0:.0f}'.format(df_co2),
                             className='numeric_value')
                ], className='temp_symbol_column')
            ], className='temp_image_row'),

        ], className='title_card_column')
    ]


@app.callback(Output('line_chart1', 'figure'),
              [Input('update_value', 'n_intervals')],
              [Input('line_color', 'on')],
              [Input('last_values', 'on')])
def tab_one_callback(n_intervals, line_color, last_values):
    tab_one_data = tab_one(n_intervals, line_color, last_values)

    return tab_one_data


@app.callback(Output('line_chart2', 'figure'),
              [Input('update_value', 'n_intervals')])
def tab_two_callback(n_intervals):
    tab_two_data = tab_two(n_intervals)

    return tab_two_data


@app.callback(Output('line_chart3', 'figure'),
              [Input('update_value', 'n_intervals')])
def tab_three_callback(n_intervals):
    tab_three_data = tab_three(n_intervals)

    return tab_three_data


@app.callback(Output('line_chart4', 'figure'),
              [Input('update_value', 'n_intervals')])
def tab_four_callback(n_intervals):
    tab_four_data = tab_four(n_intervals)

    return tab_four_data


if __name__ == '__main__':
    app.run_server(debug=True)
