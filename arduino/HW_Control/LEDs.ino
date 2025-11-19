/*
This file contains the functions for the LED control
*/
byte mapped_LEDs[] = { 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 }; //remapped depending on your hardware setup

void setLED(byte LED, bool state) {//turn a LED on or off
  if (state) {
    led_strip.setPixelColor(mapped_LEDs[LED], led_strip.Color(0, 0, 0, 255)); // Full white (W channel)
    // leds[LED] = CRGB(LED_c[0], LED_c[1], LED_c[2]);
  } else {
    led_strip.setPixelColor(mapped_LEDs[LED], led_strip.Color(0, 0, 0, 0)); // Full white (W channel)
  }
  led_strip.show();
}

void test_leds() {//blink all LEDs one by one
  for (byte i = 0; i < NUM_LEDS; i++){
    setLED(i, true);
    delay(200);
    setLED(i, false);
    delay(200);
  }
}

void init_leds() {
  led_strip.begin();
  led_strip.setBrightness(LED_b);  // global brightness
  led_strip.clear();
  led_strip.show();
}