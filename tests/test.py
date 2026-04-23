import cyberpi
stato_linea = cyberpi.quad_rgb_sensor.get_line_sta()
while True:
    print(stato_linea)