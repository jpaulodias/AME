# Análise modal experimental (AME) usando Arduino e MPU6050
O MPU6050 é uma unidade de medida inercial (IMU, na sigla em inglês) que utiliza sistemas microeletromecânicos (MEMS) para medir acelerações lineares e velocidades angulares.

Quando estacionário, ele mede a aceleração da gravidade e com um pouco de trigonometria é possível encontrar as direções em que seus eixos estão apontando. Isso pode ser usado para subtrair as componentes gravitacionais e manter apenas as inerciais quando em movimento linear.

Contudo, é importante atentar que, se o sensor também girar, a compensação da gravidade se torna complicada. As medições do acelerômetro e do giroscópio precisam ser fundidas, o que exige um tratamento mais elaborado. No entanto, para aplicações com rotações desprezíveis (como a apresentada a seguir), o processo é bem simples e o MPU6050 funciona perfeitamente. Com isso em mente, conectei os códigos desta pasta permitem medir a frequência natural de uma viga engastada-livre com uma massa adicional concentrada na ponta (equivalente à massa do sensor).
