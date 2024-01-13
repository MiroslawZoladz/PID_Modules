//CAMERA

//Wysyła przez UART stan na pinie 3 na każym rosnący zboczu przebiegu na pinie 2.

//INPUT: INPUT: 2-PD2(Uno), 2-PD1(Leonardo), 3-PD3(Uno), 3-PD0(Leonardo)
//OUTPUT: - UART

//Zbocza rosnące przebiegu podanego na pin 2 uruchamiją przerwanie, w którym stan pinu 3 jest odczytywany oraz wysyłany przez UART.
//Testy dzialaja tylko na Uno, bo resetuje sie przy otwieraniu portu

#define SIGNAL_PIN 3
#define SAMPLE_PIN 2

byte send_sample_divider;
bool send_sample_flag;

void OnChange_Sample(){
  send_sample_divider++;
  if (send_sample_divider==10) {
    send_sample_divider=0;
    send_sample_flag = true;
  }
}

void setup() {
  pinMode(SIGNAL_PIN, INPUT_PULLUP);
  pinMode(SAMPLE_PIN, INPUT_PULLUP);
    
  Serial.begin(115200);
  Serial.setTimeout(-1);
  Serial.println("Camera");

  attachInterrupt(digitalPinToInterrupt(SAMPLE_PIN), OnChange_Sample, RISING);
}

void loop() {
  if (send_sample_flag){
    send_sample_flag = false;
    Serial.print(digitalRead(SIGNAL_PIN));
  }
}
