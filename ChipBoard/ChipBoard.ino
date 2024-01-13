#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>

OneWire oneWire(14);
DallasTemperature DS18B20(&oneWire);
char board_id_string[8*2+1];

// ------ auxiliary ------------

void byte_array_to_hex_string(unsigned char byte_array_size, unsigned char byte_array[], char hex_string[]){
  for(unsigned char i = 0; i<byte_array_size; i++){
    sprintf(hex_string+(2*i), "%.2X", byte_array[i]);
  }
  hex_string[byte_array_size*2] = NULL;
}

// ----- DS18B20 --------------
void DS18B20_Initialize(unsigned char ID[]){
    
  Wire.begin();
  DS18B20.begin();
  DS18B20.setResolution(9);    
  DS18B20.getAddress(ID, 0);  
}

float DS18B20_ReadTemp(){
  DS18B20.requestTemperatures();
  return DS18B20.getTempCByIndex(0);
}

// --------- MCP3425 ----------
#define MCP3425_I2C_ADDR 0x68// CQ:000:0x68; CS:010:0x6A

void MCP3425_Initialize(){  
  Wire.begin(); // Initialise I2C communication as MASTER    
  Wire.beginTransmission(0x6A); // Start I2C Transmission ( I2C Addr)
  Wire.write(0x10); // Send configuration command // Continuous conversion mode, 12-bit resolution
  Wire.endTransmission(); // Stop I2C Transmission
}

float MCP3425_ReadRaw(){  
  unsigned int data[2];  
  
  Wire.beginTransmission(MCP3425_I2C_ADDR); // Start I2C Transmission 
  Wire.write(0x00); // Select data register  
  Wire.endTransmission(); // Stop I2C Transmission
  
  Wire.requestFrom(MCP3425_I2C_ADDR, 2); // Request 2 bytes of data  
  // Read 2 bytes of data, raw_adc msb, raw_adc lsb 
  if(Wire.available() == 2)
  {
    data[0] = Wire.read();
    data[1] = Wire.read();
  }   
  // Convert the data to 12-bits
  int raw_adc = (data[0] & 0x0F) * 256 + data[1];
  if(raw_adc > 2047)
  {
    raw_adc -= 4095;
  }
  
  return (744.3 - (float)raw_adc)* 0.552;
}

// ------- MAIN ------------------

void setup() {  
  Serial.begin(115200);
  Serial.setTimeout(-1);

  // ID AND AIR TEMP SENSOR
  // get id
  unsigned char ID[8];
  DS18B20_Initialize(ID);
  byte_array_to_hex_string(6, ID+1, board_id_string);

  // CHIP TEMP SENSOR
  MCP3425_Initialize();

  // Callib, Set PWM frequency for D5 & D6
  TCCR0B = TCCR0B & B11111000 | B00000001;    // set timer 0 divisor to     1 for PWM frequency of 62500.00 Hz  
  pinMode(6, OUTPUT);
}

void loop (){
   char rx_char, raedout_mode;
   
   // odczyt trybu
   Serial.readBytes(&raedout_mode, 1);
   Serial.write(&raedout_mode, 1);
   
   // forwardowanie obcych pomiarów
   while (true) {
      Serial.readBytes(&rx_char, 1);
      if (rx_char == '\n') break;
      Serial.write(&rx_char, 1);
   }
   
   // dołożenie swojego
   Serial.print(";");
   switch(raedout_mode){
      case 's':      
      Serial.println(board_id_string);
      break;     
      
      case 'r':
      Serial.println(MCP3425_ReadRaw());
      break;
      
      case 't':
      Serial.println(DS18B20_ReadTemp());
      break;

      case 'C':      
      Serial.println("");
      analogWrite(6, 25); //10%      
      break;

      case 'c':
      Serial.println("");
      analogWrite(6, 0); //10%      
      break;

      default:
      Serial.println("???");
      break;
   }    
}
