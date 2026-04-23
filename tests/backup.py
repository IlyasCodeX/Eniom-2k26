import cyberpi, time

mbot = cyberpi.mbot2
sensor = cyberpi.quad_rgb_sensor
colore = cyberpi.quad_rgb_sensor.get_color_sta

# Parametri di velocità
VEL_CROCIERA = 20
VEL_MAX = 50
ACCELERAZIONE = 2

# Parametri gap
DISTANZA_BASE = 3
RITORNO_VELOCITA = 20

# Variabili globali
current_speed = VEL_CROCIERA
tentativi_gap = 0

def gestisce_stato_linea(stato):
    global current_speed, tentativi_gap

    # ── ROSSO: stop immediato ─────────────────────────────────────────
        #return

    # ── VERDE: gestione direzione ──────────────────────────────────────
    sx_verde = colore("L2") == "green" or colore("L1") == "green"
    dx_verde = colore("R2") == "green" or colore("R1") == "green"

    if sx_verde:
        mbot.straight(2, speed=5)
        if sx_verde and dx_verde:
            mbot.turn(200)
        else:
            mbot.straight(5, speed= 15)
            mbot.turn(100)
    elif dx_verde:
        mbot.straight(2, speed=5)
        if sx_verde and dx_verde:
            mbot.turn(200)
        else:
            mbot.straight(5, speed= 15)
            mbot.turn(-100)
    elif sx_verde and dx_verde:
        mbot.forward(0)
        mbot.turn(200)
        

    # ── STATO LINEA ────────────────────────────────────────────────────
    if stato == 15:  # bianco → gestione gap
     #   mbot.drive_speed(-35,35)
    #else:
        #tentativi_gap = 0  # ha trovato la linea → reset!

        if stato == 9:  # dritto
            if mbot.read_digital(1) == 1:
                mbot.straight(50, speed=15)
            else:
                if current_speed < VEL_MAX:
                    current_speed += ACCELERAZIONE
                mbot.drive_speed(current_speed, -current_speed)

        elif stato in [11, 3]:  # sinistra
            current_speed = VEL_CROCIERA
            mbot.drive_speed(15, -30)

        elif stato == 13:  # destra
            current_speed = VEL_CROCIERA
            mbot.drive_speed(30, -15)

        elif stato == 12:
            mbot.turn_right(-40)

        elif stato == 8:  # 90 gradi destra
            mbot.straight(2, speed=20)
            mbot.turn(110)

        elif stato == 1:  # 90 gradi sinistra
            mbot.straight(2, speed=20)
            mbot.turn(-110)

        elif stato == 14:  # curva stretta destra
            mbot.drive_speed(50, -20)

        elif stato == 7:  # curva stretta sinistra
            mbot.drive_speed(10, -50)

    # ── OSTACOLO: sensore distanza ─────────────────────────────────────
    if cyberpi.ranging_sensor.get() <= 10:
        mbot.straight(-8, speed=20)
        mbot.turn(100)
        for _ in range(6):
            mbot.straight(10, speed=20)
            mbot.turn(-44)

# ── LOOP PRINCIPALE ────────────────────────────────────────────────────
while True:
    if colore("L1") == "red" or colore("R1") == "red":
        cyberpi.audio.play("beeps")
        mbot.forward(0)
    print(stato_linea)
    gestisce_stato_linea(stato_linea)