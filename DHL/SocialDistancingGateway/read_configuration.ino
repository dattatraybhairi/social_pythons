void read_configuration()
{
  uint8_t time_out = 500;
  memset(sbuf, 0, sizeof(sbuf));
  
  //while (Serial.available())
  //  uint8_t dummy_data = Serial.read();

  currentMillis = millis();
  while ((Serial.available() < 2) && (millis() - currentMillis < time_out))
  {
    yield();
  }

  //Serial.print("\nSA:");
  //Serial.println(Serial.available());
  
  if (Serial.available())
    for (int i = 0; i < 2; i++)
      sbuf[i] = Serial.read();

  //Serial.println();

//  for (int i = 0; i < 5; i++)
//  {
//    Serial.print(sbuf[i]);
//    Serial.print(" ");
//  }
}
