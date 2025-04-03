from tkinter import messagebox
import ttkbootstrap as ttk
import tkinter as tk

class VentanaEmpresa(tk.Toplevel):
    def __init__(self, parent, empresa_singleton):
        super().__init__(parent)
        self.title("Información de la Empresa (Singleton)")

        # Recibimos la instancia única de la empresa
        self.empresa = empresa_singleton

        # Etiquetas con la información
        ttk.Label(self, text=f"NIT: {self.empresa.nit}").pack(pady=5)
        ttk.Label(self, text=f"Nombre: {self.empresa.nombre}").pack(pady=5)
        ttk.Label(self, text=f"Razón Social: {self.empresa.razon_social}").pack(pady=5)

        # Campos para ingresar nuevos valores
        frame_campos = ttk.Frame(self)
        frame_campos.pack(pady=10)

        # NIT
        ttk.Label(frame_campos, text="NIT nuevo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nit = ttk.Entry(frame_campos, width=25)
        self.entry_nit.grid(row=0, column=1, padx=5, pady=5)

        # Nombre
        ttk.Label(frame_campos, text="Nombre nuevo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = ttk.Entry(frame_campos, width=25)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        # Razón Social
        ttk.Label(frame_campos, text="Razón Social nueva:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_razon = ttk.Entry(frame_campos, width=25)
        self.entry_razon.grid(row=2, column=1, padx=5, pady=5)



        btn_nueva_instancia = ttk.Button(
            self,
            text="Intentar crear nueva instancia",
            command=self.intentar_crear_nueva_instancia
        )
        btn_nueva_instancia.pack(pady=10)




        # Llamada para centrar y definir el tamaño de la ventana
        self.centrar_ventana()



    def intentar_crear_nueva_instancia(self):
        """ 
        Crea (o intenta crear) otra instancia de EmpresaProTec con
        los valores ingresados en los campos de texto.
        Luego compara si es la misma que self.empresa.
        """
        from model.empresaProTec import EmpresaProTec  # Ajusta la ruta si corresponde

        # Tomamos los valores de los Entry
        nit_nuevo = self.entry_nit.get().strip()
        nombre_nuevo = self.entry_nombre.get().strip()
        razon_nueva = self.entry_razon.get().strip()

        # Intentamos crear otra instancia
        nueva_instancia = EmpresaProTec(nit_nuevo, nombre_nuevo, razon_nueva)

        # Comparamos si es la misma instancia que self.empresa
        if self.empresa is nueva_instancia:
            messagebox.showinfo(
                "Singleton",
                f"¡Sigue siendo la MISMA instancia!\n\n"
                f"ID actual: {id(self.empresa)}\n"
                f"ID 'nueva': {id(nueva_instancia)}\n\n"
                "El patrón Singleton funciona."
            )
        else:
            messagebox.showerror(
                "Singleton",
                "Se creó una instancia distinta (¡no debería pasar!)."
            )


    def centrar_ventana(self):
        """
        Ajusta la posición y tamaño inicial para que aparezca centrada en la pantalla.
        """
        # Asegura que tkinter calcule el layout antes de posicionar
        self.update_idletasks()

        # Aumenta el tamaño para que se aprecie el título en la barra
        ancho_ventana = 400
        alto_ventana = 400

        # Calcula coordenadas para centrar en la pantalla
        x = (self.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y = (self.winfo_screenheight() // 2) - (alto_ventana // 2)

        # Aplica la geometría resultante (dimensiones + posición)
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")