#include <WiFiS3.h>
#define ENABLE_DRIVEDC_BRAKE_DELAY
#include "MatrixMiniR4.h"

const char* NAME = "R4-T01";
const char* PASS = "12345678";
WiFiServer server(80);

const char PAGE[] =
  "<!DOCTYPE html><html><head><meta charset='utf-8'>"
  "<meta name='viewport' content='width=device-width,initial-scale=1'><title>Mini R4</title>"
  "<style>body{background:#ECE8F7;text-align:center;font-family:sans-serif}"
  "button{width:84px;height:84px;margin:6px;border:0;border-radius:50%;"
  "background:#3B3256;color:#B7A4EC;font-size:32px}#s{background:#EE6B5E;color:#fff}</style>"
  "</head><body><h2>Mini R4</h2>"
  "<p><button onclick=\"go('F')\">▲</button></p>"
  "<p><button onclick=\"go('L')\">◀</button><button id='s' onclick=\"go('S')\">■</button>"
  "<button onclick=\"go('R')\">▶</button></p>"
  "<p><button onclick=\"go('B')\">▼</button></p>"
  "<script>function go(c){fetch('/'+c)}</script></body></html>";

void setup()
{
  MiniR4.begin();
  MiniR4.PWR.setBattCell(2);
  Serial.begin(9600);
  MiniR4.DriveDC.begin(1, 2, false, true);
  MiniR4.OLED.setTextSize(2);
  MiniR4.OLED.clearDisplay();
  MiniR4.OLED.setCursor(0, 8);
  MiniR4.OLED.print(NAME);
  MiniR4.OLED.display();
  WiFi.config(IPAddress(192, 168, 4, 1));
  if (WiFi.beginAP(NAME, PASS) != WL_AP_LISTENING) {
    MiniR4.OLED.setCursor(0, 40);
    MiniR4.OLED.print("AP fail");
    MiniR4.OLED.display();
    while (true);
  }
  server.begin();
  MiniR4.OLED.setTextSize(1);
  MiniR4.OLED.setCursor(0, 40);
  MiniR4.OLED.print(WiFi.localIP());
  MiniR4.OLED.display();
}

void loop()
{
  WiFiClient client = server.available();
  if (!client) return;
  String line = client.readStringUntil('\n');
  while (client.connected() && client.readStringUntil('\n').length() > 1) {}
  int a = line.indexOf(' ') + 1;
  String path = line.substring(a, line.indexOf(' ', a));
  client.print("HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: ");
  client.print(path == "/" ? "text/html; charset=utf-8\r\n\r\n" : "text/plain\r\n\r\nOK");
  if (path == "/") client.print(PAGE);
  client.stop();
  if (path == "/F") MiniR4.DriveDC.MoveSyncTime(50, 50, 0.5, true);
  if (path == "/B") MiniR4.DriveDC.MoveSyncTime(-50, -50, 0.5, true);
  if (path == "/L") MiniR4.DriveDC.MoveSyncTime(-50, 50, 0.5, true);
  if (path == "/R") MiniR4.DriveDC.MoveSyncTime(50, -50, 0.5, true);
  if (path == "/S") MiniR4.DriveDC.brake(true);
}
