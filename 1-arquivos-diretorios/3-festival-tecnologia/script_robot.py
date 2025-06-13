# Script para Robô Seguidor de Linha
import RPi.GPIO as GPIO
sensor_esq = 18
sensor_dir = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_esq, GPIO.IN)
GPIO.setup(sensor_dir, GPIO.IN)
def seguir_linha():
    if GPIO.input(sensor_esq) == 0:
        print("Vira à direita")
    elif GPIO.input(sensor_dir) == 0:
        print("Vira à esquerda")
    else:
        print("Seguir em frente")