# --- EXAMPLES ----
# pwmBuzzer_D20 = buzzer_get('D20')
# pwmBuzzer_D20.duty_u16(95)

# ledButton_D20 = led_button_get('D20')
# while True:
#     x = ledButton_D20.button_in()
#     print(x)
#     ledButton_D20.LED_out(x)

# motion_sensor_D20 = motion_sensor_get('D20')
# while True:
#     x = motion_sensor_D20.value()
#     print(x)

# loudness_sensor_A2 = analog_sensor_get('A2')
# while True:
#     x = loudness_sensor_A2.read_u16()
#     print(x)

# light_sensor_A2 = analog_sensor_get('A2')
# while True:
#     x = light_sensor_A2.read_u16()
#     print(x)

# ultrasonic_D20 = ultrasonic_get('D20')
# while True:
#     x = ultrasonic_D20.MeasureInCentimeters()
#     print(x)

# Chainable LED
# red = (16, 0, 0)
# white = (255, 255, 255)
# chainable_LED_D18 = chainable_LED_get('D20')
# chainable_LED_D18.fill(white)
# red = (16, 0, 0)
# white = (255, 255, 255)
# while True:
# #    print("1")
#     chainable_LED_D18.fill(white)
#     time.sleep(1)
# #    print("2")
#     chainable_LED_D18.fill((16,0,0))
#     time.sleep(1)
# #    print("3")
#     chainable_LED_D18.fill((0,16,0))
#     time.sleep(1)
# #    print("4")
#     chainable_LED_D18.fill((0,0,16))
#     time.sleep(1)
# #    print("5")
