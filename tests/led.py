import cyberpi, time

while True:
    cyberpi.mbot2.motor_drive(100, 0)
    time.sleep(1)
    cyberpi.mbot2.motor_drive(100, 0)
    time.sleep(1)