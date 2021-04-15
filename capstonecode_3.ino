const int readPin = A3;
int readVal;
float V2 ;
float Temp ;

int dT_1 = 5000;
int dT_2 = 5; 

const int input_pins[3] = {13,12,11}; // 3 inputs
//const int output_pins[4]={2,3,4,7,8}; // 7 total output

int i=0;

const int ENABLE = 3; //pwm signal input to enable the motor speed 
const int DIRA = 4; 
const int DIRB = 7;
const int relay_enable_1 = 2;
const int relay_enable_2 = 8;

const int t_flag =10; // temp flag


void setup() {
 
  pinMode(readPin,INPUT); 
  for(int j=0;j<3; j++){
    pinMode(input_pins[j],INPUT);
  }
  pinMode(readPin,INPUT);
  pinMode(ENABLE,OUTPUT);
  pinMode(DIRA,OUTPUT);
  pinMode(DIRB,OUTPUT);
  pinMode(relay_enable_1,OUTPUT);
  pinMode(relay_enable_2,OUTPUT); 



  pinMode(t_flag,OUTPUT); // temp read pin
 
  
 Serial.begin(9600);
}

void loop() {

while(i<1){

  
 //initalizes all of the outputs to the appropriate inital states 
 
 analogWrite(ENABLE,0);                //Motor OFF 
 digitalWrite(DIRA,LOW);
 digitalWrite(DIRB,LOW);
 digitalWrite(relay_enable_1,HIGH); //relay 1 off
 digitalWrite(relay_enable_2,HIGH); // relay 2 off

 digitalWrite(t_flag,LOW); // temp flag diabled
 
 Serial.println("time delay is happening"); //time delay before the inital loop activates 
 delay(dT_1);
 i++;
}

Serial.print(digitalRead(input_pins[0]));

Serial.print(digitalRead(input_pins[1]));

Serial.println(digitalRead(input_pins[2]));

delay(1000);


readVal= analogRead(readPin ); // reads the input analog input from sensor 
V2=(5./1023.)*readVal; // converts analog input to voltage value 
Temp = ((100*V2)- 50); // converts voltage to temperature in celsius 
//Serial.println(Temp);

                              // starts checking inputs from pi 

if(digitalRead(input_pins[0])==LOW && digitalRead(input_pins[1])==LOW &&  digitalRead(input_pins[2])==LOW){ //// Function 1 (000)----------> NULL


Serial.println("NUll");

}

else if(digitalRead(input_pins[0])==LOW && digitalRead(input_pins[1])==LOW &&  digitalRead(input_pins[2])==HIGH){ //// Function 2 (001)----------> Lights ON
Serial.println("Light ON");

digitalWrite( relay_enable_1,LOW);
Serial.println(Temp);
  
  if ( Temp>=28){ // temp limit set 
    Serial.println("TEMP FLAG-----> TOO HOT");//enable temp flag 
    digitalWrite(t_flag,HIGH);

  }
  
  else{
    Serial.println("Normal Temp");// disable temp flag 
    digitalWrite(t_flag,LOW);
  }
}

else if(digitalRead(input_pins[0])==LOW && digitalRead(input_pins[1])==HIGH &&  digitalRead(input_pins[2])==LOW){ //// Function 3 (010)----------> Motor Direction A (Open)
Serial.println("Motor Direction A ");
analogWrite( ENABLE,255);
digitalWrite( DIRA,HIGH);
digitalWrite( DIRB,LOW);

}

else if(digitalRead(input_pins[0])==LOW && digitalRead(input_pins[1])==HIGH &&  digitalRead(input_pins[2])==HIGH){ //// Function 4(011)----------> Motor Direction B (Close)
Serial.println("Motor Direction B");
analogWrite( ENABLE,255);
digitalWrite( DIRA,LOW);
digitalWrite( DIRB,HIGH);


}

else if(digitalRead(input_pins[0])==HIGH && digitalRead(input_pins[1])==LOW &&  digitalRead(input_pins[2])==LOW){ //// Function 5 (100)----------> Motor OFF
Serial.println("Motor OFF");
analogWrite( ENABLE,0);
digitalWrite( DIRA,LOW);
digitalWrite( DIRB,LOW);

}

else if(digitalRead(input_pins[0])==HIGH && digitalRead(input_pins[1])==LOW &&  digitalRead(input_pins[2])==HIGH){ //// Function 6 (101)----------> Fan ON
Serial.println(" Fan ON");
digitalWrite( relay_enable_2,LOW);
digitalWrite(t_flag,LOW); // reset temp flag 
}

else if(digitalRead(input_pins[0])==HIGH && digitalRead(input_pins[1])==HIGH &&  digitalRead(input_pins[2])==LOW){ //// Function 7 (110)----------> Fan OFF
Serial.println("Fan OFF ");
digitalWrite( relay_enable_2,HIGH);
}


else if(digitalRead(input_pins[0])==HIGH && digitalRead(input_pins[1])==HIGH&&  digitalRead(input_pins[2])==HIGH){ //// Function 8 (111)----------> Lights OFF
// reset temperature flags 
digitalWrite( relay_enable_1,HIGH);
Serial.println("Light OFF");
digitalWrite(t_flag,LOW); // reset temp flag

}

//delay(dT_2);  //time delay if needed 

}
