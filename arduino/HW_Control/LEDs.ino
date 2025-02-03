/*
This file contains the functions for the LED control
*/


void setLED(byte LED, bool state) {//turn a LED on or off
  if (state) {
    leds[LED] = CRGB(LED_c[0], LED_c[1], LED_c[2]);
  } else {
    leds[LED] = CRGB(0,0,0);
  }
  FastLED.show();
}


void init_leds() {//initialise all LEDs
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(LED_b);
  FastLED.clear();
  FastLED.show();
}


void test_leds() {//blink all LEDs one by one
  for (byte i = 0; i < NUM_LEDS; i++){
    setLED(i, true);
    delay(200);
    setLED(i, false);
    delay(200);
  }
}
