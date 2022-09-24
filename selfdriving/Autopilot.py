#Imports to get her working ;)

import numpy as np
import pandas as pd
import numpy as np
#Automation 
import pyautogui
from multiprocessing import Process
from pynput.keyboard import Key, Listener, KeyCode
import time 
import os
import random
import logging
#Time Series Machine Learning Based
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout  
from keras.models import Sequential 
import tensorflow as tf
from Vehicle_Class import Vehicle


#Load pretrained model

model = keras.models.load_model(os.getcwd() + '/StochasticLSTM.h5') #Make sure it's saved in same
                                                                   #directory

car = Vehicle(100, model)

car.numerical_integration_enabled = False
# car.listen()

time.sleep(3)
# car.autopilot() #Listen to your movements...
car.predict_keys(vertical=True)

