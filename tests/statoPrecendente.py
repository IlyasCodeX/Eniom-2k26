import cyberpi

mbot = cyberpi.mbot2

stato_linea = cyberpi.quad_rgb_sensor.get_line_sta
stato_precedente = None
stato_attuale = None


while True:
    stato_attuale = stato_linea()
    
    print(f"stato attuale: {stato_attuale}")
    print(f"stato precedente: {stato_precedente}")
    
    if stato_attuale == 4:
        mbot.turn(-20)
        if stato_precedente == 6 or stato_precedente == 2 or stato_precedente == 4:
            mbot.straight(13)
    
    if stato_attuale == 2:
        mbot.turn(20)
        if stato_precedente == 6 or stato_precedente == 2 or stato_precedente == 4:
            mbot.straight(13)
    
    if stato_attuale == 0:
        if stato_precedente == 6 or stato_precedente == 2 or stato_precedente == 4:
            mbot.straight(13)
    
    if stato_attuale == 6:
        mbot.forward(10)
    else:
        mbot.forward(0)
    
    stato_precedente = stato_attuale