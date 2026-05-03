# Duel Helper

Duel Helper is a desktop tool that detects images on screen and automatically clicks them. Load one or more reference images (*templates*), configure the search area and parameters, and the program handles detection and clicking while you do other things.

> *Duel Helper es una herramienta de escritorio que detecta imágenes en pantalla y hace clic sobre ellas automáticamente. Cargás una o varias imágenes de referencia (templates), configurás el área de búsqueda y los parámetros, y el programa se encarga de detectarlas y clickearlas mientras seguís haciendo otras cosas.*

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red?style=flat-square&logo=opencv)

---

## Features / Funciones

**Templates**
- Load existing PNG/JPG/BMP images as templates; the program copies them automatically to its working directory. / *Cargá imágenes PNG/JPG/BMP existentes como templates; el programa las copia automáticamente a su directorio de trabajo.*
- Create templates directly from the app by drawing a selection over a screen overlay. / *Creá templates directamente desde la app seleccionando un área de la pantalla sobre un overlay.*
- Reorder templates with drag-and-drop. Order determines detection priority. / *Reordenás los templates con drag-and-drop. El orden determina la prioridad de detección.*
- Each template can be individually enabled or disabled with a double-click. / *Cada template puede habilitarse o deshabilitarse individualmente con doble clic.*

**Per-template settings / Configuración por template**
- **Custom accuracy / Precisión propia**: match threshold independent from the global one. / *Umbral de coincidencia independiente del global.*
- **Cooldown**: minimum wait time between two clicks on the same template. / *Tiempo mínimo entre dos clics sobre el mismo template.*
- **Max clicks / Máximo de clics**: per-session click limit for that template. / *Límite de clics por sesión para ese template.*
- **Stop after N clicks**: automatically stops the helper after N clicks on this template. / *Detiene el helper automáticamente al llegar a N clics.*

**Presets**
- Save and load named template lists. / *Guardás y cargás listas de templates con nombre.*
- The last used preset is remembered on next launch. / *Se recuerda el último preset usado al abrir la app.*

**Main settings / Configuración principal**
- **Global accuracy / Precisión global** (0–1): how close the match must be. Adjustable with a slider. / *Qué tan exacta debe ser la coincidencia. Ajustable con un slider.*
- **Scan interval / Intervalo de escaneo**: time range between scans (min/max in seconds). / *Rango de tiempo entre búsquedas (mín/máx en segundos).*
- **Mouse move time / Tiempo de movimiento del mouse**: duration of the cursor movement. / *Duración del movimiento del cursor.*

**Extra options / Opciones extra**
- **Multi-monitor**: choose which screen to watch from a descriptive dropdown. / *Elegís en qué pantalla buscar desde un menú con nombres descriptivos.*
- **Search area / Área de búsqueda**: restrict detection to a specific screen region. / *Restringís la detección a una región específica de la pantalla.*
- **Auto-stop by time / Detención por tiempo**: the helper stops automatically after N minutes. / *El helper se detiene solo después de N minutos.*
- **Global click limit / Límite global de clics**: stops after N total clicks in the session. / *Se detiene al alcanzar N clics en total.*
- **Random idle breaks / Pausas aleatorias**: simulates human behavior with periodic breaks. / *Simula comportamiento humano con descansos periódicos.*
- **Configurable hotkey / Hotkey configurable**: pause/resume from any app with a configurable key. / *Pausar/reanudar desde cualquier app con una tecla a elección.*

**Human-like behavior / Comportamiento humano**
- Mouse movements include overshooting, easing, and random variation. / *Movimientos del mouse con overshooting, easing y variación aleatoria.*
- Variable delay before each click. / *Delay variable antes de cada clic.*
- Click point jitter within the target area. / *Jitter en el punto de clic dentro del target.*

**Interface / Interfaz**
- UI in English and Spanish, switchable at runtime from the menu. / *Interfaz en inglés y español, cambiable en tiempo de ejecución.*
- Activity log with timestamps and a clear button. / *Log de actividad con timestamps y botón para limpiar.*
- Session summary on stop: total clicks, runtime, and per-template breakdown. / *Resumen al finalizar con clics totales, tiempo de sesión y desglose por template.*

---

## Installation / Instalación

### Executable (recommended) / Ejecutable (recomendado)

Download `DuelHelper.exe` from the [Releases](../../releases) section. No Python or dependencies required — it's a portable executable that works on its own.

*Descargá el archivo `DuelHelper.exe` desde la sección [Releases](../../releases). No requiere Python ni ninguna dependencia instalada — es un ejecutable portátil que funciona por sí solo.*

### From source / Desde el código fuente

```bash
# 1. Clone the repository / Clonar el repositorio
git clone https://github.com/TU_USUARIO/DuelHelper.git
cd DuelHelper

# 2. Create virtual environment (recommended) / Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies / Instalar dependencias
pip install -r requirements.txt

# 4. Run / Ejecutar
python DuelHelper.py
```

> **macOS/Linux:** `pyautogui` may require accessibility permissions for mouse control. / *`pyautogui` puede requerir permisos de accesibilidad para controlar el mouse.*

---

## Usage / Uso

1. **Add templates / Agregar templates** — Click *Add Template* to load an existing image, or *Create Template* to capture a screen region. / *Hacé clic en Add Template para cargar una imagen existente, o en Create Template para capturar un área de la pantalla.*

2. **Configure basic settings / Configurar opciones básicas** — Adjust accuracy, scan interval, and mouse move time. / *Ajustá la precisión, el intervalo de escaneo y el tiempo de movimiento del mouse.*

3. **Per-template options / Opciones por template** *(optional/opcional)* — Select a template and open *Template Options* to set custom accuracy, cooldown, click limit, or auto-stop. / *Seleccioná un template y abrí Template Options para configurar precisión propia, cooldown, límite de clics o detención automática.*

4. **Extra options / Opciones extra** *(optional/opcional)* — Click *Show Extra Options* to pick the monitor, define a search area, set limits, or configure the hotkey. / *Hacé clic en Show Extra Options para elegir el monitor, definir un área de búsqueda, limitar tiempo/clics o configurar la hotkey.*

5. **Save preset / Guardar preset** *(optional/opcional)* — Save the current setup with *Save Current as Preset* for later reuse. / *Guardá la configuración actual con Save Current as Preset para reutilizarla después.*

6. **Start / Iniciar** — Click *Start*. The helper runs in the background. / *Hacé clic en Start. El helper corre en segundo plano.*

7. **Pause / Pausar** — Use the *Pause* button or the configured hotkey (default `F9`). / *Usá el botón Pause o la hotkey configurada (por defecto F9).*

8. **Stop / Detener** — Click *Stop*. A session summary is shown. / *Hacé clic en Stop. Aparece un resumen de la sesión.*

---

## Disclaimer / Aviso legal

This tool is provided for educational and personal use only. The use of automation software may violate the terms of service of certain games or platforms. The author takes no responsibility for any bans, penalties, or consequences resulting from the use of this program. **Use it at your own risk.**

*Esta herramienta se proporciona únicamente con fines educativos y de uso personal. El uso de software de automatización puede violar los términos de servicio de ciertos juegos o plataformas. El autor no se hace responsable por baneos, sanciones ni ninguna otra consecuencia derivada del uso de este programa. **Usalo bajo tu propia responsabilidad.***

---

## Dependencies / Dependencias

| Library / Librería | Purpose / Uso |
|---|---|
| `opencv-python` | Template matching / Detección de templates |
| `numpy` | Image array operations / Operaciones sobre arrays de imagen |
| `pyautogui` | Mouse control and capture (fallback) / Control del mouse y captura (fallback) |
| `mss` | Fast screen capture / Captura de pantalla rápida |
| `Pillow` | Image utilities / Utilidades de imagen |
| `tkinter` | GUI (bundled with Python) / Interfaz gráfica (incluida con Python) |

> If you use the executable, none of these need to be installed. / *Si usás el ejecutable, no necesitás instalar nada.*

---

## License / Licencia

[MIT](LICENSE)
