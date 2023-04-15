from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
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
        html.Div([
            dcc.Graph(id='line_chart3',
                      config={'displayModeBar': False})
        ], className='tab_page'),
        html.Img(id='tooltip_chart',
                 n_clicks=0,
                 src='/assets/tooltip.png',
                 className='info_image'),
    ], className='card_info_image'),
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
            html.Div([
                html.Div(id='temp', className='card_bg'),
                html.Img(id='modal_temp',
                         n_clicks=0,
                         src='/assets/info.png',
                         className='info_image'),
            ], className='card_info_image'),
            html.Div([
                html.Div(id='hum', className='card_bg'),
                html.Img(id='modal_hum',
                         n_clicks=0,
                         src='/assets/info.png',
                         className='info_image'),
            ], className='card_info_image'),
            html.Div([
                html.Div(id='light_intensity', className='card_bg'),
                html.Img(id='modal_light_intensity',
                         n_clicks=0,
                         src='/assets/info.png',
                         className='info_image'),
            ], className='card_info_image'),
            html.Div([
                html.Div(id='co2', className='card_bg'),
                html.Img(id='modal_co2',
                         n_clicks=0,
                         src='/assets/info.png',
                         className='info_image'),
            ], className='card_info_image'),
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

    # Modal temperature
    dbc.Modal([
        dbc.ModalBody(
            html.Div([
                html.P(dcc.Markdown('''
            As the DHT 22 sensor is inside the plastic container and hanged outside the window, this saves 
            the sensor from external weather factor but the plastic container acts like a **greenhouse.** 
            Despite the holes on the bottom side of the plastic container, some heat remains trapped 
            inside, causing the high temperature.
            '''), style={'text-align': 'justify'}),
                html.P(dcc.Markdown('''
            As a result of external factors, this card shows 
            the wrong temperature value on a sunny day. An **accurate** value can be observed on this 
            **card** even on a **cloudy day or at night**.
            '''), style={'text-align': 'justify'})
            ])
        ),
        dbc.ModalFooter(dbc.Button("Close",
                                   id="close_temp_info",
                                   className="ms-auto",
                                   n_clicks=0))
    ], id="modal_temp_info",
        centered=True,
        is_open=False,
        size="lg"),
    # Modal temperature

    # Modal humidity
    dbc.Modal([
        dbc.ModalBody(
            html.P(dcc.Markdown('''
            The **humidity** value is also affected by external factors. On a **sunny day**, there is an abrupt 
            decrease in humidity value. An accurate humidity measurement can also be observed **at night or 
            on a cloudy day**.
            '''), style={'text-align': 'justify'})
        ),
        dbc.ModalFooter(dbc.Button("Close",
                                   id="close_hum_info",
                                   className="ms-auto",
                                   n_clicks=0))
    ], id="modal_hum_info",
        centered=True,
        is_open=False,
        size="lg"),
    # Modal humidity

    # Modal light intensity
    dbc.Modal([
        dbc.ModalBody(
            html.P(dcc.Markdown('''
           The light dependent resistor **(LDR)** measures an accurate value on a daytime basis. At night, 
           **street light or room light** falls on this sensor, causing the small amount of light intensity. 
           It is also inside the same container and hangs outside the window.
           '''), style={'text-align': 'justify'})
        ),
        dbc.ModalFooter(dbc.Button("Close",
                                   id="close_light_intensity_info",
                                   className="ms-auto",
                                   n_clicks=0))
    ], id="modal_light_intensity_info",
        centered=True,
        is_open=False,
        size="lg"),
    # Modal light intensity

    # Modal co2
    dbc.Modal([
        dbc.ModalBody(
            html.P(dcc.Markdown('''
           The **MQ 135 gas sensor** is not connected to the microcontroller because I am using a 
           microcontroller with only one **analog pin**. This card displays only **zero values** as a result. 
           A microcontroller with **more than one analog pin** is required to measure **CO2 levels** 
           in the air.
           '''), style={'text-align': 'justify'})
        ),
        dbc.ModalFooter(dbc.Button("Close",
                                   id="close_co2_info",
                                   className="ms-auto",
                                   n_clicks=0))
    ], id="modal_co2_info",
        centered=True,
        is_open=False,
        size="lg"),
    # Modal co2

    # Tooltip chart
    dbc.Modal([
        dbc.ModalBody(
            html.P(dcc.Markdown('''
           Some hours of **yesterday's values** are skipped at the end of the day. There is a reason for this: the 
           thing speak cloud can only read the **last 8000 values** in a day. Therefore, some of yesterday's hours 
           are missing, while all of **today's hours** are displayed.
           '''), style={'text-align': 'justify'})
        ),
        dbc.ModalFooter(dbc.Button("Close",
                                   id="close_chart_info",
                                   className="ms-auto",
                                   n_clicks=0))
    ], id="modal_chart_info",
        centered=True,
        is_open=False,
        size="lg")
    # Tooltip chart

])


@app.callback(
    Output("modal_temp_info", "is_open"),
    [Input("modal_temp", "n_clicks")],
    [Input("close_temp_info", "n_clicks")],
    [State("modal_temp_info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal_hum_info", "is_open"),
    [Input("modal_hum", "n_clicks")],
    [Input("close_hum_info", "n_clicks")],
    [State("modal_hum_info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal_light_intensity_info", "is_open"),
    [Input("modal_light_intensity", "n_clicks")],
    [Input("close_light_intensity_info", "n_clicks")],
    [State("modal_light_intensity_info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal_co2_info", "is_open"),
    [Input("modal_co2", "n_clicks")],
    [Input("close_co2_info", "n_clicks")],
    [State("modal_co2_info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("modal_chart_info", "is_open"),
    [Input("tooltip_chart", "n_clicks")],
    [Input("close_chart_info", "n_clicks")],
    [State("modal_chart_info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


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
