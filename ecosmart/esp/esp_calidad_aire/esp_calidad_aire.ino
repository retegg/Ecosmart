#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <MQ135.h>

const char* ssid = "TP-Link_B52E";
const char* password = "wrooo2023";

ESP8266WebServer server(80);
const int MQ135_PIN = A0; // Pin analógico al que está conectado el sensor MQ-135

MQ135 mq135(MQ135_PIN);

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }

  Serial.println("Conectado a la red WiFi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/type", handleType);
  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  float airQuality = readAirQuality();
  server.send(200, "text/plain", String(airQuality));
}
void handleType() {
  server.send(200, "text/plain", "3");
}
float readAirQuality() {
  float rs = 0;
  rs = analogRead(MQ135_PIN);
  delay(100);
  return rs;
}
