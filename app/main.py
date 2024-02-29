import pandas as pd 
import plotly.express as px
from dash import dcc, Dash, Output, Input, html, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

df = pd.read_excel('data/Superstore.xls')
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

date_picker = html.Div([
        dmc.DatePicker(
            id='date-picker-start',
            label='Start Date',
            minDate=df['Order Date'].min(),
            maxDate=df['Order Date'].max(),
            value=df['Order Date'].min(),
            className='control'
        ),
        
        dmc.DatePicker(
            id='date-picker-end',
            label='End Date',
            minDate=df['Order Date'].min(),
            maxDate=df['Order Date'].max(),
            value=df['Order Date'].max(),
            className='control'
        ),
    ]
)

multi_sel_reg = html.Div([
    dmc.MultiSelect(
        id='multi-select-region',
        label='Region',
        data=df['Region'].unique(),
        className='control'
    )
])

multi_sel_category = html.Div([
    dmc.MultiSelect(
        id='multi-select-category',
        label='Category',
        data=df['Category'].unique(),
        className='control'
    )
])

app.layout = html.Div([
    html.Div(html.H1('Dashboard',
                     className='nav-text'),
             className='navbar'),
    dbc.Row([
        dbc.Col([
            html.H3('Filter',
                    className='text-filter'),
            dbc.Row([date_picker, multi_sel_reg, multi_sel_category])
            ], width=3, class_name='control-sec'),
        
        dbc.Col([
            dbc.Row([dbc.Col(dcc.Graph(id='line-chart-sales',), width=12, class_name='g-2 rounded-4')]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-chart-category'), width=8, class_name='g-2 rounded-4'),
                dbc.Col(dcc.Graph(id='pie-chart-category'), width=4, class_name='g-2 rounded-4')
                ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='pie-chart-subcat'), width=4, class_name='g-2 rounded-4'),
                dbc.Col(dcc.Graph(id='pie-chart-region'), width=4, class_name='g-2 rounded-4'),
                dbc.Col(dcc.Graph(id='pie-chart-segment'), width=4, class_name='g-2 rounded-4'),
                ]),
            dbc.Row(dbc.Col(dcc.Graph(id='treemap-plot'), class_name='g-2 rounded-4')),
            dbc.Row(dbc.Col(dcc.Graph(id='relation-chart-svp'), class_name='g-2 rounded-4'))
            ], width=9)
        ], class_name='body')
])

@app.callback(
    Output('line-chart-sales', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value'),
    Input('multi-select-category', 'value')
)
def line_chart_sales(start_date, end_date, region, category):
    
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    if category != None:
        filtered_df = filtered_df.loc[filtered_df['Category'].isin(category)]
    else:
        pass
    
    filtered_df['month_year'] = filtered_df['Order Date'].dt.to_period('M')
    linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"])["Sales"].sum()).reset_index()
    linechart['month_year'] = linechart['month_year'].dt.to_timestamp()
    linechart = linechart.sort_values(by='month_year')
    fig = px.line(linechart, x="month_year", y="Sales", 
                  labels={"Sales": "Amount"}, 
                  title= 'Sales Performance',
                  height=500,
                  template='plotly_white')
    
    return fig

@app.callback(
    Output('bar-chart-category', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value')
)
def bar_plot_categories(start_date, end_date, region):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    filtered_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()
    fig = px.bar(filtered_df, x = "Category", y = "Sales",
                 title='Total Sales by Category',
                 text = ['${:,.2f}'.format(x) for x in filtered_df["Sales"]],
                 template = "plotly_white")
    
    return fig

@app.callback(
    Output('pie-chart-category', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value')
)
def pie_plot_categories(start_date, end_date, region):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    fig = px.pie(filtered_df, values = "Sales",
                 title='Category Wise Sales',
                 names = "Category", template = "plotly_white", hole = 0.5)
    fig.update_traces(text = filtered_df["Category"], textposition = "outside")
    fig.update_layout(showlegend=False)
    
    return fig

@app.callback(
    Output('pie-chart-subcat', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value'),
    Input('multi-select-category', 'value')
)
def pie_plot_subcat(start_date, end_date, region, category):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    if category != None:
        filtered_df = filtered_df.loc[filtered_df['Category'].isin(category)]
    else:
        pass
    
    fig = px.pie(filtered_df, values = "Sales",
                 title='Sales of Goods',
                 names = "Sub-Category", template = "plotly_white", hole = 0.5)
    fig.update_traces(text = filtered_df["Sub-Category"], textposition = "outside")
    fig.update_layout(showlegend=False)
    
    return fig

@app.callback(
    Output('pie-chart-region', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-category', 'value')
)
def pie_plot_region(start_date, end_date, category):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
        
    if category != None:
        filtered_df = filtered_df.loc[filtered_df['Category'].isin(category)]
    else:
        pass
    
    fig = px.pie(filtered_df, values = "Sales",
                 title='Region Wise Sales',
                 names = "Region", hole = 0.5, template='plotly_white')
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    fig.update_layout(showlegend=False)
    
    return fig 

@app.callback(
    Output('pie-chart-segment', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value'),
    Input('multi-select-category', 'value')
)
def pie_plot_segment(start_date, end_date, region, category):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    if category != None:
        filtered_df = filtered_df.loc[filtered_df['Category'].isin(category)]
    else:
        pass
    
    fig = px.pie(filtered_df, values = "Sales",
                 title='Consumer Segmentation',
                 names = "Segment", hole = 0.5, template='plotly_white')
    fig.update_traces(text = filtered_df["Segment"], textposition = "outside")
    fig.update_layout(showlegend=False)
    
    return fig

@app.callback(
    Output('treemap-plot', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value'),
    Input('multi-select-category', 'value')
)
def treemap_plot(start_date, end_date, region, category):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    if category != None:
        filtered_df = filtered_df.loc[filtered_df['Category'].isin(category)]
    else:
        pass
    
    fig = px.treemap(filtered_df, path = ["Region","Category","Sub-Category"], values = "Sales",hover_data = ["Sales"],
                  color = "Sub-Category",
                  template='plotly_white')
    
    return fig

@app.callback(
    Output('relation-chart-svp', 'figure'),
    Input('date-picker-start', 'value'),
    Input('date-picker-end', 'value'),
    Input('multi-select-region', 'value'),
    Input('multi-select-category', 'value')
)
def relasion_chart(start_date, end_date, region, category):
    filtered_df = df.loc[(df['Order Date'] >= start_date) & (df['Order Date'] <= end_date)].copy()
    
    if region != None:
        filtered_df = filtered_df.loc[filtered_df['Region'].isin(region)]
    else:
        pass
    
    if category != None:
        filtered_df = filtered_df.loc[filtered_df['Category'].isin(category)]
    else:
        pass
    
    fig = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity", template='plotly_white')
    fig['layout'].update(title="Relationship between Sales and Profits",
                           titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
                           yaxis = dict(title = "Profit", titlefont = dict(size=19)))
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)