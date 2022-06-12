import RPi.GPIO as GPIO
import time
import os
import requests



GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)


echopin = [4,18]
trigpin = [17,27]
 
for j in range(2):
    GPIO.setup(trigpin[j], GPIO.OUT)
    GPIO.setup(echopin[j], GPIO.IN)
    print(j, echopin[j], trigpin[j])
    print(" ")
    


 
def ping(echo, trig):
    
    GPIO.output(trig, False)

    time.sleep(0.5)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    pulse_start = time.time()


    while GPIO.input(echo) == 0:
        pulse_start = time.time()


    while GPIO.input(echo) == 1:
        pulse_end = time.time()


    pulse_duration = pulse_end - pulse_start
    # mutiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = pulse_duration * 17150
    
    distance = round(distance, 2)
    
    return distance

print(" press Ctrl+c to stop program ")
customertracker = 0
try:
    
    while True:
        
        

        
        #In Sensor
        distance = ping(echopin[0], trigpin[0])
        
        #Out Sensor
        distance1 = ping(echopin[1], trigpin[1])
        


        if (distance < 30):
            time.sleep(0.5)
            
               
            print("Customer walked in")
            requests.post('https://maker.ifttt.com/trigger/customerIn/json/with/key/cuSnwRhufs9YsIvO0CA5un', timeout = 60)
            customertracker += 1
            
        

            
        if (distance1 < 30 and customertracker > 0):
            time.sleep(0.5)
            
            requests.post('https://maker.ifttt.com/trigger/customerOut/json/with/key/cuSnwRhufs9YsIvO0CA5un', timeout = 60)
            print("Customer Walked Out")
            customertracker -= 1
        
        
        if (customertracker > 0):
            os.system('timeout 60s curl https://api.particle.io/v1/devices/e00fce68b4a1fcad83aa9f39/customerTracker -d access_token=d367aafaa562032c7ba883fe035bae0878df8ef6 -d "args=Customers Inside"')
        else:
            os.system('timeout 60s curl https://api.particle.io/v1/devices/e00fce68b4a1fcad83aa9f39/customerTracker -d access_token=d367aafaa562032c7ba883fe035bae0878df8ef6 -d "args=No Customers Inside"')
            
            


        print("Customers in store: ", customertracker)
      
 
        
    
except KeyboardInterrupt:
    print("keyboard interrupt detected, File closed")        
