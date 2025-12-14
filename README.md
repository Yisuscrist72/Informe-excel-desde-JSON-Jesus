# 🛒 Proyecto Python: Gestión de Productos (API, Tkinter y PDF)

Este repositorio contiene una aplicación de escritorio desarrollada en Python que permite consumir datos de una API externa, filtrarlos mediante una interfaz gráfica (GUI) creada con Tkinter, y generar un informe en formato PDF con los resultados filtrados.

## 🌟 Características Principales

* **Consumo de API:** Obtiene datos en tiempo real de la API de productos de [dummyjson.com](https://dummyjson.com/).
* **Interfaz Gráfica:** Utiliza **Tkinter** para proporcionar una ventana intuitiva donde visualizar y manipular los datos.
* **Filtrado Rápido:** Permite buscar y filtrar productos por **título** o **categoría** en tiempo real.
* **Generación de Informes:** Crea un archivo **PDF** (usando ReportLab) con un listado detallado de los productos que cumplen con el criterio de filtrado actual.

## 🛠️ Tecnologías y Librerías Utilizadas

El proyecto fue desarrollado usando las siguientes librerías de Python:

| Tecnología | Propósito |
| :--- | :--- |
| `requests` | Realizar peticiones HTTP (GET) a la API. |
| `tkinter` (`ttk`) | Construcción de la Interfaz Gráfica de Usuario (GUI). |
| `reportlab` | Creación y formato del documento PDF (informe). |

## 🚀 Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Requisitos

Asegúrate de tener **Python 3.x** instalado.

### 2. Clonar el Repositorio

```bash
git clone <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
