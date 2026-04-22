import cyberpi, time

# NOTA IMPORTANTE:
# gli stati linea quando viene uploadato il 
# codice sono invertiti rispetto alla documentazione:
# 
# stato 0:
#   docs:
#       [N][N][N][N]
# 
#   stato effettivo:
#       [B][B][B][B]
#
# invece quando viene runnato normalmente (quindi con 
# il tasto "run") gli stati sono gli stessi delle docs
#
# link delle docs: 
# https://www.yuque.com/makeblock-help-center-en/mcode/cyberpi-api-mbuild

mbot = cyberpi.mbot2
sensor = cyberpi.quad_rgb_sensor
colore = cyberpi.quad_rgb_sensor.get_color_sta

# Parametri di velocità
VEL_CROCIERA = 5
VEL_MAX = 15
ACCELERAZIONE = 1.7

# Parametri gap
DISTANZA_BASE = 3
RITORNO_VELOCITA = 20

# Variabili globali
current_speed = VEL_CROCIERA

# Recupero linea
white_counter = 0
white_counter_threshold = 3.5

stato_precedente = None

def trovato_verde():
    return colore("L2") == "green" or colore("L1") == "green" or colore("R2") == "green" or colore("R1") == "green"
    
def gestisci_verde():
    sx_verde = colore("L2") == "green" or colore("L1") == "green"
    dx_verde = colore("R2") == "green" or colore("R1") == "green"
    
    if sx_verde and dx_verde:
        cyberpi.led.show("g g g g g")
        mbot.turn(270)
        mbot.straight(7, speed=15)
        cyberpi.led.off()
        return
    elif sx_verde:
        cyberpi.led.show("g g k k k")
        mbot.turn(-80)
        mbot.straight(6, speed=15)
        cyberpi.led.off()
        return
    elif dx_verde:
        cyberpi.led.show("k k k g g")
        mbot.turn(80)
        mbot.straight(6, speed=15)
        cyberpi.led.off()
        return

def recupero_linea():
    global white_counter, white_counter_threshold
    
    cyberpi.led.show("r r r r r")
    
    while True:
        mbot.forward(0)
    
        mbot.turn(-45)
    
        if sensor.get_line_sta() != 15:
            white_counter = 0
            cyberpi.led.off()
            return
    
        mbot.turn(90)
    
        if sensor.get_line_sta() != 15:
            white_counter = 0
            cyberpi.led.off()
            return
        
        mbot.turn(-45)
        
        if sensor.get_line_sta() != 15:
            white_counter = 0
            cyberpi.led.off()
            return
        
        mbot.straight(-5, 20)
        
        cyberpi.led.off()
        
    
    cyberpi.led.off()

def gestisce_stato_linea(stato, stato_precedente):
    global current_speed
    
    # ── ROSSO: stop immediato ──────────────────────────────────────────
    if colore("L1") == "red" or colore("R1") == "red" or colore("L2") == "red" or colore("R2") == "red":
        cyberpi.audio.play("beeps")
        mbot.forward(0)
        return
    
    # ── VERDE: gestione direzione ──────────────────────────────────────
    gestisci_verde()
    
    # ── STATO LINEA ────────────────────────────────────────────────────
    if stato == 9:  # dritto
        if mbot.read_digital(1) == 1:
            mbot.straight(50, speed=15)
        else:
            if current_speed < VEL_MAX:
                current_speed += ACCELERAZIONE
            mbot.drive_speed(current_speed, -current_speed)
    elif stato == 11:  # sinistra
        current_speed = VEL_CROCIERA
        mbot.drive_speed(15, -30)
    elif stato == 3:
        #current_speed = VEL_CROCIERA
        #mbot.drive_speed(5, -40)
        mbot.turn(-35)
    elif stato == 13:  # destra
        current_speed = VEL_CROCIERA
        mbot.drive_speed(30, -15)
    elif stato == 12:
        #mbot.drive_speed(50, -5)
        mbot.turn(35)
    elif stato == 8:  # 90 gradi destra
        mbot.straight(3, speed=20)
    
        if trovato_verde():
            mbot.straight(6, speed=20)
        else:
            mbot.turn(90)
    elif stato == 1:  # 90 gradi sinistra
        mbot.straight(3, speed=20)
        
        if trovato_verde():
            mbot.straight(6, speed=20)
        else:
            mbot.turn(-90)
    elif stato == 14:  # curva stretta destra
        mbot.turn(15)
        #mbot.drive_speed(110, -0)
    elif stato == 7:  # curva stretta sinistra
        mbot.turn(-15)
        #mbot.drive_speed(0, -110)
    elif stato == 5:
        mbot.turn(10)
    elif stato == 10:
        mbot.turn(-10)
    elif stato == 0:
        mbot.straight(5, 10)
    
    # ── OSTACOLO: sensore distanza ─────────────────────────────────────
    if cyberpi.ranging_sensor.get() <= 10:
        cyberpi.console.print("Faccio l'ostacolo...")
        cyberpi.led.show("y y y y y")
        mbot.straight(-8, speed=20)
        mbot.turn(100)
        for _ in range(3):
            mbot.straight(10, speed=20)
            mbot.turn(-44)
            stato = sensor.get_line_sta()
        cyberpi.console.clear()
        
        cyberpi.led.off()

# ── LOOP PRINCIPALE ────────────────────────────────────────────────────
while True:
    stato_linea = sensor.get_line_sta()
    
    if stato_linea == 15:
        while stato_linea == 15:
            if white_counter >= white_counter_threshold:
                white_counter = 0
                recupero_linea()
                break
            
            mbot.forward(15)
            white_counter += 0.1
            cyberpi.console.print(white_counter)
            cyberpi.console.clear()
            
            stato_linea = sensor.get_line_sta()
            
        if white_counter >= white_counter_threshold:
            white_counter = 0
            recupero_linea()
    else:
        white_counter = 0
        
        gestisce_stato_linea(stato_linea, stato_precedente)
            
    stato_precedente = stato_linea