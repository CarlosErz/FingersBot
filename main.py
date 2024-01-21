import customtkinter as tk
import serial.tools.list_ports
import cv2
from variables import *
from handa_fingers import *

# Configuración de la librería / Library configuration
tk.set_appearance_mode("dark") 
tk.set_default_color_theme("dark-blue") 
tk.deactivate_automatic_dpi_awareness()

# Configuración de la aplicación / App configuration
app = tk.CTk() 
app.geometry(WINDOWS_SIZE)
app.title(TITLE)
app.iconbitmap(ICON)
app.iconbitmap(ICON_BLANCO)
app.resizable(False, False)
app.config(bg="#080013")

# Centrar en la pantalla / Center in the screen
app.geometry(f"+{int(app.winfo_screenwidth()/2 - int(WINDOWS_SIZE.split('x')[0])/2)}+{int(app.winfo_screenheight()/2 - int(WINDOWS_SIZE.split('x')[1])/2)}")

# Funciones / Functions
def combobox_callback(choice):
    print("La cámara escogida es:", choice)

def combobox_callback_port(choice):
    print("El puerto escogido es:", choice)

def get_camera_names():
    camera_names = []
    cameras_found = False
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            camera_name = cap.get(cv2.CAP_PROP_POS_MSEC)
            camera_names.append(f"{i}")
            cap.release()
            cameras_found = True
    if not cameras_found:
        return ["No se encontraron cámaras"]

    return camera_names

def star_app():
    hands_funcion(puerto_com, camara, cantidad_servos, get_ports,  active_arduino)
    print("Iniciando")


def port_com_active():
    if switch_var.get() == "on":
        puerto_com = get_selected_com_port()
        print(switch_var.get())
    else:
        puerto_com = "No se encontraron puertos COM"
        print(switch_var.get())
        return False
    


def get_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    if not ports:
        return ["No se encontraron puertos COM"]
    return ports

# Etiqueta
label = tk.CTkLabel(app, text="CONFIGURACION DE FINGERS", font=("Arial", 18,"bold"), fg_color="#080013", text_color="white", anchor="center")
label.pack(padx=10, pady=20)

# Obtener nombres de cámaras
camera_names = get_camera_names()
label = tk.CTkLabel(app, text="Selecciona la cámara:", font=("Arial", 12), fg_color="#080013", text_color="white", anchor="center")
label.pack()

# Combobox camera
combobox = tk.CTkComboBox(app, values=camera_names, command=combobox_callback, width=200, height=30, font=("Arial", 12),
                          border_color="#19003A", fg_color="#080013", button_color="#19003A", text_color="white", dropdown_font=("Arial", 12), dropdown_fg_color="#19003A", dropdown_text_color="white")
combobox.set(camera_names[0])
combobox.pack(padx=10, pady=10)

switch_var = tk.StringVar(value=port_com_active)
witch = tk.CTkSwitch(app, text="CTkSwitch", command=port_com_active,
                                 variable=switch_var, onvalue="on", offvalue="off", state=tk.DISABLED if not get_ports() else tk.NORMAL)
switch_var.set("on")
witch.pack(padx=10, pady=10)

label = tk.CTkLabel(app, text="Selecciona el puerto:", font=("Arial", 12), fg_color="#080013", text_color="white", anchor="center")
label.pack()

# Combobox
ports = get_ports()
combobox_port = tk.CTkComboBox(app, values=ports, width=200, height=30, font=("Arial", 12), command=combobox_callback_port, fg_color="#080013", border_color="#19003A", button_color="#19003A", text_color="white", dropdown_font=("Arial", 12), dropdown_fg_color="#19003A", dropdown_text_color="white", state=tk.DISABLED if not ports else tk.NORMAL)
combobox_port.set(ports[0] if ports else "No se encontraron puertos COM")
combobox_port.pack(padx=10, pady=10)

button = tk.CTkButton(app, text="Iniciar", font=("Arial", 12), 
                      width=(200), fg_color="#080013", border_color="#2A0063", border_spacing=(10), 
                      hover_color="#2A0063", border_width=(2), text_color="white", command=star_app, anchor="center")
button.pack(side="bottom", padx=10, pady=10)

# Valor de comunicación a la mano / Value the communication to hands 
label = tk.CTkLabel(app, text="Cuantos Servos conectar:", font=("Arial", 12), fg_color="#080013", text_color="white", anchor="center")
label.pack()

def combobox_callback_servo(choice): 
    print('Valor del servo,', choice)
    value_choice = choice
    return value_choice

# Combobox
servo_combobox = tk.CTkComboBox(app, values=['5','3'], command=combobox_callback_servo, width=200, height=30, font=("Arial", 12),
                          border_color="#19003A", fg_color="#080013", button_color="#19003A", text_color="white", dropdown_font=("Arial", 12), dropdown_fg_color="#19003A", dropdown_text_color="white")
servo_combobox.set('3')
servo_combobox.pack(padx=10, pady=10)

def get_selected_camera():
    return combobox.get()

def get_selected_com_port():
    return combobox_port.get()

def get_selected_servos():
    return servo_combobox.get()

def active_arduino():
    return switch_var.get()


puerto_com = get_selected_com_port()  
camara = get_selected_camera()  
cantidad_servos = get_selected_servos() 
active_arduino = active_arduino()

app.mainloop()
