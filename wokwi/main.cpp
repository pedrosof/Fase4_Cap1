#include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

// Definir os pinos
#define DHTPIN 4       // Pino onde o DHT22 está conectado
#define DHTTYPE DHT22  // Tipo do sensor DHT

#define LDR_PIN 34     // Pino do LDR (ADC) - GPIO 34

#define BUTTON_P 27    // Botão P no GPIO 27
#define BUTTON_K 26    // Botão K no GPIO 26

// Definir pinos SDA e SCL para a comunicação I2C
#define SDA_PIN 22     // Pino SDA (dados I2C)
#define SCL_PIN 21     // Pino SCL (relógio I2C)

// Inicializar o sensor DHT
DHT dht(DHTPIN, DHTTYPE);

// Inicializar o display OLED (SSD1306)
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Limites para exibição na tela OLED
float temp_threshold = 30.0;  // Limiar para a temperatura (em graus Celsius)
float humidity_threshold = 30.0;  // Limiar para a umidade (em percentual)

// Mapeamento de LDR para faixa de LUX
#define LUX_MAX 1000    // LUX máximo que queremos mostrar
#define LUX_MIN 0       // LUX mínimo

void setup() {
  // Inicializar comunicação serial
  Serial.begin(115200);  // Inicializa o monitor serial
  
  // Inicializa a comunicação I2C com os pinos SDA e SCL
  Wire.begin(SDA_PIN, SCL_PIN);

  // Inicializa o sensor DHT
  dht.begin();
  
  // Inicializa o display OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {  // Endereço I2C do OLED
    Serial.println(F("Falha ao inicializar o display OLED!"));
    while (true);
  }
  
  // Configuração do LDR
  analogReadResolution(12);  // Resolução de 12 bits para o LDR (0-4095)

  // Configuração dos botões como entradas
  pinMode(BUTTON_P, INPUT_PULLUP);
  pinMode(BUTTON_K, INPUT_PULLUP);
  
  // Limpar o display inicialmente
  display.clearDisplay();
}

void loop() {
  // Adicionando um atraso de 1 segundo antes de ler o sensor
  delay(1000);
  
  // Ler valores do sensor DHT (temperatura e umidade)
  int temp = dht.readTemperature();  // Temperatura em Celsius
  int hum = dht.readHumidity();     // Umidade em %

  // Verificar se a leitura falhou
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Falha ao ler o sensor DHT!");
    return;
  }
  
  // Ler o valor do LDR (luminosidade)
  int ldr_value = analogRead(LDR_PIN);
  
  // Calcular o valor de LUX com base na leitura do LDR
  int lux_value = map(ldr_value, 0, 4095, LUX_MIN, LUX_MAX);  // Mapeando para uma faixa de 0 a 1000 LUX
  
  // Enviar os dados para o Monitor Serial
  Serial.print("Temp:"); 
  Serial.print(temp);    // Valor da temperatura
  Serial.print("\t");

  Serial.print("Umid:"); 
  Serial.print(hum);     // Valor da umidade
  Serial.print("\t");

  Serial.print("LUX:");  
  Serial.println(lux_value);  // Valor de LUX
  
  // Verifica o botão P
  if (digitalRead(BUTTON_P) == LOW) {  // Botão P pressionado
    display.setCursor(0, 30);    // Posiciona na linha 3
    display.print("Botao P press.");
    Serial.println("Botao P pressionado");
  }

  // Verifica o botão K
  if (digitalRead(BUTTON_K) == LOW) {  // Botão K pressionado
    display.setCursor(0, 40);    // Posiciona na linha 4
    display.print("Botao K press.");
    Serial.println("Botao K pressionado");
  }

  // Exibir temperatura, umidade e luminosidade na tela OLED
  display.setTextSize(1);      
  display.setTextColor(SSD1306_WHITE);
  
  display.setCursor(0, 0);    
  display.print("Temp: ");
  display.print(temp);
  display.print(" C");

  display.setCursor(0, 10);    
  display.print("Umid: ");
  display.print(hum);
  display.print(" %");

  display.setCursor(0, 20);    
  display.print("LUX: ");
  display.print(lux_value);

  display.display();
}
