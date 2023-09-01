#include <DHT.h> // Incluye la librería para el sensor DHT

#define DHTPIN 5   // Define el pin al que está conectado el sensor
#define DHTTYPE DHT11   // Cambia a DHT22 si estás usando ese sensor

DHT dht(DHTPIN, DHTTYPE); // Crea una instancia del sensor

void setup() {
  Serial.begin(9600); // Inicializa la comunicación serial
  dht.begin(); // Inicializa el sensor DHT
}

void loop() {
  // Lee la temperatura en grados Celsius
  float temperature = dht.readTemperature();

  // Lee la humedad relativa
  float humidity = dht.readHumidity();

  // Verifica si la lectura fue exitosa
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Error al leer el sensor DHT");
    return;
  }

  // Muestra los valores en el monitor serial
  Serial.print("Temperatura: ");
  Serial.print(temperature);
  Serial.print(" °C\t");
  Serial.print("Humedad: ");
  Serial.print(humidity);
  Serial.println("%");

  delay(2000); // Espera 2 segundos antes de la siguiente lectura
}
