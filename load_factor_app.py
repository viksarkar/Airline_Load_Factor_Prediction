import streamlit as st
import pandas as pd
import numpy as np
import pickle
#import base64
#import seaborn as sns
#import plotly.graph_objects as go
import matplotlib.pyplot as plt
import datetime


st.write("""
## Airline Fullness (Load Factor) Prediction App
""")

def getflightdata(data, origin, destination, carrier, month):
    if carrier == 'No Selection':
        allcarrierdata = data[(data['ORIGIN']==origin) & (data['DEST']==destination) &\
                       (data['MONTH']==month)]
        singlecarrierdata = []
        numflights = allcarrierdata.shape[0]
        numcarriers = len(allcarrierdata['UNIQUE_CARRIER_NAME'].unique())
    else:
        allcarrierdata = data[(data['ORIGIN']==origin) & (data['DEST']==destination) &\
                       (data['MONTH']==month)]
        singlecarrierdata = allcarrierdata[allcarrierdata['UNIQUE_CARRIER_NAME']==carrier]
        numflights = singlecarrierdata.shape[0]
        numcarriers = 1
    return [allcarrierdata, singlecarrierdata, numflights, numcarriers]

Origins = pd.read_csv("Top_Airports.csv", header=None)
origin_choice = st.sidebar.selectbox('Select your Origin Airport:', Origins, index=76)
# st.write('Your Origin Airport is', origin_choice)

Destinations = pd.read_csv("Top_Airports.csv", header=None)
dest_choice = st.sidebar.selectbox('Select your Destination Airport:', Destinations, index=73)
# st.write('Your Destination Airport is', dest_choice)

months = ['January','February','March','April','May','June','July','August',\
          'September','October','November','December']
travel_month = st.sidebar.selectbox('Select your month of travel', months)
datetime_object = datetime.datetime.strptime(travel_month, "%B")
month_choice = datetime_object.month

Carriers = pd.read_csv("Top_Carriers.csv", header=None)
carrier_choice = st.sidebar.selectbox('Select your Carrier (OPTIONAL):', Carriers, index=0)
# if carrier_choice=='No Selection':
#     st.write('You did not select any carrier')
# else :
#     st.write('Your carrier is', carrier_choice)

data = pd.read_csv('All_Flights.csv')
[allcarrierdata, singlecarrierdata, numflights, numcarriers] = getflightdata(data, origin_choice, dest_choice, carrier_choice, month_choice)

if carrier_choice == 'No Selection':
    st.write('We have found', numflights, 'flights between', origin_choice,'and'\
             , dest_choice, 'on', numcarriers,'unique carriers for travel in',\
                 travel_month,'.')
else:
    st.write('We have found', numflights, 'flights between', origin_choice,'and'\
             , dest_choice, 'on', carrier_choice,'for travel in',travel_month,'.')

encoder = pickle.load(open('OneHotEncoder.pkl', 'rb'))
rfr = pickle.load(open('Load_Factor_SVR_Model.pkl', 'rb'))

if numflights > 0:
    if len(singlecarrierdata) == 0:
        X = encoder.transform(allcarrierdata)
        planetypes = pd.read_csv('L_AIRCRAFT_TYPE.csv')
        allcarrierdata = allcarrierdata.merge(planetypes,how='left',left_on='AIRCRAFT_TYPE',right_on='Code')
        allcarrierdata['Load Factor (%)'] = rfr.predict(X).astype(np.int64)
        allcarrierdata = allcarrierdata.rename(columns={"UNIQUE_CARRIER_NAME":"Carrier", "Description": "Aircraft Type", "DEPARTURES_SCHEDULED": "No. of Flights"})
        finaldata = allcarrierdata[['Carrier','Aircraft Type','No. of Flights','Load Factor (%)']]
        finaldata['No. of Flights'] = finaldata['No. of Flights'].astype(int)
        finaldata = finaldata.sort_values('Load Factor (%)', ascending=True)
        st.table(finaldata.assign(hack='').set_index('hack'))
    else:
        X = encoder.transform(singlecarrierdata)
        planetypes = pd.read_csv('L_AIRCRAFT_TYPE.csv')
        singlecarrierdata = singlecarrierdata.merge(planetypes,how='left',left_on='AIRCRAFT_TYPE',right_on='Code')
        singlecarrierdata['Load Factor (%)'] = rfr.predict(X).astype(np.int64)
        singlecarrierdata = singlecarrierdata.rename(columns={"UNIQUE_CARRIER_NAME":"Carrier", "Description": "Aircraft Type", "DEPARTURES_SCHEDULED": "No. of Flights"})
        finaldata = singlecarrierdata[['Carrier','Aircraft Type','No. of Flights','Load Factor (%)']]
        finaldata['No. of Flights'] = finaldata['No. of Flights'].astype(int)
        finaldata = finaldata.sort_values('Load Factor (%)', ascending=True)
        st.table(finaldata.assign(hack='').set_index('hack'))
    col1, col2 = st.columns(2)        
    image_hyperlink = 'http://www.gcmap.com/map?P='+origin_choice+'-'+dest_choice+'&MS=bm&MR=540&MX=540x540&PM=b:disc7%2b%22%25t%25+%28N%22'
    col1.image(image_hyperlink, width=400)
    col1.write('Map source : www.gcmap.com')       
else:
    image_hyperlink = 'http://www.gcmap.com/map?P='+origin_choice+'-'+dest_choice+'&MS=bm&MR=540&MX=540x540&PM=b:disc7%2b%22%25t%25+%28N%22'
    col1.image(image_hyperlink, use_column_width=True)
    col1.write('Map source : www.gcmap.com')       

# st.image(
#             "https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/6/2017/11/04133712/waterfall.jpg",
#             width=400, # Manually Adjust the width of the image as per requirement
#         )
