#include <EEPROM.h>

// ----- PINS ---------

//  common 
#define LED_PIN 13

// ZYBO reset
#define ZYBO_RST_PIN  6

//  regenerator  
#define REGENERATOR_TIMEBASE_PIN  2
// TRIGGER OUTPUT: 10-PB2

//  selector  
#define SELECTOR_TIMEBASE_PIN  3
#define SELECTOR_REJECT_PIN    5

//    ---------- REGENERATOR ---------

volatile unsigned int trigger_period=50; // in us

volatile bool regenerator_timebase_onchange_f;
volatile unsigned long regenerator_micro_sec_curr;
unsigned long regenerator_micro_sec_prev;

float regen_coeficient; // from eeprom in setup 
volatile bool do_regen_callib;
volatile bool save_regen_coeficient;

volatile bool irq_occured;

void Regenerator_TimerConfig(){
  DDRB |= (1<<PB2); //alternatively pinMode(10, OUT);(PB2 - Uno, PB6 Leonardo) - setting pin connected to sqr_wave_gen direction to output
  TCCR1A |= (1<<WGM11)|(1<<WGM10); //COM1A0|WGM11|WGM10 - non inverting, fast PWM mode, TOP in OCR1A
  TCCR1A &= ~((1<<COM1A1)|(1<<COM1A0)|(1<<COM1B0)|(1<<COM1B1));
  TCCR1B |= (1<<WGM13)|(1<<WGM12); //further setting timer mode and setting prescaler to 0(clock disabled)
  TCCR1B &= ~((1<<ICNC1)|(1<<ICES1)|(1<<CS12)|(1<<CS11)|(1<<CS10));

  TCCR1A |= (1<<COM1B1); // ??
}

void Regenerator_SetPeriod(unsigned int T){ // in 1/16 us
  OCR1A = T;
  OCR1B = T/2;
  TCCR1B |= (1<<CS10);
}

void Regenerator_Timebase_OnChange(){  
  regenerator_micro_sec_curr = micros();
  regenerator_timebase_onchange_f = true;
}

// ----- SELECTOR ------- 

//#define SELECTOR_TIMEBASE_PIN         3
//#define SELECTOR_REJECT_PIN           5

#define MAX_TSTAMP_NR             30

volatile unsigned long time_base_ctr;

void Selector_Timebase_OnChange(){
  time_base_ctr++;
}

void Selector_Reject(){
  digitalWrite(SELECTOR_REJECT_PIN, HIGH);
  delay(100);
  digitalWrite(SELECTOR_REJECT_PIN, LOW);
}

// SETUP

void setup() {  
  
  // regenerator
  
  ////Regenerator_TimerConfig();        
  ////Regenerator_SetPeriod((trigger_period*16)-1);
  
  pinMode(REGENERATOR_TIMEBASE_PIN, INPUT_PULLUP);     
  EEPROM.get(0, regen_coeficient); 
  attachInterrupt(digitalPinToInterrupt(REGENERATOR_TIMEBASE_PIN), Regenerator_Timebase_OnChange, RISING);
  
  // selecotr
  
  pinMode(SELECTOR_TIMEBASE_PIN, INPUT_PULLUP);
  pinMode(SELECTOR_REJECT_PIN, OUTPUT);
    
  attachInterrupt(digitalPinToInterrupt(SELECTOR_TIMEBASE_PIN), Selector_Timebase_OnChange, RISING);

  // common
  pinMode(LED_PIN, OUTPUT);

  // ZYBO_RST
  pinMode(ZYBO_RST_PIN, OUTPUT);
  digitalWrite(ZYBO_RST_PIN, LOW);
  delay(1);
  digitalWrite(ZYBO_RST_PIN, HIGH);

  Serial.begin(115200); 
  Serial.setTimeout(0);
  Serial.println("Synchronizer");
  
  Selector_Reject();  

  // hello world
  digitalWrite(LED_PIN, LOW);
  delay(1000);
  for (byte i = 0; i < 3; i++){
    digitalWrite(LED_PIN, HIGH);
    delay(50); 
    digitalWrite(LED_PIN, LOW);
    delay(500);
  }
}

// MAIN LOOP
void loop() {

  static unsigned long T_in;
  
  static char serial_buffer[20];
  static byte char_ctr=0;
  static byte cmd_length=0;  
  
  static bool new_cmd_f = false;  
  static char cmd_code;
  static unsigned long cmd_arg;

  static bool new_timestamp_f=false;
  
  struct Timestamp{
    bool valid;
    unsigned long ulValue;
  };  
  static struct Timestamp tstamps[MAX_TSTAMP_NR];

  unsigned long ul_tmp; 
    
  // command reception
  while (Serial.available()){
     char c = Serial.read();   
     serial_buffer[char_ctr++]=c;
     if (c == '\n') {
        serial_buffer[char_ctr] = 0;
        cmd_length = char_ctr-1;    
        char_ctr = 0;
        new_cmd_f = true;
        break;      
     }
  }

  // decode & execute command
  if (new_cmd_f) {
    new_cmd_f = false;
    
    if (cmd_length > 0){ 
      
      // decode
      cmd_code = serial_buffer[0];    
      if (cmd_length > 2) {
        cmd_arg = atol(serial_buffer+2);
      }
          
      // execute
      switch (cmd_code){  

        case 'd': // debug
          noInterrupts();
          ul_tmp = time_base_ctr;             
          interrupts(); 
          Serial.println(ul_tmp);          
        break;
        
        case 's': // reset
          Regenerator_TimerConfig();        
          Regenerator_SetPeriod((trigger_period*16)-1);
          Serial.println("start");
        break;
        
        case 't': // add timestamp
          new_timestamp_f = true;                    
        break;
        
        case 'p': // set trigger period
          trigger_period = cmd_arg;
        
          if (!irq_occured) {            
            Regenerator_SetPeriod((trigger_period*16)-2);
          } else {
            do_regen_callib = true;
            
          }
        break;
        
        default:;
     }    
   }
 }

  // regenerator timebase on chnge handler
  if(regenerator_timebase_onchange_f){    
    regenerator_timebase_onchange_f=0;
    
    T_in = regenerator_micro_sec_curr - regenerator_micro_sec_prev;
    regenerator_micro_sec_prev = regenerator_micro_sec_curr;
    
    if (do_regen_callib){
      do_regen_callib = false;  
      
      Serial.println(trigger_period);   
      regen_coeficient = (float)T_in/(float)trigger_period;
      EEPROM.put(0, regen_coeficient);
    }
    
    if(irq_occured){
      Regenerator_SetPeriod( ((T_in*16)-1)/regen_coeficient );
    }
    irq_occured = true;  
  }
  
  // add tstamp  to table
  
  if (new_timestamp_f){
    byte i;
     new_timestamp_f = false;         
     for(byte i = 0; i < MAX_TSTAMP_NR; i++){      
        if(tstamps[i].valid == false){
           tstamps[i].valid = true;
           tstamps[i].ulValue = cmd_arg;
           
           break;
        }
     }
     if(i==MAX_TSTAMP_NR){
        digitalWrite(LED_PIN, LOW); // ! dlaczewgo low
     }
  }

  // Selector_Reject triggering, if any timestamp is outdated
  bool Selector_Reject_flag = false;
  unsigned long t;
  
  noInterrupts();
  t = time_base_ctr;              
  interrupts(); 
  for(byte i = 0; i < MAX_TSTAMP_NR; i++){      
     if(tstamps[i].valid){    
        if(tstamps[i].ulValue <= t){
           tstamps[i].valid = false;
           Selector_Reject_flag = true;         
        }        
     }
  }

  // Selector_Reject generation
  if (Selector_Reject_flag) {
    Selector_Reject();    
  }
}
