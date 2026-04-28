import cyberpi

colori = cyberpi.quad_rgb_sensor.get_color

while True:
    print(colori("L2"), colori("L1"), colori("R1"), colori("R2"))
    