import cyberpi, time

KP = 2.2
KD = 8.5
VELOCITA_BASE = 10
VELOCITA_MAX = 30

def main():
    
    
    while True:
        print(cyberpi.quad_rgb_sensor.get_offset_track())
        
main()