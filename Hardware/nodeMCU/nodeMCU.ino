#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

// --- WIFI CONFIGURATION ---
const char* ssid = "Nothing";       // Your Mobile Hotspot Name
const char* password = "abdulrahman";     // Your Mobile Hotspot Password
String serverIP = "http://10.139.52.94:5000/update_sensor";

// --- PIN CONFIGURATION (CORRECTED) ---
// D5 = GPIO 14, D6 = GPIO 12, D1 = GPIO 5, D2 = GPIO 4
const int trigPin = 14; // D5
const int echoPin = 12; // D6
const int led = 5;      // D1 (Corrected: GPIO 5 is D1)
const int buzzer = 4;   // D2 (Corrected: GPIO 4 is D2)

void setup() {
  Serial.begin(115200);
  
  // Set Pin Modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(led, OUTPUT);
  pinMode(buzzer, OUTPUT);

  // Initialize Outputs (Low = Off)
  digitalWrite(led, LOW);
  digitalWrite(buzzer, LOW);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void loop() {
  // 1. Read Distance (Ultrasonic Sensor)
  long duration;
  int distance;
  
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Calculate distance in cm

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // 2. Send to Laptop Server (Federated Simulation)
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    
    // Start connection to server
    http.begin(client, serverIP);
    http.addHeader("Content-Type", "application/json");
    
    // Create JSON payload
    String jsonPayload = "{\"distance\":\"" + String(distance) + "\"}";
    
    // Send POST request
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
      
      // -----------------------------------------------------
      // 3. THIS IS THE TRIGGER CODE (FIXED)
      // -----------------------------------------------------
      // We check for "1}" because the server sends {"command":1}
      
      if (response.indexOf("1}") > 0) { 
        Serial.println("!!! THEFT ALERT !!!");
        
        // ACTIVATE HARDWARE
        digitalWrite(buzzer, HIGH);
        digitalWrite(led, HIGH);
        
        delay(1000); // Beep for 1 second
      } else {
        // TURN OFF HARDWARE
        digitalWrite(buzzer, LOW);
        digitalWrite(led, LOW);
      }
      // -----------------------------------------------------
      
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end(); // Free resources
  } else {
    Serial.println("WiFi Disconnected");
  }
  
  delay(500); // Wait 0.5 seconds before next reading
}