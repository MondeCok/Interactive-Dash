import pandas as pd 
import dash 
import plotly.express as px
from dash import dcc, Dash, Output, Input, html, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

df = pd.read_excel('Superstore.xls')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

date_picker = html.Div([
        dmc.DatePicker(
            id="date-picker-start",
            label="Start Date",
            minDate=df['Order Date'].min(),
            maxDate=df['Order Date'].max(),
            value=df['Order Date'].min(),
            style={"width": 200},
        ),
        
        dmc.DatePicker(
            id="date-picker-end",
            label="End Date",
            minDate=df['Order Date'].min(),
            maxDate=df['Order Date'].max(),
            value=df['Order Date'].max(),
            style={"width": 200},
        ),
    ]
)

multi_sel_region = html.Div([
    dmc.MultiSelect(
        id='multi-select-region',
        label='Region',
        data=df['Region'].unique(),
        style={"width": 250, "marginBottom": 10},
    )
])

multi_sel_category = html.Div([
    dmc.MultiSelect(
        id='multi-select-category',
        label='Category',
        data=df['Category'].unique(),
        style={"width": 250, "marginBottom": 10},
    )
])