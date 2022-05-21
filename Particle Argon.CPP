int customerTracker(String input);

int led1 = D3;
            
void setup() {
    pinMode(led1, OUTPUT);
    digitalWrite(led1, HIGH);
    delay(2000);
    digitalWrite(led1, LOW);
    Particle.function("customerTracker", customerTracker);
    
    
}

void loop() {
    
}
        
int customerTracker(String input)
{
        
    if(input == "Customers Inside")
    {
        digitalWrite(led1, HIGH);
        return 1;
    }
    else
    {
        digitalWrite(led1, LOW);
        return -1;
    }
}
