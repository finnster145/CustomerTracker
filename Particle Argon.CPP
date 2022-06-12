#The input recieved via the cloud function request by the rpi.
int customerTracker(String input);

#LED Pin setup
int led1 = D3;
            
void setup() {
    
    #Default pin mode setup
    pinMode(led1, OUTPUT);
    digitalWrite(led1, HIGH);
    delay(2000);
    digitalWrite(led1, LOW);
    
    #Reads data in via the Cloud function
    Particle.function("customerTracker", customerTracker);
    
    
}

void loop() {
    
}
        
int customerTracker(String input)
{
     
    #If RPi sends data that says "customers inside" then this will be initiated and will turn the LED ON
    if(input == "Customers Inside")
    {
        digitalWrite(led1, HIGH);
        return 1;
    }
    else
    #If the cloud function recieves data that is anything other than customers inside then it will turn the LED off.
    {
        digitalWrite(led1, LOW);
        return -1;
    }
}
