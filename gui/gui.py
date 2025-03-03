import customtkinter as tk
import threading 
from tkinter import messagebox
import serial.tools.list_ports
from Config import WINDOWS_SIZE, TITLE, ICON_BLANCO, codigo_arduino
from image_processing import image_processing

class GUI:
    def __init__(self):
        self.app = tk.CTk()
        self.configure_app()
        self.create_widgets()
        self.set_initial_values()

    def configure_app(self):
        self.app.geometry(WINDOWS_SIZE)
        self.app.title(TITLE)
        self.app.iconbitmap(ICON_BLANCO)
        self.app.resizable(False, False)
        self.app.config(bg="#080013")
        self.app.geometry(f"+{int(self.app.winfo_screenwidth()/2 - int(WINDOWS_SIZE.split('x')[0])/2)}+{int(self.app.winfo_screenheight()/2 - int(WINDOWS_SIZE.split('x')[1])/2)}")

    def create_widgets(self):
        self.create_labels()
        self.create_comboboxes()
        self.create_switch()
        self.create_buttons()

    def create_labels(self):
        tk.CTkLabel(self.app, text="CONFIGURACIÓN DE FINGERS", font=("Arial", 18, "bold"), fg_color="#080013", text_color="white", anchor="center").pack(padx=10, pady=20)
        tk.CTkLabel(self.app, text="Selecciona la cámara:", font=("Arial", 12), fg_color="#080013", text_color="white", anchor="center").pack()
        
    def create_comboboxes(self):
        """Crea los combobox para seleccionar cámaras y puertos COM con carga en segundo plano."""
        self.camera_names = ["Buscando cámaras..."]
        self.combobox_camera = tk.CTkComboBox(self.app, values=self.camera_names, command=self.combobox_callback, width=200, height=30, font=("Arial", 12), border_color="#19003A", fg_color="#080013", button_color="#19003A", text_color="white", dropdown_font=("Arial", 12), dropdown_fg_color="#19003A", dropdown_text_color="white")
        self.combobox_camera.pack(padx=10, pady=10)

        tk.CTkLabel(self.app, text="Selecciona el puerto COM:", font=("Arial", 12), fg_color="#080013", text_color="white", anchor="center").pack()

        self.ports = ["Buscando puertos..."]
        self.combobox_port = tk.CTkComboBox(self.app, values=self.ports, width=200, height=30, font=("Arial", 12), command=self.combobox_callback_port, fg_color="#080013", border_color="#19003A", button_color="#19003A", text_color="white", dropdown_font=("Arial", 12), dropdown_fg_color="#19003A", dropdown_text_color="white", state=tk.DISABLED)
        self.combobox_port.pack(padx=10, pady=10)

        # 🔥 Ejecutar carga en segundo plano
        threading.Thread(target=self.load_camera_names, daemon=True).start()
        threading.Thread(target=self.load_ports, daemon=True).start()

    def load_camera_names(self):
        """Carga las cámaras en segundo plano y actualiza el combobox."""
        self.camera_names = self.get_camera_names()
        self.combobox_camera.configure(values=self.camera_names)
        self.combobox_camera.set(self.camera_names[0])

    def load_ports(self):
        """Carga los puertos en segundo plano y actualiza el combobox."""
        self.ports = self.get_ports()
        self.combobox_port.configure(values=self.ports)
        self.combobox_port.set(self.ports[0] if self.ports else "No se encontraron puertos COM")
        self.combobox_port.configure(state=tk.NORMAL)  # Habilitar el combobox después de la carga

    def create_switch(self):
        self.switch_var = tk.StringVar(value=self.port_com_active)
        self.switch = tk.CTkSwitch(self.app, text="Puerto activo", command=self.port_com_active, variable=self.switch_var, onvalue="on", offvalue="off", state=tk.DISABLED if not self.ports else tk.NORMAL)
        self.switch_var.set("on")
        self.switch.pack(padx=10, pady=10)

    def create_buttons(self):
        tk.CTkButton(self.app, text="Iniciar", font=("Arial", 12), width=200, fg_color="#080013", border_color="#2A0063", border_spacing=10, hover_color="#2A0063", border_width=2, text_color="white", command=self.star_app, anchor="center").pack(side="bottom", padx=10, pady=10)
        tk.CTkButton(self.app, text="Copiar código arduino", font=("Arial", 12), width=200, fg_color="#080013", border_color="#2A0063", border_spacing=10, hover_color="#2A0063", border_width=2, text_color="white", command=self.copiCode, anchor="center").pack(side="bottom", padx=10, pady=10)

    def set_initial_values(self):
        self.puerto_com = self.get_selected_com_port()
        self.camara = self.get_selected_camera()
        self.active_arduino = self.active_arduino()

    def get_camera_names(self):
        """Obtiene la lista de cámaras disponibles en segundo plano."""
        import cv2
        camera_names = []
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_names.append(f"{i}")
                cap.release()
        return camera_names if camera_names else ["No se encontraron cámaras"]

    def combobox_callback(self, choice):
        print("La cámara escogida es:", choice)

    def combobox_callback_port(self, choice):
        print("El puerto escogido es:", choice)

    def port_com_active(self):
        if self.switch_var.get() == "on":
            self.puerto_com = self.get_selected_com_port()
            print(self.switch_var.get())
        else:
            self.puerto_com = "No se encontraron puertos COM"
            print(self.switch_var.get())
            return False

    def star_app(self):
        """Inicia la detección de manos, asegurando que la cámara sea un número válido"""
        if self.camara == "Buscando cámaras..." or not self.camara.isdigit():
            self.camara = "0"  # 🔥 Si aún no se detectan cámaras, usar la cámara 0
            messagebox.showwarning("Advertencia", "No se detectaron cámaras, usando cámara 0 por defecto.")

        procesamiento_imagen = image_processing(self.puerto_com, int(self.camara), self.get_ports, self.active_arduino)
        procesamiento_imagen.hands_funcion()


    def get_ports(self):
        """Obtiene los puertos COM disponibles en segundo plano."""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports if ports else ["No se encontraron puertos COM"]

    def copiCode(self):
        arduino = codigo_arduino
        self.app.clipboard_append(arduino)
        self.app.update()
        messagebox.showinfo("Código Copiado", "El código ha sido copiado al portapapeles.")
        self.app.after(2000)

    def get_selected_camera(self):
        return self.combobox_camera.get()

    def get_selected_com_port(self):
        return self.combobox_port.get()

    def active_arduino(self):
        return self.switch_var.get()

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
