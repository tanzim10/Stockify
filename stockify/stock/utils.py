import requests
import json
import yfinance as yf
import math
import numpy as np
import pandas as pd
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta,date
import base64
from io import BytesIO




def stock_fetch_api(symbols):
    stock_data = {}
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period='1d')
        stock_data[symbol] = data.to_dict(orient='list')
    
    datas ={}
    for key,val in stock_data.items():
        datas[key] =[]
        for stk,price in val.items():
            price = round(price[0],3)
            datas[key].append(price)
   
    return datas

def unit_price_fetch(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    data = data.to_dict(orient='records')
    unit_price = round(data[0]['Open'],5)
    return unit_price

def get_predictions(symbol,date_end):

    start_date = '2012-01-01'
    end_date = date_end

    # Get the stock quote
    df = yf.download(symbol, start=start_date, end=end_date)
    

    #Create a new Dataframe with only 'Close' column
    data = df.filter(['Close'])
    #Convert the dataframe to a numpy array
    dataset = data.values
    #Get the number of rows to train the model on
    training_data_len = math.ceil(len(dataset) *0.80)
    #print(data.shape)
    #print(training_data_len)
    # Scaling the data in between the range(0,1)

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)
    #print(scaled_data)

    #Create training data set
    # Create the scaled trained dataset
    train_data = scaled_data[0:training_data_len, :]
    #Split the data into x_train and y_train datasets
    x_train = []
    y_train = []
    for i in range(60,len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i,0])
        if i<=60:
            #print(x_train)
            #print(y_train)
            print()

    #Convert the x_train and y_train to numpy arrays 
    x_train , y_train = np.array(x_train), np.array(y_train) # type: ignore
    #Reshape the data
    x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
    #print(x_train.shape)

    #Build the LSTM Model
    model = Sequential()
    model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
    model.add(LSTM(50,return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss ='mean_squared_error')

    #Train the model
    model.fit(x_train,y_train, batch_size =1, epochs =1)

    #Create testing data set
    #Create a new array containing scaled values from index 1543-2002
    test_data = scaled_data[training_data_len -60: , : ]
    #Create the dataset x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, : ]
    for i in range(60,len(test_data)):
        x_test.append(test_data[i-60:i,0])

    #Convert the data to a numpy array
    x_test = np.array(x_test)

    #Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

    #Get the models predicted proce values 
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions) #Unscaling the value

    #Plot the data
    train =data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions


    new_df = df.filter(['Close'])
    last_60_days = new_df[-60:].values
    # Scale the data to be values between 0 and 1
    last_60_days_scaled = scaler.transform(last_60_days)
    #Create an empty list
    X_test = []
    #Append the last 60 days
    X_test.append(last_60_days_scaled)
    #Conver the X_test dataset to a numpy array
    X_test = np.array(X_test)
    # Reshape the data
    X_test = np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
    # Get the predicted scale price
    pred_price = model.predict(X_test)
    #undo the scaling
    pred_price = scaler.inverse_transform(pred_price)

    return valid,train, pred_price

def get_dates(end_dates):
    date_format = "%Y-%m-%d"
    datetime_obj = datetime.strptime(end_dates, date_format)
    start_date = date(2012, 1, 1)
    end_date = datetime_obj.date()

    current_date = start_date
    years = []

    while current_date <= end_date:
        years.append(current_date.year)
        current_date += timedelta(days=1)

    return years

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format ='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()

    return graph

def get_plot(valid,train):
    plt.switch_backend('AGG')
    plt.figure(figsize=(15,6))
    plt.title('Model')
    plt.xlabel('Date', fontsize = 18)
    plt.ylabel('Close Price USD $')
    plt.plot(train['Close'])
    plt.plot(valid[['Close','Predictions']])
    plt.xticks(rotation =45)
    plt.legend(['Train','Val','Predictions'], loc ='upper right')
    plt.tight_layout()
    graph = get_graph()

    return graph

def pred_date(end_date):

    date_format = "%Y-%m-%d"
    date_obj = datetime.strptime(end_date, date_format)
    next_date = date_obj + timedelta(days=1)
    next_date_string = next_date.strftime(date_format)

    return next_date_string










    


