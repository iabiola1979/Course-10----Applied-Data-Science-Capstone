# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 17:20:00 2025

@author: iabio
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import plotly 

# Import required libraries
import dash
from dash import Dash, dcc, html, Input, Output
#import dash_html_components as html
#import dash_core_components as dcc
#from dash.dependencies import Input, Output
import plotly.express as px








url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
df = pd.read_csv(url)


cols = list(df.columns)
cols



#### F9 booster Launch success rate
a = df.groupby('Booster Version Category')['class'].count()

b = df.groupby('Booster Version Category')['class'].sum()

c = b/a

#### Launch site success rate
a1 = df.groupby('Launch Site')['class'].count()

b1 = df.groupby('Launch Site')['class'].sum()

c1 = b1/a1








# Read the airline data into pandas dataframe
spacex_df = df # pd.read_csv("spacex_launch_dash.csv")
spacex_df['success'] = spacex_df['class']
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()




# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(children=[html.H2("Select Launch Site:", style={'textAlign': 'left', 'color': '#503D36','font-size': 25}),
                                                   dcc.Dropdown(options=['ALL Sites', 'CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS SLC-40'], \
                                                                placeholder = 'Select a Launch Site here',
                                                                value='ALL Sites', id='site-dropdown',
                                                                searchable=True)]),
                                html.Br(),
                                
  
                                   

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph( id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                
                                html.Div(dcc.RangeSlider(id='payload-range-slider', min=0, max=10000, step = 1000, \
                                                         marks ={0:'0', 100: '100',500:'500', 1000:'1000', 1500:'1500',  
                                                                 2500 :'2500', 5000:'5000', 7500:'7500', 9000:'9000', 10000:'10000'}, 
                                                         value =[0,10000])),                           
                                
                                
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'), \
              Input(component_id  = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site):
 
        if entered_site=='ALL Sites':
            filtered_df = spacex_df
            fig = px.pie(data_frame=filtered_df, values='class', names ='Launch Site', \
                         title = "Distribution by Launch Sites")
        
        
        else:
            filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
            grp_data = filtered_df.groupby('class')['success'].count().reset_index()

            fig = px.pie(data_frame=grp_data, values='success', names ='class', \
                         title = "Total Succes Launches for site {}".format(entered_site))
            
        return fig 
 

   
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'), \
              Input(component_id  = 'site-dropdown', component_property = 'value'),
              Input(component_id  = 'payload-range-slider', component_property = 'value'))
    

def get_scatter_chart(entered_site, slider_input):
 
        if entered_site=='ALL Sites':
            filtered_df = spacex_df
            fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color = 'Booster Version Category', \
                         title = "Success-Payload Relationships")
        
        
        else:
            filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
            fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color = 'Booster Version Category', \
                         title = "Success-Payload Relationship at Launch site {}".format(entered_site))
            
        return fig 
 
    
    
    




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
    
    
    
    
    
    
    
    