#include "MatrixMiniR4.h"

void setup()
{
  MiniR4.begin();
  MiniR4.PWR.setBattCell(2);
  Serial.begin(9600);
  MiniR4.OLED.setTextSize(2);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 0);
  MiniR4.OLED.print("Hello");
  MiniR4.OLED.setCursor(0, 24);
  MiniR4.OLED.print("Mini R4 OK");
  MiniR4.OLED.display();
  MiniR4.Buzzer.Tone(NOTE_C5, 200);
  Serial.println("Mini R4 OK");
}

void loop()
{
  MiniR4.LED.setColor(1, 0, 255, 0);
  delay(500);
  MiniR4.LED.setColor(1, 0, 0, 0);
  delay(500);
}
