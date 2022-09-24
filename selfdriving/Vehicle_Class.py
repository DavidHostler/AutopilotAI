#Automation
import pyautogui
from multiprocessing import Process
from pynput.keyboard import Key, Listener, KeyCode
import time 
import os
import random
import logging
import numpy as np

class Vehicle:
    
    def __init__(self, memory_window_size, model):
        self.latest_vx = 0.0
        self.latest_vy = 0.0 #2D velocity components
        '''In order to have up-to-data training data, the two arrays must be QUEUES.
        The oldest information needs to be forgotten first, so pop from the front of each every time
        a new value is added to the velocity data for the graph.
        
        #Assumption is that by cumulatively adding increments of the acceleration with each keypress,
        the sum in the onPress function effectively numerically integrates the acceleration wrt time,
        i,e. += 1.0 * alpha, our incremental change in time (although we should adjust this by finding differences
        in Unix time!)
        
        
        '''
        self.model = None
        self.key = None
        self.history = None
        self.vx = [] #Update this parameter with new values each time
        self.vy = []
        self.x_predicted, self.y_predicted = [], []
        
        
        self.memory_window_size = memory_window_size
        
        self.X_horizontal, self.y_horizontal = [0] * memory_window_size , [0] * memory_window_size
        self.X_vertical, self.y_vertical  = [0] * memory_window_size , [0] * memory_window_size

        
        
        self.time_elapsed = 0.0
        
        self.numerical_integration_enabled = True
        
        
    def onPress(self,key):
        numerical_integration_enabled= self.numerical_integration_enabled
        w = KeyCode.from_char("w")
        s = KeyCode.from_char("s")
        d = KeyCode.from_char("d")
        a = KeyCode.from_char("a")
        p = KeyCode.from_char("p")
        logging.info(str(key))
        self.key = key #Store this value in the data structure to get 
        if self.numerical_integration_enabled is True:
            alpha = time.time()
        else:
            alpha = 0.1 #If numerical integration is not enabled, keep timestep constant 
        if key == Key.esc:
            print(self.latest_vy)
            return False
        elif key == p:
            print("autopilot is activated")
            # self.autopilot()
        elif key == w:
            #Perform numerical integration over each timestep 
            if self.numerical_integration_enabled is True:
                alpha -= time.time()                         #Calculate the timestep after the keypress is detected
            self.latest_vy += 1.0 * alpha#Accelerate
            self.vy.append(self.latest_vy)
            
            self.vx.append(self.latest_vx)
        elif key == s:
            if self.numerical_integration_enabled is True:
                alpha -= time.time() 

            self.latest_vy -= 1.0 * alpha#Decelerate
            self.vy.append(self.latest_vy)
            
            self.vx.append(self.latest_vx)
            
        elif key == d:
            if self.numerical_integration_enabled is True:
                alpha -= time.time() 

            self.latest_vx += 1.0 * alpha#Turn right
            self.vx.append(self.latest_vx)
            
            self.vy.append(self.latest_vy)
            
        elif key == a:
            if self.numerical_integration_enabled is True:
                alpha -= time.time()             
            self.latest_vx -= 1.0 * alpha#Turn left!
            self.vx.append(self.latest_vx)
            
            self.vy.append(self.latest_vy) #If the horizontal keys are pressed, 
                                           #assume that from Newton's 1st law (given ~0 friction force for now) 
                                           #that motion of the vehicle in the other coordinate remains constant.
                                           #We'll dampen this with friction data later!
            
        else:
            pass
#         print(alpha)
        print(self.latest_vx, self.latest_vy)

        #if key == Key.esc:
        # return false
    def listen(self):
        with Listener(on_press = self.onPress) as listener:
            listener.join() 
 
    
    def gaussian_noise(self, value, num_noise_pts=100):
        sigma = 0.2
        return np.random.normal(value, sigma,(num_noise_pts, 1)) #standard deviation can be obtained more accu 
    
    def predict_keys(self, vertical):
        '''Generate a series of normally distributed random variables at each successive timestep alpha'''
        if self.model is None:
            return    
        
        mean = None
        sigma = 0.25
        if vertical is True:
            x_test, y_test = None,  self.latest_vy #Randomly initialize the first mu
            
        else:
            x_test, y_test = None, self.latest_vx #y_test is label data, vy is vertical...
        predictions = []
        y_test_examples = []
        #Initially, Gauss is null And 
        counter = 0
        
        
        while counter < 50:
            x_test = np.random.normal(y_test, sigma, (100,1))
            y_test = x_test[random.randint(0, len(x_test)-1)] #Select a random number from the previous gauss_ dis
            y_test_examples.append(y_test)
            test_prediction = self.model.predict(np.expand_dims(x_test, axis=0))
            print(test_prediction[0][0])
            if vertical is True:
                self.y_predicted.append(test_prediction[0][0])
                if test_prediction > y_test:
                    print('w')
                    pyautogui.press('w')
                else:
                    print('s')
                    pyautogui.press('s')
            else:
                self.x_predicted.append(test_prediction[0][0])
                if test_prediction > y_test:
                    print('d')
                    pyautogui.press('d')
                else:
                    print('a')
                    pyautogui.press('a')
            
            counter += 1
            time.sleep(0.001)
        
    

        
    ''' 
    Implement concurrency using python's Multiprocessing module
    so that the model can make predictions on the vertical and horizontal velocity components 
    as well as the keylogger simultaneously
    '''
    def autopilot(self):
        p1 = Process(target=self.listen)
        p2 = Process(target=self.predict_keys(vertical=True)) #Vertical velocity components
        p3 = Process(target=self.predict_keys(vertical=False))#Horizontal velocity components
        
        p1.start()
        
        # p1.join()
        # if self.key == KeyCode.from_char("p"):
        #     p1.terminate()
        #     p2.start()
        #     p3.start()
        #     p2.join()
        #     p3.join()#Join processes if p is detected as keypress
        # if p2.is_alive() and p3.is_alive():
        #     if self.key == KeyCode.from_char("o"):
        #         p2.terminate()
        #         p3.terminate()
        #         return 

        '''Exits with keyesc...'''

        if self.key != KeyCode.from_char("p"):
            p1.join()
        elif self.key == KeyCode.from_char("o"):
            if p2.is_alive() and p3.is_alive():
                p2.terminate()#Kill the AI thread
                p3.terminate()
        else:
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()
             
    