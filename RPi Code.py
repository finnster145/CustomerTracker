#Import modules used within the code
import RPi.GPIO as GPIO
import time
import os
import requests


#RPi GPIO setup
GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)

#RPi pins setup, these are the pins for the Ultrasonic sensors. 
echopin = [4,18]
trigpin = [17,27]
 
#Initiating the setups. In a for loop to reduce code. This is made easier as the echopin and trigpin are in an array.
for j in range(2):
    GPIO.setup(trigpin[j], GPIO.OUT)
    GPIO.setup(echopin[j], GPIO.IN)
    print(j, echopin[j], trigpin[j])
    print(" ")
    


#Function that will monitor for a customer walking in or out of the shop. 
#Users a timer to determine the distance between the ultrasonic sensor and the object in front to calculate the distance.
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
#Sets customertracker to 0 to begin tracking
customertracker = 2
LEDUpdate = 0
try:
    
    while True:
        
        

        
        #In Sensor
        distance = ping(echopin[0], trigpin[0])
        
        #Out Sensor
        distance1 = ping(echopin[1], trigpin[1])
        

        #Default distance between the sensor and the other door is set to 30cm, if an object passes in front of the
        #sensor and is less than 30cm it will detect it as a customer walking in.
        if (distance < 30):
            time.sleep(0.5)
            
               
            print("Customer walked in")
            
            #iFTTT webhook with timeout of 60seconds.
            
            requests.post('https://maker.ifttt.com/trigger/customerIn/json/with/key/cuSnwRhufs9YsIvO0CA5un', timeout = 60)
            
            #updates customer tracker by adding 1 to the current count.
            customertracker += 1
            
        
  
        #The exit door. Makes sure that the distance is less than 30 and that the customertracker is greater than 0 to ensure no false detection.          
        if (distance1 < 30 and customertracker > 0):
            time.sleep(0.5)
            
            #iFTTT webhook to send notification. sends timeout feature.
            requests.post('https://maker.ifttt.com/trigger/customerOut/json/with/key/cuSnwRhufs9YsIvO0CA5un', timeout = 60)
            print("Customer Walked Out")
            customertracker -= 1
        
        
        
        #If a customer is in the store it will activate the webhook in the particle via the system CLI. It has a timeout of 60seconds.
        if (customertracker == 1 and LEDUpdate != 1):
            os.system('timeout 60s curl https://api.particle.io/v1/devices/e00fce68b4a1fcad83aa9f39/customerTracker -d access_token=d367aafaa562032c7ba883fe035bae0878df8ef6 -d "args=Customers Inside"')
          LEDUpdate = 1
        elif (customertracker < 1 and LEDUpdate == 1):
            os.system('timeout 60s curl https://api.particle.io/v1/devices/e00fce68b4a1fcad83aa9f39/customerTracker -d access_token=d367aafaa562032c7ba883fe035bae0878df8ef6 -d "args=No Customers Inside"')
            LEDUpdate = 0
            
            

        #Displays in the terminal how many people are in the store.
        print("Customers in store: ", customertracker)
      
 
        
#Closes the prgram if a key interrupt occurs.
except KeyboardInterrupt:
    print("keyboard interrupt detected, File closed")        
