#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "TP-Link_B52E";
const char* password = "wrooo2023";

ESP8266WebServer server(80);
int ledPin = 13; // Pin D7 on D1 Mini
int buttonPin = 16; //D8

boolean led_state = true;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLDOWN); 
  digitalWrite(ledPin, HIGH);

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
  server.on("/on", handleOn);
  server.on("/off", handleOff);
  server.on("/bright", handleBrightness);

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
  state = digitalRead(buttonPin);
  if (state == HIGH){
      if (led_state == true){
          digitalWrite(ledPin, LOW);
      }else {
          digitalWrite(ledPin, HIGH);
      }
  }
}

void handleRoot() {
  server.send(200, "text/plain", "Bienvenido al servidor ESP8266");
}

void handleOn() {
  digitalWrite(ledPin, HIGH);
  server.send(200, "text/plain", "LED encendido");
  led_state = true;
}

void handleOff() {
  digitalWrite(ledPin, LOW);
  server.send(200, "text/plain", "LED apagado");
  led_state = false;
}

void handleBrightness() {
  if (server.hasArg("data")) {
    int brightness = server.arg("data").toInt();
    analogWrite(ledPin, brightness);
    server.send(200, "text/plain", "Brillo ajustado: " + String(brightness));
  } else {
    server.send(400, "text/plain", "Solicitud incorrecta");
  }
}
