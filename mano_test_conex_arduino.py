import serial
import time

#ser = serial.Serial('COM4', 9600)

ciclo = True


while ciclo:
    
    print("1) Abrir la mano")
    print("2) Cerrar mano")
    print("3) Cerrar programa")
    opcion = input("Ingrese una opcion: ")

    if opcion == "1":
       # ser.write(b'1')
       print("op 1 ")
    elif opcion == "2":
        #ser.write(b'2')
        print("op2")
    elif opcion == "3":
        ciclo = False
    else:
        print("Opción no válida. Inténtalo de nuevo.")

    time.sleep(1)

#ser.close()




    
