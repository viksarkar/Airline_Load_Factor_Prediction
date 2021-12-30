# Airline_Load_Factor_Prediction
ML App to predict the load factor of flights on a specified route

The data used for this project will be T100 data from the Bureau of Transportation Statistics which can be downloaded [here](https://www.transtats.bts.gov/DL_SelectFields.asp?gnoyr_VQ=GDM&QO_fu146_anzr=Nv4%20Pn44vr45).
Given the effect of the COVID-19 pandemic on air travel, the data used is from 2017 through 2019. 

The data used is restricted to the following: 

    1. The carrier name
    2. The origin airport
    3. The destination airport
    4. The month of the year
    5. The airplane type
    6. The distance covered
    7. The number of departures scheduled

One hot encoding is used for categorical variables 1, 2, 3 and 5 above.The load factor is calculated as the ratio of #passengers to #available seats. This is expressed as a percentage used as the target for model training.

The model will be a Random Forest Regressor. A grid search was used to tune the hyper parameters (cross validated 3 times) and the model is then created. 
Testing the model on a test set representing 20% of the whole data set found the error to be on the order of 11% (MSE of 118). 

Streamlit is used to create an app that can be used with this model. The app is hosted on Heroku and can be found [here](). The screenshots below shows some of the functionality of the app. 
