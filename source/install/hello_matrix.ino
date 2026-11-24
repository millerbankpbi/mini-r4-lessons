#include "MatrixMiniR4.h"

void setup()
{
  MiniR4.begin();
  MiniR4.PWR.setBattCell(2);
  Serial.begin(9600);
  MiniR4.OLED.setTextSize(1);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 0);
  MiniR4.OLED.print("Hello");
  MiniR4.OLED.setCursor(0, 16);
  MiniR4.OLED.print("MATRIX R4");
  MiniR4.OLED.display();
}

void loop()
{

}
