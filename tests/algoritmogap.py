import cyberpi

white_counter = 0
sensor = cyberpi.quad_rgb_sensor
white_counter_threshold = 5
stato_linea = sensor.get_line_sta
mbot = cyberpi.mbot2

def recupero_linea():
    global white_counter, white_counter_threshold
    
    while True:
        mbot.forward(0)
    
        mbot.turn(-45)
    
        if sensor.get_line_sta() != 15:
            white_counter = 0
            return
    
        mbot.turn(90)
    
        if sensor.get_line_sta() != 15:
            white_counter = 0
            return
        
        mbot.turn(-45)
        
        if sensor.get_line_sta() != 15:
            white_counter = 0
            return
        
        mbot.straight(-5, 20)
    
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
            cyberpi.console.print("Recupero linea")
    else:
        white_counter = 0
        
        if stato_linea == 9:
            mbot.forward(15)
        
    cyberpi.console.print(white_counter)
    cyberpi.console.clear()