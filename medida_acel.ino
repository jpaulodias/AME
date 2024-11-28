// Inclusão da biblioteca para comunicação I2C
#include<Wire.h>

// Endereço do sensor MPU 6050 em hexadecimal
const int MPU=0x68;  

// Variáveis para armazenar as medições do sensor
float acelX, acelY, acelZ, temp, girX, girY, girZ;

// Variáveis para armazenar os offsets da calibração
const int acelX_ = 0;
const int acelY_ = 0;
const int acelZ_ = -2048;

// Fator de correção das medidas conforme o fundo de escala escolhido
//   Acelerômetro
//   +/-2g = 16384
//   +/-4g = 8192
//   +/-8g = 4096
//   +/-16g = 2048

const int esc_acel = 2048;

// Definição do intervalo de análise (milissegundos)
const unsigned long delaySrl = 3000; // Delay para alternar entre o monitor serial da IDE do Arduino e o programa de terminal no qual o log será copiado
const unsigned long intervaloDeAnalise = 10000 + delaySrl; // Tempo de análise (10 s) + delay (3 s)

void setup()
{
  // Inicializa a comunicação serial
  Serial.begin(57600);
  // delay(10000);

  // Inicializa o MPU 6050
  Wire.begin();
  Wire.beginTransmission(MPU);
  Wire.write(0x6B); 
  Wire.write(0); 
  Wire.endTransmission(true);

  // Configura o giroscópio para o fundo de escala desejado
  
  /*
    Wire.write(0b00000000); // fundo de escala em +/-250°/s
    Wire.write(0b00001000); // fundo de escala em +/-500°/s
    Wire.write(0b00010000); // fundo de escala em +/-1000°/s
    Wire.write(0b00011000); // fundo de escala em +/-2000°/s
  */

  Wire.beginTransmission(MPU);
  Wire.write(0x1B);
  Wire.write(0b00000000);  // Trocar esse comando para o fundo de escala desejado conforme comentário acima
  Wire.endTransmission();

  // Configura o acelerômetro para o fundo de escala desejado

  /*
      Wire.write(0b00000000); // fundo de escala em +/-2g
      Wire.write(0b00001000); // fundo de escala em +/-4g
      Wire.write(0b00010000); // fundo de escala em +/-8g
      Wire.write(0b00011000); // fundo de escala em +/-16g
  */

  Wire.beginTransmission(MPU);
  Wire.write(0x1C);
  Wire.write(0b00011000);  // Trocar esse comando para o fundo de escala desejado conforme comentário acima
  Wire.endTransmission();

  delay(delaySrl);
}

void loop()
{
  // Tempo passado desde o início da rodada (milissegundos)
  unsigned long t = millis();

  // Começa uma transmissão com o sensor
  Wire.beginTransmission(MPU);

  // Enfileira os bytes a serem transmitidos para o sensor
  // Começando com o registro 0x3B
  Wire.write(0x3B);

  // Finaliza e transmite os dados para o sensor. O "false" fará com que seja enviado uma mensagem 
  // de restart e o barramento não será liberado
  Wire.endTransmission(false);
  
  // Solicita os dados do sensor em 14 bytes. O "true" fará com que o barramento seja liberado após
  // a solicitação (o valor padrão deste parâmetro é true)
  Wire.requestFrom(MPU, 14, true);  
  
  // Armazena o valor dos sensores nas variaveis correspondentes
  acelX = Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)  
  acelY = Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)  
  acelZ = Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)  
 
  temp = Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)

  girX = Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)     
  girY = Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  girZ = Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  // Imprime as medições no monitor serial caso a variável t esteja dentro do intervalo de análise
  if (t < intervaloDeAnalise) {
    // Imprime o tempo passado até o loop atual
    Serial.print(t - delaySrl);
    Serial.print(",");

    // // Imprime o valor X do acelerômetro na serial
    // Serial.print("X:"); 
    // Serial.print((acelX - acelX_) / esc_acel);
    // Serial.print(",");
  
    // // Imprime o valor Y do acelerômetro na serial
    // Serial.print("Y:"); 
    // Serial.print((acelY - acelY_)/ esc_acel);
    // Serial.print(",");
    
    // // Imprime o valor Z do acelerômetro na serial
    // Serial.print("Z:"); 
    Serial.println((acelZ - acelZ_) / esc_acel);
    // Serial.println("");

    //  // Imprime o valor X do giroscópio na serial
    //  Serial.print("X:"); 
    //  Serial.print((girX - girX_) / 131);
      
    //  // Imprime o valor Y do giroscópio na serial
    //  Serial.print("Y:"); 
    //  Serial.print((girY - girY_) / 131);
      
    //  // Imprime o valor Z do giroscópio na serial
    //  Serial.print("Z:"); 
    //  Serial.println((girZ - girZ_) / 131); 
      
    //  // Imprime o valor da temperatura na serial, calculando em graus celsius
    //  Serial.print("T:"); 
    //  Serial.print(temp / 340.00 + 36.53);
    //  Serial.println("\n");
  }
   
  // delay(100);

  // Serial.println(t);
}
