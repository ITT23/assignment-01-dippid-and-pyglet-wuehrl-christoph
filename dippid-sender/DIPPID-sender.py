from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
from random import randrange
from json import dumps
from threading import Thread
import numpy as np


IP = '127.0.0.1'
PORT = 5700

sock = socket(AF_INET, SOCK_DGRAM)


# safe for the current values of the accelerometer
accelerometer_values_degree = {
    "x" : 0,
    "y" : 65,
    "z" : 124
}

# values that will be sent to localhost
message = {
    "button_1": 0,
    "accelerometer": {
    "x" : 0,
    "y" : 0,
    "z" : 0
    }
}



def press_button_randomly():
    while(True):
        random_sleep_time = randrange(5) # randomizes the time for how long the button is pressed and released
        sleep(random_sleep_time)
        if(message["button_1"] == 0):
            message["button_1"] = 1
        else:
            message["button_1"] = 0
        sleep(1)

def generate_X_value ():
    while(True):
        accelerometer_values_degree["x"] += 10
        message["accelerometer"]["x"] = calc_sin_value("x") * 0.5 #generates x values for the accelerometer, the multiplier defines the min and max value
        sleep(0.3) #defines how fast the value changes

def generate_Y_value ():
    while(True):
        accelerometer_values_degree["y"] += 15
        message["accelerometer"]["y"] = calc_sin_value("y") * 1.5 #generates y values for the accelerometer, the multiplier defines the min and max value
        sleep(0.6) #defines how fast the value changes

def generate_Z_value ():
    while(True):
        accelerometer_values_degree["z"] += 13
        message["accelerometer"]["z"] = calc_sin_value("z") * 3 #generates z values for the accelerometer, the multiplier defines the min and max value
        sleep(0.7) #defines how fast the value changes

def calc_sin_value (key):
    # formula from https://numpy.org/doc/stable/reference/generated/numpy.sin.html
    if(accelerometer_values_degree[key] > 360):
        accelerometer_values_degree[key] -= 359 #resets the values, that they are between 0 and 360
    return np.sin(accelerometer_values_degree[key] * np.pi / 180)

def main():
    button_thread = Thread(target=press_button_randomly, daemon=True)
    button_thread.start() #start a thread that activates and deactivates button_1
    x_value_thread = Thread(target=generate_X_value, daemon=True)
    x_value_thread.start() #start a thread that sets x values for the accelerometer
    y_value_thread = Thread(target=generate_Y_value, daemon=True)
    y_value_thread.start() #start a thread that sets y values for the accelerometer
    z_value_thread = Thread(target=generate_Z_value, daemon=True)
    z_value_thread.start() #start a thread that sets z values for the accelerometer
    while True:
        sock.sendto(dumps(message).encode(), (IP, PORT)) # converts the dict to a json and sends it to local host
        sleep(1)

main()