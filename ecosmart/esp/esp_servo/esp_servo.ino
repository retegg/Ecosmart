#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

const char* ssid = "TP-Link_B52E";
const char* password = "wrooo2023";

ESP8266WebServer server(80);
Servo myservo;  // Objeto servo

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
  server.on("/setangle", handleSetAngle);

  myservo.attach(D1);  // Pin D2 utilizado para controlar el servo

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  server.send(200, "text/plain", "Bienvenido al servidor ESP8266");
}

void handleSetAngle() {
  if (server.hasArg("data")) {
    int angle = server.arg("data").toInt();
    myservo.write(angle);
    server.send(200, "text/plain", "Ángulo ajustado: " + String(angle));
  } else {
    server.send(400, "text/plain", "Solicitud incorrecta");
  }
}
