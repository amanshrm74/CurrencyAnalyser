import pandas as pd
import time, btcmodel
from datetime import date, timedelta
from model import build_model
import numpy as np

class BTCModel:
    # Change this value if you want to make longer/shorter prediction, i.e. number of days.
    pred_range, window_len = 1, 1

    def __init__(self):
        # Pull past data, starting from 01/01/2016 (Data is inconsistent before then) -> two days ago
        # Bitcoin market info: "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap". 
        btc_past = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20160101&end="+(date.today() - timedelta(2)).strftime("%Y%m%d"))[0] 
        # Convert the date string to the datetime format, "Volume" to an integer and rename columns.
        btc_past = btc_past.assign(Date=pd.to_datetime(btc_past['Date']))
        btc_past['Volume'] = btc_past['Volume'].astype('int64')
        btc_past.columns =[btc_past.columns[0]]+['bt_'+i for i in btc_past.columns[1:]]
        # Create "Supply" column, to display the circulating supply - i.e. the amount of bitcoins that currently exist. 
        # This is important as the supply or exclusivity should directly affect prices.
        for coins in ['bt_']: 
            kwargs = { coins+'Supply': lambda x: (x[coins+'Market Cap'])/(x[coins+'Close']) }
            btc_past = btc_past.assign(**kwargs)
        # Only keep columns "Close", "Volume", Supply".
        model_data = btc_past[['Date']+[coin+metric for coin in ['bt_'] 
            for metric in ['Close', 'Volume', 'Supply']]]
        # Reverse the data frame so that the row represent the right time frame. Remove "Date" column, since we are now finished with the dates.
        model_data = model_data.sort_values(by='Date')
        model_data = model_data.drop('Date', 1)
        # Prepare training inputs and outputs.
        LSTM_training_inputs = []
        for i in range(len(model_data)-self.window_len):
            temp_set = model_data[i:(i+self.window_len)].copy()
            LSTM_training_inputs.append(temp_set)
        LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
        LSTM_training_inputs = np.array(LSTM_training_inputs)
        LSTM_training_outputs = []
        for i in range(self.window_len, len(model_data['bt_Close'])-self.pred_range):
            LSTM_training_outputs.append((model_data['bt_Close'][i:i+self.pred_range].values/
                                        model_data['bt_Close'].values[i-self.window_len])-1)
        LSTM_training_outputs = np.array(LSTM_training_outputs)
        # Random seed for reproducibility.
        np.random.seed(202)
        # Initialise model architecture and train model with training set.
        self.bt_model = build_model(LSTM_training_inputs, output_size=self.pred_range, neurons = 20)
        self.bt_model.fit(LSTM_training_inputs[:-self.pred_range], LSTM_training_outputs, 
                                    epochs=25, batch_size=1, verbose=2, shuffle=True)
        self.prediction = None
   
    def predict(self, day):
        # Aquire and prepare data.
        btc_day = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="+day+"&end="+day)[0]
        btc_day = btc_day.assign(Date=pd.to_datetime(btc_day['Date']))
        btc_day['Volume'] = btc_day['Volume'].astype('int64')
        btc_day.columns =[btc_day.columns[0]]+['bt_'+i for i in btc_day.columns[1:]]
        for coins in ['bt_']: 
            kwargs = { coins+'Supply': lambda x: (x[coins+'Market Cap'])/(x[coins+'Close']) }
            btc_day = btc_day.assign(**kwargs)
        m_data = btc_day[[coin+metric for coin in ['bt_'] 
                                    for metric in ['Close', 'Volume', 'Supply']]]
        LSTM_predict_inputs = []
        for i in range(len(m_data)):
            temp_set = m_data[i:(i+self.window_len)].copy()
            LSTM_predict_inputs.append(temp_set)
        LSTM_predict_inputs = [np.array(LSTM_predict_inputs) for LSTM_predict_inputs in LSTM_predict_inputs]
        LSTM_predict_inputs = np.array(LSTM_predict_inputs)
        self.prediction = (self.bt_model.predict(LSTM_predict_inputs, batch_size=1)+1)*m_data['bt_Close'].values.reshape(1,1)

    def getPrediction(self):
        return self.prediction

btc = BTCModel()
btc.predict((date.today() - timedelta(2)).strftime("%Y%m%d"))
print(btc.getPrediction())

# Pull yesterday:
#   if not null (if it is not between 12am - 3am): 
#       predict   



# Wait till 3/4am

# Start day loop:

#   if not prevously predicted:
#       pull day before yesterday
#       predict

#   pull yesterday actual 
#   train with predict and yesterday actual

#   pull yesterday 
#   predict

"""
# Change this value if you want to make longer/shorter prediction, i.e. number of days.
pred_range, window_len = 1, 1

def create():
    # Pull past data, starting from 01/01/2016 (Data is inconsistent before then) -> two days ago
    # Bitcoin market info: "Date", "Open", "High", "Low", "Close", "Volume", "Market Cap". 
    btc_past = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20160101&end="+(date.today() - timedelta(2)).strftime("%Y%m%d"))[0] 
    # Convert the date string to the datetime format, "Volume" to an integer and rename columns.
    btc_past = btc_past.assign(Date=pd.to_datetime(btc_past['Date']))
    btc_past['Volume'] = btc_past['Volume'].astype('int64')
    btc_past.columns =[btc_past.columns[0]]+['bt_'+i for i in btc_past.columns[1:]]

    # Create "Supply" column, to display the circulating supply - i.e. the amount of bitcoins that currently exist. 
    # This is important as the supply or exclusivity should directly affect prices.
    for coins in ['bt_']: 
        kwargs = { coins+'Supply': lambda x: (x[coins+'Market Cap'])/(x[coins+'Close']) }
        btc_past = btc_past.assign(**kwargs)
    # Only keep columns "Close", "Volume", Supply".
    model_data = btc_past[['Date']+[coin+metric for coin in ['bt_'] 
        for metric in ['Close', 'Volume', 'Supply']]]
    # Reverse the data frame so that the row represent the right time frame. Remove "Date" column, since we are now finished with the dates.
    model_data = model_data.sort_values(by='Date')
    model_data = model_data.drop('Date', 1)

    # Prepare training inputs and outputs.
    LSTM_training_inputs = []
    for i in range(len(model_data)-window_len):
        temp_set = model_data[i:(i+window_len)].copy()
        LSTM_training_inputs.append(temp_set)
    LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
    LSTM_training_inputs = np.array(LSTM_training_inputs)

    LSTM_training_outputs = []
    for i in range(window_len, len(model_data['bt_Close'])-pred_range):
        LSTM_training_outputs.append((model_data['bt_Close'][i:i+pred_range].values/
                                    model_data['bt_Close'].values[i-window_len])-1)
    LSTM_training_outputs = np.array(LSTM_training_outputs)

    # Random seed for reproducibility.
    np.random.seed(202)
    # Initialise model architecture and train model with training set.
    bt_model = build_model(LSTM_training_inputs, output_size=pred_range, neurons = 20)
    bt_model.fit(LSTM_training_inputs[:-pred_range], LSTM_training_outputs, 
                                epochs=25, batch_size=1, verbose=2, shuffle=True)
    return bt_model

def predict(bt_model, day):
    # Aquire and prepare data.
    btc_day = pd.read_html("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start="+day+"&end="+day)[0]
    btc_day = btc_day.assign(Date=pd.to_datetime(btc_day['Date']))
    btc_day['Volume'] = btc_day['Volume'].astype('int64')
    btc_day.columns =[btc_day.columns[0]]+['bt_'+i for i in btc_day.columns[1:]]
    for coins in ['bt_']: 
        kwargs = { coins+'Supply': lambda x: (x[coins+'Market Cap'])/(x[coins+'Close']) }
        btc_day = btc_day.assign(**kwargs)
    m_data = btc_day[[coin+metric for coin in ['bt_'] 
                                   for metric in ['Close', 'Volume', 'Supply']]]
    LSTM_predict_inputs = []
    for i in range(len(m_data)):
        temp_set = m_data[i:(i+window_len)].copy()
        LSTM_predict_inputs.append(temp_set)
    LSTM_predict_inputs = [np.array(LSTM_predict_inputs) for LSTM_predict_inputs in LSTM_predict_inputs]
    LSTM_predict_inputs = np.array(LSTM_predict_inputs)
    return (bt_model.predict(LSTM_predict_inputs, batch_size=1)+1)*m_data['bt_Close'].values.reshape(1,1)

bt_model = create()
print(predict(bt_model, (date.today() - timedelta(2)).strftime("%Y%m%d")))
"""