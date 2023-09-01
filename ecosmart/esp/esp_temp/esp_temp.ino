#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DHT.h>c

const char* ssid = "TP-Link_B52E";
const char* password = "wrooo2023";

ESP8266WebServer server(80);

#define DHTPIN 5       // Pin de datos conectado al pin digital 5
#define DHTTYPE DHT11  // Selecciona el tipo de sensor (DHT11 o DHT22)

DHT dht(DHTPIN, DHTTYPE);

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
  server.on("/temp", handleTemperature);
  server.on("/hum", handleHumidity);

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
  float temperature = dht.readTemperature();
  if (isnan(temperature)) {
    server.send(500, "text/plain", "Error al leer la temperatura");
  } else {
    server.send(200, "text/plain", String(temperature));
  }
}

void handleHumidity() {
  float humidity = dht.readHumidity();
  if (isnan(humidity)) {
    server.send(500, "text/plain", "Error al leer la humedad");
  } else {
    server.send(200, "text/plain", String(humidity));
  }
}
