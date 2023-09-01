#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DHTesp.h>  // Incluimos la nueva biblioteca

const char* ssid = "TP-Link_B52E";
const char* password = "wrooo2023";

ESP8266WebServer server(80);
DHTesp dht;  // Creamos una instancia de la clase DHTesp

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

  dht.setup(5, DHTesp::DHT11);  // Configuramos el sensor DHT11

  server.on("/", handleRoot);
  server.on("/temp", handleTemperature);
  server.on("/hum", handleHumidity);
  server.on("/type", handleType)

  server.begin();
  Serial.println("Servidor iniciado");
}

void loop() {
  server.handleClient();
}

void handleRoot() {
  server.send(200, "text/plain", "Bienvenido al servidor ESP8266");
}

void handleTemperature() {
  float temperature = dht.getTemperature();
  if (isnan(temperature)) {
    server.send(500, "text/plain", "Error al leer la temperatura");
  } else {
    server.send(200, "text/plain", String(temperature));
  }
}

void handleHumidity() {
  float humidity = dht.getHumidity();
  if (isnan(humidity)) {
    server.send(500, "text/plain", "Error al leer la humedad");
  } else {
    server.send(200, "text/plain", String(humidity));
  }
}

void handleType(){
  server.send(200, "text/plain", "1"); // tipo 1 para sensor DHT
}

  }
