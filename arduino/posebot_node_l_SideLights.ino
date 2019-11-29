 
#include <WiFi.h>        // Include the Wi-Fi library
#include <PubSubClient.h>

const char* ssid     = "posenet";         // The SSID (name) of the Wi-Fi network you want to connect to
const char* password = "posenetS";     // The password of the Wi-Fi network

// Add your MQTT Broker IP address, example:
const char* mqtt_server = "10.42.0.1";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


// user definitions //
const float systemInterval = 50;
const int inRoomSize = 600;

// left node
// const char clientName = 'arduino left';
// const char nodeId = 'l';
// const int idNo = 0;
// const char nodeTwin = 'r';

// right node
const char* clientName = "arduino right";
char nodeId = 'r';
const int idNo = 1;
const char nodeTwin = 'l';
char* subTopic = "/pose/r/HandLights";

int curMsg;

// system definitions //

float sideLRangeMax = inRoomSize / 2;
float sideLRangeMin = sideLRangeMax * (-1);
int ledRangeMin = 0;
int ledRangeMax = 255;

int relay_pin = 15;

void setup() {
  int curMsg = 0;
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(msgSuccess);
  pinMode (relay_pin, OUTPUT);
}

void setup_wifi() {
    
////////////////////////////////////////////////////////
// setup as a wifi station
  Serial.begin(115200);         // Start the Serial communication to send messages to the computer
  delay(10);
  Serial.println('\n');
  
  WiFi.begin(ssid, password);             // Connect to the network
  Serial.print("Connecting to ");
  Serial.print(ssid);

  while (WiFi.status() != WL_CONNECTED) { // Wait for the Wi-Fi to connect
    delay(500);
    Serial.print('.');
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());         // Send the IP address of the ESP8266 to the computer

  ///////////////////////////////////////////////////////
  }

void msgSuccess(char* topic, byte* payload, unsigned int length) {
      String value="";
      for (int i=0;i<length;i++){
        value+= (char)payload[i];
      }
      curMsg = value.toInt();
      Serial.print(curMsg);
}

// control the led based on nodeId and command
void ledCtrl(){
  if(subTopic == "/pose/r/SideLights"){
      int color = map(int(curMsg), sideLRangeMin, sideLRangeMax, ledRangeMin, ledRangeMax);
          Serial.print(color);
    }else if(subTopic == "/pose/r/HandLights"){
      if(curMsg==1){
        digitalWrite(relay_pin, LOW);
        Serial.print("Hand Up");
      }else if(curMsg==0){
        digitalWrite(relay_pin, LOW);
      }
      }
}
      
        //if(color < 256 and color > 0):
            // left node //
            // colorValue = rgb_to_hex(color,0, 0)
            // right node
          //  colorValue = rgb_to_hex(0, 0, color)
          //  pycom.rgbled(int(colorValue, 16))

    


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(clientName)) {
      Serial.println("connected");
      // Subscribe
      client.subscribe(subTopic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() { 
   if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 5000) {
    lastMsg = now;
  }
  ledCtrl();

  delay(systemInterval);
  
}
