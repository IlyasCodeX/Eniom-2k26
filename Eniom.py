import cyberpi, time

"""
Questo è il codice principale del line follower di Eniom,
il robot che abbiamo usato alla robocup non usa il PID perché
non c'è stato tempo di implementarlo, ma invece controlla ogni stato
e fa delle azioni di conseguenza, usa dei led per segnalare
quando ha trovato il verde, l'ostacolo oppure quando parte
l'algoritmo di ricerca della linea.

Al robot sono collegati dei led, quelli servono per avere una illuminazione
migliore nei sensori.

l'algoritmo di ricerca della linea funziona in questo modo (pseudo codice):

```py
funzione recupero_linea():
    Imposta LED rossi

    Ripeti all'infinito:
        
        Ferma il robot
        
        Ruota leggermente a sinistra (-45°)
        
        Se la linea viene trovata:
            Resetta contatore bianco
            Spegni LED
            Termina funzione
        
        Ruota a destra (+90° rispetto alla posizione attuale)
        
        Se la linea viene trovata:
            Resetta contatore bianco
            Spegni LED
            Termina funzione
        
        Ruota di nuovo a sinistra (-45°) per tornare al centro
        
        Se la linea viene trovata:
            Resetta contatore bianco
            Spegni LED
            Termina funzione
        
        Muovi il robot indietro

Inizializza contatore_bianco a 0
Imposta soglia_contatore_bianco a 3.5

Ripeti all'infinito:
    Leggi stato_linea dal sensore

    Se stato_linea è uguale a 15 (linea non rilevata / tutto bianco):
        Finché stato_linea rimane 15:
            Se contatore_bianco è maggiore o uguale alla soglia:
                Resetta contatore_bianco a 0
                Chiama funzione recupero_linea()
        
                Esci dal ciclo interno
            
            Muovi il robot in avanti a velocità 15
            Incrementa contatore_bianco di 0.1
        
            Stampa il valore del contatore
            Pulisci la console
            
            Aggiorna stato_linea leggendo di nuovo il sensore
        
        Dopo il ciclo:
            Se contatore_bianco ha raggiunto o superato la soglia:
                Resetta contatore_bianco a 0
                Chiama funzione recupero_linea()
```

---

NOTA IMPORTANTE:
gli stati linea quando viene uploadato il 
codice sono invertiti rispetto alla documentazione:

stato 0:
  docs:
      [N][N][N][N]

  stato effettivo:
      [B][B][B][B]

invece quando viene runnato normalmente (quindi con 
il tasto "run") gli stati sono gli stessi delle docs

link delle docs: 
https://www.yuque.com/makeblock-help-center-en/mcode/cyberpi-api-mbuild
"""

mbot = cyberpi.mbot2
sensor = cyberpi.quad_rgb_sensor
colore = cyberpi.quad_rgb_sensor.get_color_sta

verde = cyberpi.quad_rgb_sensor.get_green
rosso = cyberpi.quad_rgb_sensor.get_red
blu = cyberpi.quad_rgb_sensor.get_blue

# Parametri di velocità
VEL_CROCIERA = 5
VEL_MAX = 15
ACCELERAZIONE = 3

# Parametri gap
DISTANZA_BASE = 3
RITORNO_VELOCITA = 20

# Variabili globali
current_speed = VEL_CROCIERA

# Recupero linea
white_counter = 0
white_counter_threshold = 3.5

stato_precedente = None

# Range verdi: per una migliore ricognizione del verde
# Ecco i valori catturati dal robot:
# Destra:
#   rosso = 63.201
#   verde = 246.067
#   blu = 110.155
verde_minimo_rosso_destra = 43
verde_minimo_verde_destra = 226
verde_minimo_blu_destra = 80

verde_massimo_rosso_destra = 80
verde_massimo_verde_destra = 255
verde_massimo_blu_destra = 130

# Sinistro:
#   rosso = 99.832
#   verde = 254.909
#   blu = 150.117
verde_minimo_rosso_sinistra = 79
verde_minimo_verde_sinistra = 234
verde_minimo_blu_sinistra = 130

verde_massimo_rosso_sinistra = 119
verde_massimo_verde_sinistra = 255
verde_massimo_blu_sinistra = 170

# Così  è sicuro che i led sono spenti all'accensione del robot
cyberpi.led.off()

def compreso(valore, minimo, massimo):
    return minimo <= valore <= massimo

def verde_sinistra():
    return (
        (
            compreso(rosso("L2"), verde_minimo_rosso_sinistra, verde_massimo_rosso_sinistra)
            and compreso(verde("L2"), verde_minimo_verde_sinistra, verde_massimo_verde_sinistra)
            and compreso(blu("L2"), verde_minimo_blu_sinistra, verde_massimo_blu_sinistra)
        )
            or
        (
            compreso(rosso("L1"), verde_minimo_rosso_sinistra, verde_massimo_rosso_sinistra)
            and compreso(verde("L1"), verde_minimo_verde_sinistra, verde_massimo_verde_sinistra)
            and compreso(blu("L1"), verde_minimo_blu_sinistra, verde_massimo_blu_sinistra)
        )
    )

def verde_destra():
    return (
        (
            compreso(rosso("R2"), verde_minimo_rosso_sinistra, verde_massimo_rosso_sinistra)
            and compreso(verde("R2"), verde_minimo_verde_sinistra, verde_massimo_verde_sinistra)
            and compreso(blu("R2"), verde_minimo_blu_sinistra, verde_massimo_blu_sinistra)
        )    
            or
        (
            compreso(rosso("R1"), verde_minimo_rosso_sinistra, verde_massimo_rosso_sinistra)
            and compreso(verde("R1"), verde_minimo_verde_sinistra, verde_massimo_verde_sinistra)
            and compreso(blu("R1"), verde_minimo_blu_sinistra, verde_massimo_blu_sinistra)
        )        
    )

def trovato_verde():
    return verde_destra() or verde_sinistra()
    
def doppioverde():
    cyberpi.led.show("g g g g g")
    mbot.turn(270)
    mbot.straight(7, speed=15)
    cyberpi.led.off()
    
def trovato_linea():
    return sensor.get_line_sta() != 15

def gestisci_verde():
    if verde_sinistra() and verde_destra():
        doppioverde()
        
        return
    elif verde_sinistra():
        mbot.straight(0.9, speed=5)
        
        if verde_destra():
            doppioverde()
            
            return
        else:
            cyberpi.led.show("g g k k k")
            mbot.turn(-80)
            mbot.straight(6, speed=15)
            cyberpi.led.off()
            return
    elif verde_destra():
        mbot.straight(0.9, speed=5)
        
        if verde_sinistra():
            doppioverde()
            
            return
        else:
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
    
        if trovato_linea():
            white_counter = 0
            cyberpi.led.off()
    
            return
    
        mbot.turn(90)
    
        if trovato_linea():
            white_counter = 0
            cyberpi.led.off()

            return
        
        mbot.turn(-45)
        
        if trovato_linea():
            white_counter = 0
            cyberpi.led.off()

            return
        
        mbot.straight(-5, 20)

def gestisce_stato_linea(stato, stato_precedente):
    global current_speed
    
    # ── ROSSO: stop immediato ──────────────────────────────────────────
    if colore("L1") == "red" or colore("R1") == "red" or colore("L2") == "red" or colore("R2") == "red":
        cyberpi.audio.play("beeps")
        mbot.forward(0)
        
        cyberpi.led.show("c c c c c")
        
        return
    
    # ── VERDE: gestione direzione ──────────────────────────────────────
    if trovato_verde():
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
        mbot.turn(-35)
    elif stato == 13:  # destra
        current_speed = VEL_CROCIERA
        mbot.drive_speed(30, -15)
    elif stato == 12:
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
    elif stato == 7:  # curva stretta sinistra
        mbot.turn(-15)
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