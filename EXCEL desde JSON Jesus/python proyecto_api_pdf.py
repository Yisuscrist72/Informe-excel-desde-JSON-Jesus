import requests
import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys # Se importa para manejar la versión de Python en el caso del error de API

# --- 1. Configuración de la API y Obtención de Datos ---
API_URL = "https://dummyjson.com/products"

def obtener_datos_productos():
    """
    Función principal para consumir la API de dummyjson.
    Realiza una petición HTTP GET y maneja posibles errores de conexión o respuesta.
    Retorna la lista de productos o una lista vacía en caso de fallo.
    """
    try:
        print("Obteniendo datos de la API...")
        # Realizar la petición GET al endpoint
        response = requests.get(API_URL)
        # Verificar el código de estado HTTP (ej: si es 404 o 500, lanza una excepción)
        response.raise_for_status() 
        # Convertir la respuesta JSON a un diccionario Python
        data = response.json()
        # Retorna la lista de productos. Si 'products' no existe, retorna una lista vacía por seguridad.
        return data.get('products', []) 
    except requests.exceptions.RequestException as e:
        # Captura cualquier error de red o HTTP (Timeout, conexión rechazada, etc.)
        print(f"Error al obtener datos de la API: {e}")
        return []

# --- Variables Globales y Carga Inicial ---
# Carga inicial de todos los datos de la API. Se usa como fuente de verdad para el filtrado.
datos_completos = obtener_datos_productos() 
# Lista que contiene los datos que se muestran actualmente en la GUI (el resultado del filtrado).
datos_filtrados = datos_completos.copy() 

# --- 2. Funciones de Tkinter (GUI) y Lógica de Filtrado ---

def actualizar_lista_productos(lista_datos):
    """
    Función para actualizar el widget Listbox de Tkinter.
    Muestra los datos proporcionados en la lista de la interfaz.
    """
    # Limpiar todos los elementos actuales del Listbox
    lista_productos.delete(0, tk.END) 
    
    if not lista_datos:
        lista_productos.insert(tk.END, "No se encontraron productos.")
        return

    for item in lista_datos:
        # Formato de línea para mostrar en el Listbox (usando f-strings para alineación)
        # ID | Título (max 30 caracteres) | Precio ($) | Categoría
        linea = f"{item['id']:<4} | {item['title'][:30]:<30} | ${item['price']:<6} | {item['category']}"
        lista_productos.insert(tk.END, linea)

def filtrar_datos(event=None):
    """
    Función de filtrado. Se activa cada vez que se presiona una tecla en el campo de entrada.
    Busca coincidencias en los títulos o categorías de los productos.
    """
    global datos_filtrados
    # Obtener el texto del campo de filtro y convertirlo a minúsculas para una búsqueda sin distinción de mayúsculas
    criterio = entrada_filtro.get().lower() 

    if not criterio:
        # Si el campo está vacío, restaurar todos los datos
        datos_filtrados = datos_completos.copy()
    else:
        # Usar una lista por comprensión para filtrar: incluir el producto si el criterio
        # está en el título O en la categoría (ambos en minúsculas).
        datos_filtrados = [
            p for p in datos_completos 
            if criterio in p['title'].lower() or criterio in p['category'].lower()
        ]

    # Actualizar la interfaz con el resultado del filtrado
    actualizar_lista_productos(datos_filtrados)
    # Restaura el mensaje de estado al estilo por defecto e informa el conteo.
    status_label.config(text=f"Mostrando {len(datos_filtrados)} de {len(datos_completos)} productos.", style="TLabel")

# --- 3. Generación del PDF (Informe) ---

def generar_pdf():
    """
    Crea un documento PDF utilizando la librería ReportLab.
    El contenido del PDF son los datos actualmente guardados en 'datos_filtrados'.
    """
    if not datos_filtrados:
        # Usar el estilo de advertencia si no hay datos para generar el PDF
        status_label.config(text="⚠️ No hay datos filtrados para generar el PDF.", style="Advertencia.TLabel")
        return

    nombre_archivo = "informe_productos_filtrados.pdf"
    
    try:
        # Inicializa el objeto Canvas (lienzo) de ReportLab
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        ancho, alto = letter
        y_pos = alto - 50 # Posición inicial vertical para escribir

        # --- Contenido Estático (Título y Cabeceras) ---
        c.setFont("Helvetica-Bold", 16)
        c.drawString(30, y_pos, "🛒 Informe de Productos Filtrados")
        y_pos -= 30

        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y_pos, "ID")
        c.drawString(70, y_pos, "Título")
        c.drawString(350, y_pos, "Categoría")
        c.drawString(500, y_pos, "Precio ($)")
        y_pos -= 15
        
        # Línea horizontal para separar la cabecera del contenido
        c.line(30, y_pos, ancho - 30, y_pos)
        y_pos -= 15

        # --- Contenido Dinámico (Datos Filtrados) ---
        c.setFont("Helvetica", 10)
        for producto in datos_filtrados:
            # Control de salto de página: si la posición 'y' es muy baja, crea una nueva página
            if y_pos < 50:
                c.showPage() 
                y_pos = alto - 50 # Restablecer posición 'y'
                # Vuelve a dibujar las cabeceras en la nueva página
                c.setFont("Helvetica-Bold", 10)
                c.drawString(30, y_pos, "ID"); c.drawString(70, y_pos, "Título"); c.drawString(350, y_pos, "Categoría"); c.drawString(500, y_pos, "Precio ($)")
                y_pos -= 30
                c.setFont("Helvetica", 10)
            
            # Dibujar los datos del producto
            c.drawString(30, y_pos, str(producto['id']))
            c.drawString(70, y_pos, producto['title'][:40])
            c.drawString(350, y_pos, producto['category'])
            c.drawString(500, y_pos, f"${producto['price']:.2f}")
            y_pos -= 15 # Mover la posición vertical para la siguiente línea

        # Guardar y cerrar el documento PDF
        c.save() 
        # Mostrar mensaje de éxito en la GUI 
        status_label.config(text=f"✅ PDF '{nombre_archivo}' generado exitosamente.", style="Exito.TLabel")

    except Exception as e:
        # Mostrar mensaje de error si ReportLab falla al generar el PDF
        status_label.config(text=f"❌ Error al generar PDF: {e}", style="Error.TLabel") 


# --- 4. Configuración de la Interfaz Gráfica (Tkinter) ---

# 1. Ventana principal
root = tk.Tk()
root.title("Proyecto API, Tkinter y PDF")
root.geometry("800x600")

# 2. Configuración de Estilos de Tkinter
# Inicializa el sistema de estilos de Tkinter
style = ttk.Style() 
# Definimos estilos personalizados usando 'style.configure' para asignar colores
style.configure("Exito.TLabel", foreground="green")
style.configure("Error.TLabel", foreground="red")
style.configure("Advertencia.TLabel", foreground="orange")
# El estilo por defecto de ttk.Label es "TLabel"

# 3. Marco de Filtrado (Contiene el campo de texto y el botón de PDF)
frame_filtro = ttk.Frame(root, padding="10")
frame_filtro.pack(fill='x') # Rellena horizontalmente

ttk.Label(frame_filtro, text="Filtrar por Título o Categoría:").pack(side=tk.LEFT, padx=5)

# Campo de entrada para el filtro
entrada_filtro = ttk.Entry(frame_filtro, width=50)
entrada_filtro.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
# Conectar la función de filtrado al evento de liberar tecla (KeyRelease) para filtrar en tiempo real
entrada_filtro.bind("<KeyRelease>", filtrar_datos) 

# Botón para generar el PDF
ttk.Button(frame_filtro, text="Generar PDF", command=generar_pdf).pack(side=tk.RIGHT, padx=5)

# 4. Marco de la Lista de Productos (Contiene el Listbox y el Scrollbar)
frame_lista = ttk.Frame(root, padding="10")
frame_lista.pack(fill='both', expand=True) # Rellena todo el espacio restante

# Listbox: El widget que mostrará los datos tabulados
lista_productos = tk.Listbox(frame_lista, width=100, height=25, font=("Courier", 10))
lista_productos.pack(side="left", fill="both", expand=True)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=lista_productos.yview)
scrollbar.pack(side="right", fill="y")
# Conectar el Listbox al Scrollbar
lista_productos.config(yscrollcommand=scrollbar.set)

# 5. Etiqueta de Estado (Barra de estado en la parte inferior, inicializada sin estilo)
status_label = ttk.Label(root, text="", padding="5")
status_label.pack(fill='x')


# 6. Inicialización de la GUI
if datos_completos:
    # Si la carga de la API fue exitosa, mostrar los datos iniciales
    actualizar_lista_productos(datos_completos)
    # Establecer el estado inicial con el estilo por defecto "TLabel"
    status_label.config(text=f"Datos de la API cargados. Mostrando {len(datos_completos)} productos.", style="TLabel")
else:
    # Si hubo un error en la carga de la API, notificar con el estilo de error
    status_label.config(text="❌ Error: No se pudieron cargar los datos de la API. Verifique la conexión o instale 'requests'.", style="Error.TLabel")

# Iniciar el bucle principal de Tkinter
root.mainloop()