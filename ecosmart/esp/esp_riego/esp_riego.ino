#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


const char* ssid = "TP-Link_B52E";
const char* password = "wrooo2023";
int inputPin = 15; // Pin D1 en Wemos D1 Mini
int val = 0;

ESP8266WebServer server(80);

void handleRoot() {
  server.send(200, "text/plain", String(val));  
}

void setup() {
  pinMode(inputPin, INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
  val = analogRead(inputPin);
  

}
