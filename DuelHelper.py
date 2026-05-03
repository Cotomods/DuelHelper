import threading
import time
import random
import os
import shutil
import sys
import subprocess
import base64
import json
from dataclasses import dataclass
from typing import List, Optional, Tuple, Dict

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

import cv2
import numpy as np
import pyautogui

try:
    from mss import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

ICON_B64: str = "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"

@dataclass
class TemplateItem:
    path: str
    image: Optional[np.ndarray]  # grayscale template; None if missing
    width: int
    height: int
    # Last matched region (frame coordinates, not including monitor offset)
    last_region: Optional[Tuple[int, int, int, int]] = None
    # Time of last click on this template (seconds since epoch)
    last_click_time: float = 0.0
    # Is this template enabled for clicking?
    enabled: bool = True
    # Per-template override settings
    custom_threshold: Optional[float] = None
    click_cooldown: Optional[float] = None  # seconds between clicks for this template
    max_clicks_per_run: Optional[int] = None
    # Stop the entire run after this template has been clicked N times (None = off)
    stop_after_clicks: Optional[int] = None
    # Runtime-only counter, reset on each Start
    clicks_this_run: int = 0


STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        # Window / menu
        "title": "Duel Helper",
        "menu_options": "Options",
        "menu_language": "Language",
        # Frames
        "frame_templates": "Templates",
        "frame_main_settings": "Main Settings",
        "frame_presets": "Template Presets",
        "frame_template_options": "Template Options",
        "frame_extra_options": "Extra Options",
        "frame_log": "Log",
        # Template buttons
        "btn_add_template": "Add Template",
        "btn_create_template": "Create Template",
        "btn_open_folder": "Open Templates Folder",
        "btn_remove_template": "Remove Selected Template",
        "btn_template_options": "Template Options",
        # Preset buttons
        "btn_save_preset": "Save Current as Preset",
        "btn_load_preset": "Load Preset",
        "btn_delete_preset": "Delete Preset",
        # Template options panel
        "lbl_no_template": "No template selected",
        "chk_use_template": "Use this template",
        "lbl_own_threshold": "Own match accuracy (0-1, blank = use main):",
        "lbl_cooldown": "Wait between clicks (sec, blank = 3):",
        "lbl_max_clicks": "Max clicks for this template (blank = no limit):",
        "lbl_stop_after": "Stop helper after this many clicks (blank = off):",
        "btn_save_tpl_settings": "Save Template Settings",
        "lbl_no_preview": "No preview",
        "lbl_missing_image": "Missing image",
        # Main settings
        "lbl_threshold": "Match accuracy (0-1):",
        "lbl_scan_interval": "Time between scans (min/max sec):",
        "lbl_move_time": "Mouse move time (min/max sec):",
        "chk_confirm_start": "Ask for confirmation before starting",
        "btn_show_extra": "Show Extra Options",
        "btn_hide_extra": "Hide Extra Options",
        # Extra options
        "lbl_monitor": "Screen to watch (1 = main):",
        "btn_set_region": "Set search area",
        "btn_clear_region": "Clear search area",
        "lbl_auto_stop": "Stop run after (min, 0 = keep running):",
        "lbl_max_clicks_run": "Max clicks this run (0 = no limit):",
        "lbl_idle": "Take a short break every (min, 0 = no breaks):",

        # Control buttons
        "btn_start": "Start",
        "btn_stop": "Stop",
        "btn_pause": "Pause",
        "btn_resume": "Resume",
        # Status
        "status_idle": "Idle",
        "status_running": "Running",
        "status_paused": "Paused",
        "status_stopping": "Stopping",
        "status_prefix": "Status",
        "status_preset": "Preset",
        "status_templates": "Templates",
        "status_clicks": "Clicks",
        "log_stopping": "Stopping bot...",
        "log_stopped": "Bot stopped.",
        "log_started": "Bot started.",
        "log_paused": "Bot paused.",
        "log_resumed": "Bot resumed.",
        "log_worker_stopped_wait": "Waiting for worker thread to stop...",
        # Dialogs - warnings / errors
        "dlg_missing_tpl_title": "Missing templates",
        "dlg_missing_tpl_msg": "{count} template(s) are marked as missing and will be skipped. Continue?",
        "dlg_no_templates_title": "No templates",
        "dlg_no_templates_msg": "Please add at least one template before starting.",
        "dlg_invalid_settings_title": "Invalid settings",
        "dlg_invalid_settings_msg": "Please ensure all numeric fields are valid.",
        "dlg_threshold_title": "Number not valid",
        "dlg_threshold_msg": "Match accuracy must be between 0.1 and 0.99.",
        "dlg_scan_title": "Numbers not valid",
        "dlg_scan_msg": "Time between scans must be at least 0.05 seconds, and the first value cannot be larger than the second.",
        "dlg_move_title": "Numbers not valid",
        "dlg_move_msg": "Mouse move time must be at least 0.01 seconds, and the first value cannot be larger than the second.",
        "dlg_mss_title": "mss not installed",
        "dlg_mss_msg": "The 'mss' library is not installed. The helper will fall back to 'pyautogui' for screen capture, which may feel slower.\n\nTo fix this, run: pip install mss\n\nContinue anyway?",
        "dlg_confirm_start_title": "Start bot?",
        "dlg_confirm_start_msg": "Start bot with {enabled}/{total} templates enabled?",
        "dlg_no_tpl_selected_title": "No template selected",
        "dlg_no_tpl_selected_msg": "Please select a template to apply settings.",
        "dlg_tpl_toggle_title": "No template selected",
        "dlg_tpl_toggle_msg": "Please select a template to toggle.",
        "dlg_tpl_threshold_title": "Number not valid",
        "dlg_tpl_threshold_msg": "Match accuracy must be a number between 0 and 1.",
        "dlg_tpl_cooldown_title": "Number not valid",
        "dlg_tpl_cooldown_msg": "Wait time must be a number of seconds, 0 or more.",
        "dlg_tpl_maxclicks_title": "Number not valid",
        "dlg_tpl_maxclicks_msg": "Max clicks must be a whole number, 0 or more.",
        "dlg_tpl_stopafter_title": "Number not valid",
        "dlg_tpl_stopafter_msg": "The stop-after-clicks value must be a whole number, 0 or more.",
        "dlg_set_region_title": "Set Search Area",
        "dlg_set_region_msg": "After you click OK, the screen will dim.\nClick and drag to choose the part of the screen where the helper should look.\nPress Esc to cancel.",
        "dlg_create_tpl_title": "Create Template",
        "dlg_create_tpl_msg": "After you click OK, the screen will dim.\nClick and drag to select the area you want to save as a template.\nPress Esc to cancel.",
        "dlg_tpl_name_title": "Template Name",
        "dlg_tpl_name_msg": "Enter a name for the new template (just the name, no .png):",
        "dlg_tpl_overwrite_title": "Overwrite?",
        "dlg_tpl_overwrite_msg": "A template named '{filename}' already exists. Overwrite it?",
        "dlg_copy_error_title": "Error",
        "dlg_copy_error_msg": "Failed to copy template: {e}",
        "dlg_create_error_title": "Error",
        "dlg_create_error_msg": "Failed to create template: {e}",
        "dlg_folder_error_title": "Error",
        "dlg_folder_error_msg": "Failed to open Templates folder: {e}",
        "dlg_save_preset_title": "Save Preset",
        "dlg_save_preset_msg": "Enter a name for this preset:",
        "dlg_no_preset_templates_title": "No templates",
        "dlg_no_preset_templates_msg": "There are no templates loaded to save as a preset.",
        "dlg_preset_name_empty_title": "Invalid name",
        "dlg_preset_name_empty_msg": "Preset name cannot be empty.",
        "dlg_empty_preset_title": "Empty preset",
        "dlg_empty_preset_msg": "Preset '{name}' has no templates.",
        "dlg_no_preset_title": "No preset selected",
        "dlg_no_preset_msg": "Please select a preset to load.",
        "dlg_preset_not_found_title": "Preset not found",
        "dlg_preset_not_found_msg": "Preset '{name}' does not exist.",
        "dlg_delete_preset_title": "Delete Preset",
        "dlg_delete_preset_msg": "Are you sure you want to delete preset '{name}'?",
        "dlg_no_preset_delete_title": "No preset selected",
        "dlg_no_preset_delete_msg": "Please select a preset to delete.",
        # Log controls (point 1)
        "btn_clear_log": "Clear Log",
        # Session summary (point 2)
        "dlg_session_title": "Session Summary",
        "dlg_session_msg": "The bot stopped.\n\nTotal clicks: {total}\nRuntime: {runtime}\n\nClicks per template:\n{per_template}",
        # Monitor labels (point 5)
        "monitor_label": "Monitor {idx} — {w}×{h} at ({x},{y})",
        "monitor_primary": "Monitor {idx} (Primary) — {w}×{h}",
        # Hotkey (point 6)
        "lbl_hotkey": "Pause/Resume hotkey:",
        "btn_set_hotkey": "Change",
        "dlg_hotkey_title": "Set Hotkey",
        "dlg_hotkey_msg": "Press any key to use as the pause/resume hotkey.\nPress Escape to cancel.",
        "log_hotkey_set": "Hotkey set to: {key}",
        "log_hotkey_disabled": "Hotkey disabled.",
        # Template creation log messages
        "log_tpl_create_too_small": "Template creation cancelled: selected area too small.",
        "log_tpl_create_no_name": "Template creation cancelled: no name provided.",
        "log_tpl_create_empty_name": "Template creation cancelled: empty name.",
        "log_tpl_create_no_overwrite": "Template creation cancelled: file already exists and overwrite not confirmed.",
        "log_tpl_create_cancelled": "Template creation cancelled by user.",
        # Search region log messages
        "log_region_too_small": "Search region selection cancelled: area too small.",
        "log_region_cancelled": "Search region selection cancelled by user.",
        "log_region_set": "Search region set to left={left}, top={top}, w={w}, h={h}.",
        "log_region_none_to_clear": "No search region to clear.",
        "log_region_cleared": "Search region cleared (using full monitor).",
        "log_tpl_load_failed": "Failed to load image (marked missing): {path}",
        "log_tpl_added": "Added template: {path} ({w}x{h})",
        "log_tpl_copied": "Copied template to Templates folder: {path}",
        "log_tpl_saved": "Saved new template: {path}",
        "log_tpl_removed": "Removed template: {path}",
        "log_tpl_settings_updated": "Updated settings for template: {path}",
        "log_tpl_enabled": "Template {name} enabled.",
        "log_tpl_disabled": "Template {name} disabled.",
        "log_preset_load_failed": "Failed to load presets: {e}",
        "log_preset_save_failed": "Failed to save presets: {e}",
        "log_preset_saved": "Saved preset \'{name}\' with {count} templates.",
        "log_preset_missing_tpl": "Missing template for preset \'{name}\': {filename}",
        "log_preset_loaded": "Loaded preset \'{name}\' with {loaded} templates (missing: {missing}).",
        "log_preset_deleted": "Deleted preset \'{name}\'.",
        "log_worker_started": "Worker started with threshold={threshold}, scan={scan_min}-{scan_max}s, move={move_min}-{move_max}s.",
        "log_autostop_runtime": "Auto-stop: reached maximum runtime.",
        "log_autostop_clicks": "Auto-stop: reached global click limit.",
        "log_idle_pause": "Idle pause for {secs}s to appear more human.",
        "log_tpl_matched": "Template matched at ({x}, {y}, {w}x{h}), score={score}. Moving to ({tx}, {ty}) and clicking.",
        "log_stop_after_reached": "Stopping bot: template {name} reached stop-after-clicks limit ({limit}).",
        "log_crash": "[CRASH] Worker stopped due to an unexpected error: {e}",
        "log_crash_tb": "[CRASH] Traceback:\n{tb}",
        "dlg_select_template_title": "Select template image",
        "status_stop_label": "Stop",
        # Template listbox display tags
        "tpl_tag_missing": "[MISSING]",
        "tpl_tag_off": "[OFF]",
        # Move template log
        "log_tpl_moved": "Moved \'{name}\' from position {src} to {dst}.",
        # File dialog filters
        "filetype_images": "Image files",
        "filetype_all": "All files",
    },
    "es": {
        # Window / menu
        "title": "Duel Helper",
        "menu_options": "Opciones",
        "menu_language": "Idioma",
        # Frames
        "frame_templates": "Plantillas",
        "frame_main_settings": "Configuración Principal",
        "frame_presets": "Presets de Plantillas",
        "frame_template_options": "Opciones de Plantilla",
        "frame_extra_options": "Opciones Extra",
        "frame_log": "Registro",
        # Template buttons
        "btn_add_template": "Agregar Plantilla",
        "btn_create_template": "Crear Plantilla",
        "btn_open_folder": "Abrir Carpeta de Plantillas",
        "btn_remove_template": "Eliminar Plantilla Seleccionada",
        "btn_template_options": "Opciones de Plantilla",
        # Preset buttons
        "btn_save_preset": "Guardar como Preset",
        "btn_load_preset": "Cargar Preset",
        "btn_delete_preset": "Eliminar Preset",
        # Template options panel
        "lbl_no_template": "Ninguna plantilla seleccionada",
        "chk_use_template": "Usar esta plantilla",
        "lbl_own_threshold": "Precisión propia (0-1, vacío = usar la principal):",
        "lbl_cooldown": "Espera entre clics (seg, vacío = 3):",
        "lbl_max_clicks": "Máx. clics para esta plantilla (vacío = sin límite):",
        "lbl_stop_after": "Detener el helper después de N clics (vacío = no):",
        "btn_save_tpl_settings": "Guardar Configuración de Plantilla",
        "lbl_no_preview": "Sin vista previa",
        "lbl_missing_image": "Imagen no encontrada",
        # Main settings
        "lbl_threshold": "Precisión de detección (0-1):",
        "lbl_scan_interval": "Tiempo entre escaneos (mín/máx seg):",
        "lbl_move_time": "Tiempo de movimiento del mouse (mín/máx seg):",
        "chk_confirm_start": "Pedir confirmación antes de iniciar",
        "btn_show_extra": "Mostrar Opciones Extra",
        "btn_hide_extra": "Ocultar Opciones Extra",
        # Extra options
        "lbl_monitor": "Pantalla a monitorear (1 = principal):",
        "btn_set_region": "Definir área de búsqueda",
        "btn_clear_region": "Limpiar área de búsqueda",
        "lbl_auto_stop": "Detener después de (min, 0 = nunca):",
        "lbl_max_clicks_run": "Máx. clics en esta sesión (0 = sin límite):",
        "lbl_idle": "Tomar un descanso cada (min, 0 = nunca):",

        # Control buttons
        "btn_start": "Iniciar",
        "btn_stop": "Detener",
        "btn_pause": "Pausar",
        "btn_resume": "Reanudar",
        # Status
        "status_idle": "Inactivo",
        "status_running": "Ejecutando",
        "status_paused": "Pausado",
        "status_stopping": "Deteniendo",
        "status_prefix": "Estado",
        "status_preset": "Preset",
        "status_templates": "Plantillas",
        "status_clicks": "Clics",
        "log_stopping": "Deteniendo bot...",
        "log_stopped": "Bot detenido.",
        "log_started": "Bot iniciado.",
        "log_paused": "Bot pausado.",
        "log_resumed": "Bot reanudado.",
        "log_worker_stopped_wait": "Esperando que el hilo de trabajo se detenga...",
        # Dialogs
        "dlg_missing_tpl_title": "Plantillas faltantes",
        "dlg_missing_tpl_msg": "{count} plantilla(s) están marcadas como faltantes y serán ignoradas. ¿Continuar?",
        "dlg_no_templates_title": "Sin plantillas",
        "dlg_no_templates_msg": "Por favor agregá al menos una plantilla antes de iniciar.",
        "dlg_invalid_settings_title": "Configuración inválida",
        "dlg_invalid_settings_msg": "Asegurate de que todos los campos numéricos sean válidos.",
        "dlg_threshold_title": "Número inválido",
        "dlg_threshold_msg": "La precisión de detección debe ser entre 0.1 y 0.99.",
        "dlg_scan_title": "Números inválidos",
        "dlg_scan_msg": "El tiempo entre escaneos debe ser al menos 0.05 segundos, y el primero no puede ser mayor que el segundo.",
        "dlg_move_title": "Números inválidos",
        "dlg_move_msg": "El tiempo de movimiento del mouse debe ser al menos 0.01 segundos, y el primero no puede ser mayor que el segundo.",
        "dlg_mss_title": "mss no instalado",
        "dlg_mss_msg": "La librería 'mss' no está instalada. El helper usará 'pyautogui' para capturar pantalla, lo cual puede ser más lento.\n\nPara solucionarlo, ejecutá: pip install mss\n\n¿Continuar de todas formas?",
        "dlg_confirm_start_title": "¿Iniciar bot?",
        "dlg_confirm_start_msg": "¿Iniciar bot con {enabled}/{total} plantillas activas?",
        "dlg_no_tpl_selected_title": "Ninguna plantilla seleccionada",
        "dlg_no_tpl_selected_msg": "Por favor seleccioná una plantilla para aplicar la configuración.",
        "dlg_tpl_toggle_title": "Ninguna plantilla seleccionada",
        "dlg_tpl_toggle_msg": "Por favor seleccioná una plantilla para activar/desactivar.",
        "dlg_tpl_threshold_title": "Número inválido",
        "dlg_tpl_threshold_msg": "La precisión debe ser un número entre 0 y 1.",
        "dlg_tpl_cooldown_title": "Número inválido",
        "dlg_tpl_cooldown_msg": "El tiempo de espera debe ser un número de segundos, 0 o más.",
        "dlg_tpl_maxclicks_title": "Número inválido",
        "dlg_tpl_maxclicks_msg": "Los clics máximos deben ser un número entero, 0 o más.",
        "dlg_tpl_stopafter_title": "Número inválido",
        "dlg_tpl_stopafter_msg": "El valor de detener-tras-clics debe ser un número entero, 0 o más.",
        "dlg_set_region_title": "Definir Área de Búsqueda",
        "dlg_set_region_msg": "Al hacer clic en OK, la pantalla se oscurecerá.\nHacé clic y arrastrá para elegir el área donde el helper debe buscar.\nPresioná Esc para cancelar.",
        "dlg_create_tpl_title": "Crear Plantilla",
        "dlg_create_tpl_msg": "Al hacer clic en OK, la pantalla se oscurecerá.\nHacé clic y arrastrá para seleccionar el área que querés guardar como plantilla.\nPresioná Esc para cancelar.",
        "dlg_tpl_name_title": "Nombre de Plantilla",
        "dlg_tpl_name_msg": "Ingresá un nombre para la nueva plantilla (solo el nombre, sin .png):",
        "dlg_tpl_overwrite_title": "¿Sobreescribir?",
        "dlg_tpl_overwrite_msg": "Ya existe una plantilla llamada '{filename}'. ¿Sobreescribirla?",
        "dlg_copy_error_title": "Error",
        "dlg_copy_error_msg": "No se pudo copiar la plantilla: {e}",
        "dlg_create_error_title": "Error",
        "dlg_create_error_msg": "No se pudo crear la plantilla: {e}",
        "dlg_folder_error_title": "Error",
        "dlg_folder_error_msg": "No se pudo abrir la carpeta de plantillas: {e}",
        "dlg_save_preset_title": "Guardar Preset",
        "dlg_save_preset_msg": "Ingresá un nombre para este preset:",
        "dlg_no_preset_templates_title": "Sin plantillas",
        "dlg_no_preset_templates_msg": "No hay plantillas cargadas para guardar como preset.",
        "dlg_preset_name_empty_title": "Nombre inválido",
        "dlg_preset_name_empty_msg": "El nombre del preset no puede estar vacío.",
        "dlg_empty_preset_title": "Preset vacío",
        "dlg_empty_preset_msg": "El preset '{name}' no tiene plantillas.",
        "dlg_no_preset_title": "Ningún preset seleccionado",
        "dlg_no_preset_msg": "Por favor seleccioná un preset para cargar.",
        "dlg_preset_not_found_title": "Preset no encontrado",
        "dlg_preset_not_found_msg": "El preset '{name}' no existe.",
        "dlg_delete_preset_title": "Eliminar Preset",
        "dlg_delete_preset_msg": "¿Estás seguro de que querés eliminar el preset '{name}'?",
        "dlg_no_preset_delete_title": "Ningún preset seleccionado",
        "dlg_no_preset_delete_msg": "Por favor seleccioná un preset para eliminar.",
        # Log controls (point 1)
        "btn_clear_log": "Limpiar Registro",
        # Session summary (point 2)
        "dlg_session_title": "Resumen de Sesión",
        "dlg_session_msg": "El bot se detuvo.\n\nClics totales: {total}\nTiempo: {runtime}\n\nClics por plantilla:\n{per_template}",
        # Monitor labels (point 5)
        "monitor_label": "Monitor {idx} — {w}×{h} en ({x},{y})",
        "monitor_primary": "Monitor {idx} (Principal) — {w}×{h}",
        # Hotkey (point 6)
        "lbl_hotkey": "Tecla de pausa/reanudar:",
        "btn_set_hotkey": "Cambiar",
        "dlg_hotkey_title": "Configurar Tecla",
        "dlg_hotkey_msg": "Presioná cualquier tecla para usarla como atajo de pausa/reanudar.\nPresioná Escape para cancelar.",
        "log_hotkey_set": "Tecla configurada: {key}",
        "log_hotkey_disabled": "Tecla de atajo desactivada.",
        # Template creation log messages
        "log_tpl_create_too_small": "Creación de plantilla cancelada: área seleccionada muy pequeña.",
        "log_tpl_create_no_name": "Creación de plantilla cancelada: no se proporcionó nombre.",
        "log_tpl_create_empty_name": "Creación de plantilla cancelada: nombre vacío.",
        "log_tpl_create_no_overwrite": "Creación de plantilla cancelada: el archivo ya existe y no se confirmó la sobreescritura.",
        "log_tpl_create_cancelled": "Creación de plantilla cancelada por el usuario.",
        # Search region log messages
        "log_region_too_small": "Selección de área cancelada: área muy pequeña.",
        "log_region_cancelled": "Selección de área cancelada por el usuario.",
        "log_region_set": "Área de búsqueda: izq={left}, arr={top}, ancho={w}, alto={h}.",
        "log_region_none_to_clear": "No hay área de búsqueda para limpiar.",
        "log_region_cleared": "Área de búsqueda eliminada (usando monitor completo).",
        "log_tpl_load_failed": "No se pudo cargar la imagen (marcada como faltante): {path}",
        "log_tpl_added": "Plantilla agregada: {path} ({w}x{h})",
        "log_tpl_copied": "Plantilla copiada a la carpeta Templates: {path}",
        "log_tpl_saved": "Nueva plantilla guardada: {path}",
        "log_tpl_removed": "Plantilla eliminada: {path}",
        "log_tpl_settings_updated": "Configuración actualizada para la plantilla: {path}",
        "log_tpl_enabled": "Plantilla {name} activada.",
        "log_tpl_disabled": "Plantilla {name} desactivada.",
        "log_preset_load_failed": "Error al cargar presets: {e}",
        "log_preset_save_failed": "Error al guardar presets: {e}",
        "log_preset_saved": "Preset \'{name}\' guardado con {count} plantillas.",
        "log_preset_missing_tpl": "Plantilla faltante para el preset \'{name}\': {filename}",
        "log_preset_loaded": "Preset \'{name}\' cargado con {loaded} plantillas (faltantes: {missing}).",
        "log_preset_deleted": "Preset \'{name}\' eliminado.",
        "log_worker_started": "Trabajador iniciado con precisión={threshold}, escaneo={scan_min}-{scan_max}s, movimiento={move_min}-{move_max}s.",
        "log_autostop_runtime": "Detención automática: se alcanzó el tiempo máximo.",
        "log_autostop_clicks": "Detención automática: se alcanzó el límite global de clics.",
        "log_idle_pause": "Pausa de {secs}s para simular comportamiento humano.",
        "log_tpl_matched": "Plantilla detectada en ({x}, {y}, {w}x{h}), puntuación={score}. Moviendo a ({tx}, {ty}) y haciendo clic.",
        "log_stop_after_reached": "Deteniendo bot: la plantilla {name} alcanzó el límite de clics ({limit}).",
        "log_crash": "[CRASH] El trabajador se detuvo por un error inesperado: {e}",
        "log_crash_tb": "[CRASH] Rastreo:\n{tb}",
        "dlg_select_template_title": "Seleccionar imagen de plantilla",
        "status_stop_label": "Stop",
        # Template listbox display tags
        "tpl_tag_missing": "[FALTANTE]",
        "tpl_tag_off": "[OFF]",
        # Move template log
        "log_tpl_moved": "Plantilla \'{name}\' movida de la posición {src} a {dst}.",
        # File dialog filters
        "filetype_images": "Archivos de imagen",
        "filetype_all": "Todos los archivos",
    },
}


class TemplateClickerApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Duel Helper")
        # Keep window always on top (except when minimized by the OS)
        try:
            self.attributes("-topmost", True)
        except Exception:
            pass
        # Enforce a reasonable minimum window size
        try:
            self.minsize(700, 500)
        except Exception:
            pass

        # Templates directory (next to this script / .exe)
        if getattr(sys, "frozen", False):
            # Running as a PyInstaller-packaged executable
            base_dir = os.path.dirname(sys.executable)
        else:
            # Running as a normal .py script
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_dir = os.path.join(base_dir, "Templates")
        os.makedirs(self.templates_dir, exist_ok=True)

        # Log file path for basic diagnostics
        self.log_file_path = os.path.join(base_dir, "duel_helper.log")

        # Window icon — embedded as base64 PNG, no external files needed
        self._tk_icon: Optional[tk.PhotoImage] = None
        if ICON_B64:
            try:
                import base64 as _b64
                self._tk_icon = tk.PhotoImage(data=_b64.b64decode(ICON_B64))
                # iconphoto(True, ...) applies the icon to this window AND all
                # future Toplevel windows automatically
                self.iconphoto(True, self._tk_icon)
            except Exception:
                self._tk_icon = None

        # Presets storage (JSON file next to this script)
        self.presets_path = os.path.join(base_dir, "template_presets.json")
        self.presets: Dict[str, List[str]] = {}

        # App-wide config (JSON next to this script)
        self.config_path = os.path.join(base_dir, "duel_helper_config.json")
        self.config: Dict[str, object] = self._load_config()

        # Language — load from config, default to English
        saved_lang = str(self.config.get("language", "en")) if isinstance(self.config, dict) else "en"
        self.language: str = saved_lang if saved_lang in STRINGS else "en"

        # State
        self.templates: List[TemplateItem] = []
        self.worker_thread: Optional[threading.Thread] = None
        self.running_event = threading.Event()

        # Locks protecting shared state written by the worker thread
        self._clicks_lock = threading.Lock()
        self._paused_lock = threading.Lock()
        self._paused_flag: bool = False  # canonical pause state; use property below

        # Runtime metrics
        self.total_clicks_this_run: int = 0
        self.run_start_time: float = 0.0
        self.last_idle_time: float = 0.0


        # Config variables (will be snapshotted when starting)
        conf = self.config

        # Restore window size from config if available
        try:
            win_w = int(conf.get("window_width", 700))
            win_h = int(conf.get("window_height", 500))
            if win_w > 200 and win_h > 200:
                self.geometry(f"{win_w}x{win_h}")
            else:
                self.geometry("700x500")
        except Exception:
            self.geometry("700x500")

        self.match_threshold_var = tk.DoubleVar(value=float(conf.get("threshold", 0.85)))
        self.scan_interval_min_var = tk.DoubleVar(value=float(conf.get("scan_min", 0.3)))
        self.scan_interval_max_var = tk.DoubleVar(value=float(conf.get("scan_max", 0.7)))
        self.move_duration_min_var = tk.DoubleVar(value=float(conf.get("move_min", 0.25)))
        self.move_duration_max_var = tk.DoubleVar(value=float(conf.get("move_max", 0.7)))

        # Additional config/state variables
        # Detect the primary monitor index for use as default on first run
        def _get_primary_monitor_index() -> int:
            try:
                from mss import mss as _mss
                with _mss() as sct:
                    # mss index 0 = all monitors combined; 1..N = individual monitors
                    # Find which one matches the top-left corner (0, 0) = primary monitor
                    for idx, mon in enumerate(sct.monitors[1:], start=1):
                        if mon["left"] == 0 and mon["top"] == 0:
                            return idx
                    return 1  # fallback
            except Exception:
                return 1
        _default_monitor = _get_primary_monitor_index() if "monitor_index" not in conf else int(conf["monitor_index"])
        self.monitor_index_var = tk.IntVar(value=_default_monitor)
        self.auto_stop_minutes_var = tk.DoubleVar(value=float(conf.get("auto_stop_minutes", 0.0)))
        self.global_max_clicks_var = tk.IntVar(value=int(conf.get("global_max_clicks", 0)))
        self.random_idle_minutes_var = tk.DoubleVar(value=float(conf.get("idle_minutes", 0.0)))
        self.confirm_on_start_var = tk.BooleanVar(value=bool(conf.get("confirm_on_start", False)))

        # Search region: (left, top, width, height) or None
        sr = conf.get("search_region")
        if isinstance(sr, (list, tuple)) and len(sr) == 4:
            self.search_region: Optional[Tuple[int, int, int, int]] = (
                int(sr[0]), int(sr[1]), int(sr[2]), int(sr[3])
            )
        else:
            self.search_region = None

        # Status text — initialised to a placeholder; _update_status sets the real value after UI is built
        self.status_var = tk.StringVar(value="")
        # Advanced settings visibility flag
        self.advanced_visible = False

        # Global hotkey for pause/resume (string like "F9", or None if disabled)
        saved_hotkey = str(self.config.get("hotkey", "F9")) if isinstance(self.config, dict) else "F9"
        self.hotkey: str = saved_hotkey

        self._build_ui()
        self._update_status(self._t("status_idle"))
        self._load_presets()

        # Safety: moving mouse to top-left corner aborts pyautogui actions
        pyautogui.FAILSAFE = True

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start global hotkey listener
        self._start_hotkey_listener()

    # ---------------- Thread-safe paused property -----------------
    @property
    def paused(self) -> bool:
        with self._paused_lock:
            return self._paused_flag

    @paused.setter
    def paused(self, value: bool) -> None:
        with self._paused_lock:
            self._paused_flag = value

    # ---------------- i18n -----------------
    def _t(self, key: str, **kwargs) -> str:
        """Return the translated string for key in the current language."""
        lang_dict = STRINGS.get(self.language, STRINGS["en"])
        text = lang_dict.get(key, STRINGS["en"].get(key, key))
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text

    def on_change_language(self, lang: str) -> None:
        """Switch language and rebuild the entire UI."""
        if lang not in STRINGS or lang == self.language:
            return
        self.language = lang
        if isinstance(self.config, dict):
            self.config["language"] = lang
        try:
            self._save_config()
        except Exception:
            pass
        # Save current log contents before destroying widgets
        try:
            saved_log = self.log_text.get("1.0", tk.END)
        except Exception:
            saved_log = ""
        # Destroy all current widgets and rebuild
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
        # Restore log contents
        if saved_log.strip():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, saved_log)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        self._refresh_presets_combo()
        self._refresh_templates_listbox()
        self._update_status(self._t("status_idle"))
        self._start_hotkey_listener()

    # ---------------- UI -----------------
    def _build_ui(self) -> None:
        # Scrollable main area so the app can fit on smaller screens
        menubar = tk.Menu(self)
        options_menu = tk.Menu(menubar, tearoff=0)
        lang_submenu = tk.Menu(options_menu, tearoff=0)
        lang_submenu.add_command(label="English", command=lambda: self.on_change_language("en"))
        lang_submenu.add_command(label="Español", command=lambda: self.on_change_language("es"))
        options_menu.add_cascade(label=self._t("menu_language"), menu=lang_submenu)
        menubar.add_cascade(label=self._t("menu_options"), menu=options_menu)

        # Use dictionary-style assignment to avoid clashing with self.config dict
        self["menu"] = menubar

        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=v_scrollbar.set)

        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        main_frame = ttk.Frame(canvas, padding=10)
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor="nw")

        def _on_frame_configure(event: tk.Event) -> None:  # type: ignore[unused-argument]
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_resize(event: tk.Event) -> None:
            """Stretch main_frame to fill the canvas width when the window grows."""
            canvas.itemconfig(canvas_window, width=event.width)

        main_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_resize)

        # Mouse wheel scrolling (Windows / most platforms)
        def _on_mousewheel(event: tk.Event) -> None:  # type: ignore[unused-argument]
            # If content height is less than or equal to the visible height,
            # do not scroll (prevents "empty" scrolling when window is large).
            bbox = canvas.bbox("all")
            if not bbox:
                return
            content_height = bbox[3] - bbox[1]
            visible_height = canvas.winfo_height()
            if content_height <= visible_height:
                return

            # event.delta is typically a multiple of 120 on Windows
            delta = int(-1 * (event.delta / 120)) if event.delta != 0 else 0
            if delta != 0:
                canvas.yview_scroll(delta, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Templates frame
        templates_frame = ttk.LabelFrame(main_frame, text=self._t("frame_templates"))
        templates_frame.pack(fill=tk.BOTH, expand=False, side=tk.TOP, padx=5, pady=5)

        self.templates_listbox = tk.Listbox(templates_frame, height=5, selectmode=tk.SINGLE)
        self.templates_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        self.templates_listbox.bind("<<ListboxSelect>>", self.on_template_selected)
        self.templates_listbox.bind("<Double-Button-1>", lambda e: self.on_toggle_template_enabled())

        # --- Drag-and-drop reordering ---
        # State for the in-progress drag
        self._drag_state: dict = {"index": None, "indicator": None}

        def _dnd_start(event: tk.Event) -> None:
            idx = self.templates_listbox.nearest(event.y)
            if idx < 0 or idx >= len(self.templates):
                return
            self._drag_state["index"] = idx
            self.templates_listbox.selection_clear(0, tk.END)
            self.templates_listbox.selection_set(idx)
            self.templates_listbox.config(cursor="fleur")

        def _dnd_motion(event: tk.Event) -> None:
            if self._drag_state["index"] is None:
                return
            target = self.templates_listbox.nearest(event.y)
            if target < 0:
                return
            # Highlight target row with a visual indicator (change bg temporarily)
            self.templates_listbox.selection_clear(0, tk.END)
            self.templates_listbox.selection_set(target)
            self._drag_state["indicator"] = target

        def _dnd_release(event: tk.Event) -> None:
            src = self._drag_state["index"]
            self._drag_state["index"] = None
            self._drag_state["indicator"] = None
            self.templates_listbox.config(cursor="")
            if src is None:
                return
            dst = self.templates_listbox.nearest(event.y)
            if dst < 0 or dst == src or dst >= len(self.templates):
                # Restore original selection
                self.templates_listbox.selection_clear(0, tk.END)
                self.templates_listbox.selection_set(src)
                return
            self._move_template(src, dst)

        self.templates_listbox.bind("<ButtonPress-1>", _dnd_start)
        self.templates_listbox.bind("<B1-Motion>", _dnd_motion)
        self.templates_listbox.bind("<ButtonRelease-1>", _dnd_release)

        scrollbar = ttk.Scrollbar(templates_frame, orient=tk.VERTICAL, command=self.templates_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=5)
        self.templates_listbox.configure(yscrollcommand=scrollbar.set)

        btns_frame = ttk.Frame(templates_frame)
        btns_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        add_btn = ttk.Button(btns_frame, text=self._t("btn_add_template"), command=self.on_add_template)
        add_btn.pack(fill=tk.X, pady=(0, 5))

        create_btn = ttk.Button(btns_frame, text=self._t("btn_create_template"), command=self.on_create_template)
        create_btn.pack(fill=tk.X, pady=(0, 5))

        open_btn = ttk.Button(btns_frame, text=self._t("btn_open_folder"), command=self.on_open_templates_folder)
        open_btn.pack(fill=tk.X, pady=(0, 5))

        remove_btn = ttk.Button(btns_frame, text=self._t("btn_remove_template"), command=self.on_remove_selected_template)
        remove_btn.pack(fill=tk.X, pady=(0, 5))

        settings_btn = ttk.Button(btns_frame, text=self._t("btn_template_options"), command=self.on_toggle_template_settings_panel)
        settings_btn.pack(fill=tk.X)

        # Basic settings frame
        config_frame = ttk.LabelFrame(main_frame, text=self._t("frame_main_settings"))
        config_frame.pack(fill=tk.X, expand=False, side=tk.TOP, padx=5, pady=5)

        # Presets frame
        presets_frame = ttk.LabelFrame(main_frame, text=self._t("frame_presets"))
        presets_frame.pack(fill=tk.X, expand=False, side=tk.TOP, padx=5, pady=5)

        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(
            presets_frame,
            textvariable=self.preset_var,
            state="readonly",
        )
        self.preset_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5), pady=5)

        save_preset_btn = ttk.Button(
            presets_frame,
            text=self._t("btn_save_preset"),
            command=self.on_save_preset,
        )
        save_preset_btn.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        load_preset_btn = ttk.Button(
            presets_frame,
            text=self._t("btn_load_preset"),
            command=self.on_load_preset,
        )
        load_preset_btn.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        delete_preset_btn = ttk.Button(
            presets_frame,
            text=self._t("btn_delete_preset"),
            command=self.on_delete_preset,
        )
        delete_preset_btn.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        # Template settings panel (initially hidden)
        self.template_settings_frame = ttk.LabelFrame(main_frame, text=self._t("frame_template_options"))
        self.template_settings_frame.columnconfigure(0, weight=1)
        self.template_settings_frame.columnconfigure(1, weight=0)
        self.template_settings_frame.columnconfigure(2, weight=1)

        self.template_name_var = tk.StringVar(value=self._t("lbl_no_template"))
        name_label = ttk.Label(self.template_settings_frame, textvariable=self.template_name_var)
        name_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=5, pady=(5, 2))

        self.template_enabled_var = tk.BooleanVar(value=True)
        enabled_check = ttk.Checkbutton(
            self.template_settings_frame,
            text=self._t("chk_use_template"),
            variable=self.template_enabled_var,
        )
        enabled_check.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        ttk.Label(
            self.template_settings_frame,
            text=self._t("lbl_own_threshold"),
        ).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.template_threshold_entry = ttk.Entry(self.template_settings_frame, width=8)
        self.template_threshold_entry.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(
            self.template_settings_frame,
            text=self._t("lbl_cooldown"),
        ).grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.template_cooldown_entry = ttk.Entry(self.template_settings_frame, width=8)
        self.template_cooldown_entry.grid(row=3, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(
            self.template_settings_frame,
            text=self._t("lbl_max_clicks"),
        ).grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.template_max_clicks_entry = ttk.Entry(self.template_settings_frame, width=8)
        self.template_max_clicks_entry.grid(row=4, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(
            self.template_settings_frame,
            text=self._t("lbl_stop_after"),
        ).grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.template_stop_after_entry = ttk.Entry(self.template_settings_frame, width=8)
        self.template_stop_after_entry.grid(row=5, column=1, sticky="w", padx=5, pady=2)

        apply_btn = ttk.Button(
            self.template_settings_frame,
            text=self._t("btn_save_tpl_settings"),
            command=self.on_apply_template_settings,
        )
        apply_btn.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=(5, 5))

        self.template_preview_label = ttk.Label(self.template_settings_frame, text=self._t("lbl_no_preview"))
        self.template_preview_label.grid(row=1, column=2, rowspan=6, sticky="nsew", padx=10, pady=5)
        self.template_preview_image = None

        # Start with settings panel hidden
        self.template_settings_visible = False

        # Threshold (basic)
        threshold_row = ttk.Frame(config_frame)
        threshold_row.pack(fill=tk.X, pady=2)
        ttk.Label(threshold_row, text=self._t("lbl_threshold")).pack(side=tk.LEFT)
        threshold_scale = ttk.Scale(
            threshold_row,
            from_=0.5,
            to=0.99,
            orient=tk.HORIZONTAL,
            variable=self.match_threshold_var,
        )
        threshold_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.threshold_label = ttk.Label(threshold_row, text=f"{self.match_threshold_var.get():.2f}")
        self.threshold_label.pack(side=tk.LEFT)
        self.match_threshold_var.trace_add("write", self._update_threshold_label)

        # Scan interval (basic)
        scan_row = ttk.Frame(config_frame)
        scan_row.pack(fill=tk.X, pady=2)
        ttk.Label(scan_row, text=self._t("lbl_scan_interval")).pack(side=tk.LEFT)
        scan_min_entry = ttk.Entry(scan_row, textvariable=self.scan_interval_min_var, width=6)
        scan_min_entry.pack(side=tk.LEFT, padx=(5, 2))
        ttk.Label(scan_row, text="-").pack(side=tk.LEFT)
        scan_max_entry = ttk.Entry(scan_row, textvariable=self.scan_interval_max_var, width=6)
        scan_max_entry.pack(side=tk.LEFT, padx=(2, 5))

        # Move duration (basic)
        move_row = ttk.Frame(config_frame)
        move_row.pack(fill=tk.X, pady=2)
        ttk.Label(move_row, text=self._t("lbl_move_time")).pack(side=tk.LEFT)
        move_min_entry = ttk.Entry(move_row, textvariable=self.move_duration_min_var, width=6)
        move_min_entry.pack(side=tk.LEFT, padx=(5, 2))
        ttk.Label(move_row, text="-").pack(side=tk.LEFT)
        move_max_entry = ttk.Entry(move_row, textvariable=self.move_duration_max_var, width=6)
        move_max_entry.pack(side=tk.LEFT, padx=(2, 5))

        # Confirm before starting (basic)
        confirm_row = ttk.Frame(config_frame)
        confirm_row.pack(fill=tk.X, pady=2)
        confirm_check = ttk.Checkbutton(
            confirm_row,
            text=self._t("chk_confirm_start"),
            variable=self.confirm_on_start_var,
        )
        confirm_check.pack(side=tk.LEFT)

        # Toggle for advanced settings
        toggle_adv_row = ttk.Frame(config_frame)
        toggle_adv_row.pack(fill=tk.X, pady=(4, 0))
        self.advanced_toggle_button = ttk.Button(
            toggle_adv_row,
            text=self._t("btn_show_extra"),
            command=self.on_toggle_advanced_settings,
        )
        self.advanced_toggle_button.pack(side=tk.LEFT)

        # Advanced settings frame (initially hidden)
        self.advanced_frame = ttk.LabelFrame(main_frame, text=self._t("frame_extra_options"))
        advanced_frame = self.advanced_frame

        # Monitor selection (point 5: descriptive names)
        monitor_row = ttk.Frame(advanced_frame)
        monitor_row.pack(fill=tk.X, pady=2)
        ttk.Label(monitor_row, text=self._t("lbl_monitor")).pack(side=tk.LEFT)

        # Build descriptive monitor list
        monitor_display_values = []
        self._monitor_index_map: List[int] = []  # maps combo index -> mss monitor index
        if MSS_AVAILABLE:
            try:
                with mss() as sct_mon:
                    all_monitors = sct_mon.monitors  # index 0 = combined virtual, 1+ = real monitors
                    real_monitors = [
                        (i, mon) for i, mon in enumerate(all_monitors) if i != 0
                    ]
                    # Sort so the primary monitor (x=0, y=0) always comes first
                    real_monitors.sort(key=lambda pair: (
                        0 if (pair[1].get("left", -1) == 0 and pair[1].get("top", -1) == 0) else 1,
                        pair[0]
                    ))
                    for display_num, (i, mon) in enumerate(real_monitors, start=1):
                        w = mon.get("width", 0)
                        h = mon.get("height", 0)
                        x = mon.get("left", 0)
                        y = mon.get("top", 0)
                        # Primary monitor is always at position (0, 0) on all platforms
                        is_primary = (x == 0 and y == 0)
                        if is_primary:
                            label = self._t("monitor_primary", idx=display_num, w=w, h=h)
                        else:
                            label = self._t("monitor_label", idx=display_num, w=w, h=h, x=x, y=y)
                        monitor_display_values.append(label)
                        self._monitor_index_map.append(i)
            except Exception:
                pass

        if not monitor_display_values:
            monitor_display_values = ["Monitor 1"]
            self._monitor_index_map = [1]

        # Find display value matching the saved monitor index
        saved_idx = int(self.monitor_index_var.get())
        try:
            saved_combo_idx = self._monitor_index_map.index(saved_idx)
        except ValueError:
            saved_combo_idx = 0

        self.monitor_display_var = tk.StringVar(value=monitor_display_values[saved_combo_idx])
        self.monitor_combo = ttk.Combobox(
            monitor_row,
            values=monitor_display_values,
            textvariable=self.monitor_display_var,
            state="readonly",
            width=40,
        )
        self.monitor_combo.pack(side=tk.LEFT, padx=(5, 10))

        def _on_monitor_selected(event=None):
            combo_idx = self.monitor_combo.current()
            if 0 <= combo_idx < len(self._monitor_index_map):
                self.monitor_index_var.set(self._monitor_index_map[combo_idx])

        self.monitor_combo.bind("<<ComboboxSelected>>", _on_monitor_selected)

        # Search region controls
        region_row = ttk.Frame(advanced_frame)
        region_row.pack(fill=tk.X, pady=2)
        set_region_btn = ttk.Button(region_row, text=self._t("btn_set_region"), command=self.on_set_search_region)
        set_region_btn.pack(side=tk.LEFT, padx=(0, 5))
        clear_region_btn = ttk.Button(region_row, text=self._t("btn_clear_region"), command=self.on_clear_search_region)
        clear_region_btn.pack(side=tk.LEFT)

        # Auto-stop and limits
        auto_row = ttk.Frame(advanced_frame)
        auto_row.pack(fill=tk.X, pady=2)
        ttk.Label(auto_row, text=self._t("lbl_auto_stop")).pack(side=tk.LEFT)
        auto_entry = ttk.Entry(auto_row, textvariable=self.auto_stop_minutes_var, width=6)
        auto_entry.pack(side=tk.LEFT, padx=(5, 10))

        max_clicks_row = ttk.Frame(advanced_frame)
        max_clicks_row.pack(fill=tk.X, pady=2)
        ttk.Label(max_clicks_row, text=self._t("lbl_max_clicks_run")).pack(side=tk.LEFT)
        max_clicks_entry = ttk.Entry(max_clicks_row, textvariable=self.global_max_clicks_var, width=8)
        max_clicks_entry.pack(side=tk.LEFT, padx=(5, 10))

        idle_row = ttk.Frame(advanced_frame)
        idle_row.pack(fill=tk.X, pady=2)
        ttk.Label(idle_row, text=self._t("lbl_idle")).pack(side=tk.LEFT)
        idle_entry = ttk.Entry(idle_row, textvariable=self.random_idle_minutes_var, width=6)
        idle_entry.pack(side=tk.LEFT, padx=(5, 10))

        # Hotkey row (point 6)
        hotkey_row = ttk.Frame(advanced_frame)
        hotkey_row.pack(fill=tk.X, pady=2)
        ttk.Label(hotkey_row, text=self._t("lbl_hotkey")).pack(side=tk.LEFT)
        self.hotkey_label = ttk.Label(hotkey_row, text=self.hotkey, width=10, relief="sunken", anchor="center")
        self.hotkey_label.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(hotkey_row, text=self._t("btn_set_hotkey"), command=self.on_set_hotkey).pack(side=tk.LEFT)

        # Start/Stop/Pause buttons
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=5)

        self.start_button = ttk.Button(controls_frame, text=self._t("btn_start"), command=self.on_start)
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))

        self.stop_button = ttk.Button(controls_frame, text=self._t("btn_stop"), command=self.on_stop, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 5))

        self.pause_button = ttk.Button(controls_frame, text=self._t("btn_pause"), command=self.on_toggle_pause, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 5))

        self.status_label = ttk.Label(controls_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=10)

        # Log window (pinned to bottom)
        log_frame = ttk.LabelFrame(main_frame, text=self._t("frame_log"))
        log_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=(5, 0))

        log_top_row = ttk.Frame(log_frame)
        log_top_row.pack(fill=tk.X, padx=5, pady=(3, 0))
        ttk.Button(log_top_row, text=self._t("btn_clear_log"), command=self.on_clear_log).pack(side=tk.RIGHT)

        self.log_text = tk.Text(log_frame, height=10, wrap="word", state=tk.DISABLED)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)

        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scroll.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5), pady=5)
        self.log_text.configure(yscrollcommand=log_scroll.set)

    def _update_threshold_label(self, *args) -> None:
        try:
            value = float(self.match_threshold_var.get())
        except (tk.TclError, ValueError):
            value = 0.0
        self.threshold_label.config(text=f"{value:.2f}")

    # ---------------- Config management -----------------
    def _load_config(self) -> Dict[str, object]:
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
        except Exception:
            # On any error, fall back to defaults
            pass
        return {}

    def _save_config(self) -> None:
        # Capture current window size — but only when not maximized/zoomed,
        # so we never persist the full-screen dimensions.
        try:
            is_maximized = self.state() in ("zoomed", "iconic")
        except Exception:
            is_maximized = False

        if is_maximized:
            # Reuse the last known normal size stored in config
            try:
                win_w = int(self.config.get("window_width", 700))
                win_h = int(self.config.get("window_height", 500))
            except Exception:
                win_w, win_h = 700, 500
        else:
            try:
                win_w = int(self.winfo_width())
                win_h = int(self.winfo_height())
            except Exception:
                win_w, win_h = 700, 500

        data: Dict[str, object] = {
            "threshold": float(self.match_threshold_var.get()),
            "scan_min": float(self.scan_interval_min_var.get()),
            "scan_max": float(self.scan_interval_max_var.get()),
            "move_min": float(self.move_duration_min_var.get()),
            "move_max": float(self.move_duration_max_var.get()),
            "monitor_index": int(self.monitor_index_var.get()),
            "auto_stop_minutes": float(self.auto_stop_minutes_var.get()),
            "global_max_clicks": int(self.global_max_clicks_var.get()),
            "idle_minutes": float(self.random_idle_minutes_var.get()),
            "confirm_on_start": bool(self.confirm_on_start_var.get()),
            "search_region": list(self.search_region) if self.search_region is not None else None,
            "window_width": win_w,
            "window_height": win_h,
            "language": self.language,
            "hotkey": self.hotkey,
        }
        # Preserve last used preset if already set in memory
        last_preset = self.config.get("last_preset") if isinstance(self.config, dict) else None
        if last_preset:
            data["last_preset"] = last_preset
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.config = data
        except Exception:
            # Config saving failures are non-fatal
            pass

    # ---------------- Presets management -----------------
    def _load_presets(self) -> None:
        """Load presets from disk into memory and refresh the combo box."""
        self.presets = {}
        if os.path.exists(self.presets_path):
            try:
                with open(self.presets_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    for name, files in data.items():
                        if isinstance(files, list):
                            self.presets[str(name)] = [str(fn) for fn in files]
            except Exception as e:
                self.log(self._t("log_preset_load_failed", e=e))
                self.presets = {}
        self._refresh_presets_combo()

        # Auto-load last used preset if present in config
        last_preset = None
        if isinstance(self.config, dict):
            last_preset = self.config.get("last_preset")
        if isinstance(last_preset, str) and last_preset in self.presets:
            # Set combo box display and load templates
            display = self._preset_display_name(last_preset)
            if display:
                self.preset_var.set(display)
            self._load_preset_by_name(last_preset)

    def _save_presets(self) -> None:
        """Persist presets to disk."""
        try:
            with open(self.presets_path, "w", encoding="utf-8") as f:
                json.dump(self.presets, f, indent=2)
        except Exception as e:
            self.log(self._t("log_preset_save_failed", e=e))

    def _preset_display_name(self, name: str) -> str:
        files = self.presets.get(name)
        count = len(files) if isinstance(files, list) else 0
        return f"{name} ({count})"

    def _parse_preset_display(self, display: str) -> str:
        # Expected format: "Name (N)"; fall back to full string if parsing fails
        if "(" in display:
            return display.split("(", 1)[0].strip()
        return display.strip()

    def _refresh_presets_combo(self) -> None:
        names = sorted(self.presets.keys())
        displays = [self._preset_display_name(n) for n in names]
        self.preset_combo["values"] = displays
        # Keep selection if still present
        current_display = self.preset_var.get()
        current_name = self._parse_preset_display(current_display) if current_display else ""
        if current_name in self.presets:
            self.preset_var.set(self._preset_display_name(current_name))
        elif names:
            self.preset_var.set(self._preset_display_name(names[0]))
        else:
            self.preset_var.set("")

    def on_save_preset(self) -> None:
        """Save the currently loaded templates as a named preset."""
        if not self.templates:
            messagebox.showwarning(self._t("dlg_no_preset_templates_title"), self._t("dlg_no_preset_templates_msg"))
            return

        default_name = time.strftime("Preset_%Y%m%d_%H%M%S")
        name = simpledialog.askstring(
            self._t("dlg_save_preset_title"),
            self._t("dlg_save_preset_msg"),
            initialvalue=default_name,
            parent=self,
        )
        if name is None:
            return

        name = name.strip()
        if not name:
            messagebox.showwarning(self._t("dlg_preset_name_empty_title"), self._t("dlg_preset_name_empty_msg"))
            return

        # Sanitize name for JSON key and UI; file names are stored separately
        invalid_chars = '\\/:*?"<>|'
        for ch in invalid_chars:
            name = name.replace(ch, "_")

        # Collect basenames of templates (they should all be in Templates folder)
        files = [os.path.basename(t.path) for t in self.templates]
        self.presets[name] = files
        # Track last used preset in config
        if isinstance(self.config, dict):
            self.config["last_preset"] = name
        else:
            self.config = {"last_preset": name}
        self._save_presets()
        self._save_config()
        self._refresh_presets_combo()
        self.preset_var.set(self._preset_display_name(name))
        self.log(self._t("log_preset_saved", name=name, count=len(files)))

    def _load_preset_by_name(self, name: str) -> None:
        files = self.presets.get(name)
        if not files:
            messagebox.showwarning(self._t("dlg_empty_preset_title"), self._t("dlg_empty_preset_msg", name=name))
            return

        # Clear current templates
        self.templates.clear()
        self.templates_listbox.delete(0, tk.END)

        loaded = 0
        missing = 0
        for filename in files:
            path = os.path.join(self.templates_dir, filename)
            if os.path.exists(path):
                self._add_template_from_path(path)
                loaded += 1
            else:
                self.log(self._t("log_preset_missing_tpl", name=name, filename=filename))
                missing += 1

        # Update last_preset in config
        if isinstance(self.config, dict):
            self.config["last_preset"] = name
        else:
            self.config = {"last_preset": name}
        self._save_config()

        self.log(self._t("log_preset_loaded", name=name, loaded=loaded, missing=missing))

    def on_load_preset(self) -> None:
        """Load templates based on the selected preset."""
        display = self.preset_var.get().strip()
        if not display:
            messagebox.showwarning(self._t("dlg_no_preset_title"), self._t("dlg_no_preset_msg"))
            return

        name = self._parse_preset_display(display)
        if name not in self.presets:
            messagebox.showwarning(self._t("dlg_preset_not_found_title"), self._t("dlg_preset_not_found_msg", name=name))
            return

        self._load_preset_by_name(name)

    def on_delete_preset(self) -> None:
        """Delete the selected preset from the list and disk."""
        display = self.preset_var.get().strip()
        if not display:
            messagebox.showwarning(self._t("dlg_no_preset_delete_title"), self._t("dlg_no_preset_delete_msg"))
            return

        name = self._parse_preset_display(display)
        if name not in self.presets:
            messagebox.showwarning(self._t("dlg_preset_not_found_title"), self._t("dlg_preset_not_found_msg", name=name))
            return

        confirm = messagebox.askyesno(
            self._t("dlg_delete_preset_title"),
            self._t("dlg_delete_preset_msg", name=name),
            parent=self,
        )
        if not confirm:
            return

        del self.presets[name]
        self._save_presets()
        # Clear last_preset if it was pointing to this one
        if isinstance(self.config, dict) and self.config.get("last_preset") == name:
            self.config["last_preset"] = None
            self._save_config()
        self._refresh_presets_combo()
        self.log(self._t("log_preset_deleted", name=name))

    # ---------------- Template management -----------------
    def _template_display_text(self, item: TemplateItem) -> str:
        basename = os.path.basename(item.path)
        if item.image is None:
            return f"{self._t('tpl_tag_missing')} {basename}"
        prefix = f"{self._t('tpl_tag_off')} " if not item.enabled else ""
        return f"{prefix}{basename} ({item.width}x{item.height})"

    def _refresh_templates_listbox(self) -> None:
        self.templates_listbox.delete(0, tk.END)
        for item in self.templates:
            self.templates_listbox.insert(tk.END, self._template_display_text(item))

    def _add_template_from_path(self, path: str) -> None:
        """Load a template image from disk and add it to the list."""
        template_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if template_img is None:
            # Mark as missing but keep an entry so presets remain consistent
            item = TemplateItem(path=path, image=None, width=0, height=0, enabled=False)
            self.templates.append(item)
            self.log(self._t("log_tpl_load_failed", path=path))
            self._refresh_templates_listbox()
            return

        h, w = template_img.shape[:2]
        item = TemplateItem(path=path, image=template_img, width=w, height=h)
        self.templates.append(item)
        self.log(self._t("log_tpl_added", path=path, w=w, h=h))
        self._refresh_templates_listbox()

    def on_add_template(self) -> None:
        filetypes = [
            (self._t("filetype_images"), "*.png;*.jpg;*.jpeg;*.bmp"),
            ("PNG", "*.png"),
            ("JPEG", "*.jpg;*.jpeg"),
            ("Bitmap", "*.bmp"),
            (self._t("filetype_all"), "*.*"),
        ]
        path = filedialog.askopenfilename(
            title=self._t("dlg_select_template_title"),
            filetypes=filetypes,
            initialdir=self.templates_dir,
        )
        if not path:
            return

        # Ensure the file is stored in the Templates directory
        dest_path = os.path.join(self.templates_dir, os.path.basename(path))
        try:
            if os.path.abspath(path) != os.path.abspath(dest_path):
                shutil.copy2(path, dest_path)
                self.log(self._t("log_tpl_copied", path=dest_path))
            else:
                dest_path = path
        except Exception as e:
            messagebox.showerror(self._t("dlg_copy_error_title"), self._t("dlg_copy_error_msg", e=e))
            return

        self._add_template_from_path(dest_path)

    def on_create_template(self) -> None:
        """Create a new template by selecting a region of the screen."""
        if not messagebox.askokcancel(
            self._t("dlg_create_tpl_title"),
            self._t("dlg_create_tpl_msg"),
        ):
            return

        # Hide main window so it is not captured in the template
        self.withdraw()

        overlay = tk.Toplevel(self)
        self._apply_icon(overlay)
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.25)
        overlay.attributes("-topmost", True)
        overlay.config(bg="black", cursor="cross")

        canvas = tk.Canvas(overlay, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        state = {"x1": None, "y1": None, "rect": None}

        def on_press(event: tk.Event) -> None:
            state["x1"] = event.x_root
            state["y1"] = event.y_root
            state["rect"] = canvas.create_rectangle(
                event.x, event.y, event.x, event.y, outline="red", width=2
            )

        def on_move(event: tk.Event) -> None:
            if state["rect"] is not None and state["x1"] is not None and state["y1"] is not None:
                canvas.coords(
                    state["rect"],
                    state["x1"] - overlay.winfo_rootx(),
                    state["y1"] - overlay.winfo_rooty(),
                    event.x,
                    event.y,
                )

        def finish_selection(x1: int, y1: int, x2: int, y2: int) -> None:
            overlay.destroy()
            self.after(100, self.deiconify)

            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            if width < 5 or height < 5:
                self.log(self._t("log_tpl_create_too_small"))
                return

            # Ask user for a template name
            default_name = time.strftime("template_%Y%m%d_%H%M%S")
            self.deiconify()
            self.lift()
            self.focus_force()
            self.update()
            name = simpledialog.askstring(
                self._t("dlg_tpl_name_title"),
                self._t("dlg_tpl_name_msg"),
                initialvalue=default_name,
                parent=self,
            )
            if name is None:
                self.log(self._t("log_tpl_create_no_name"))
                return

            name = name.strip()
            if not name:
                self.log(self._t("log_tpl_create_empty_name"))
                return

            # Sanitize filename: replace invalid characters
            invalid_chars = '\\/:*?"<>|'
            for ch in invalid_chars:
                name = name.replace(ch, "_")
            filename = f"{name}.png"
            save_path = os.path.join(self.templates_dir, filename)

            # Handle overwrite
            if os.path.exists(save_path):
                overwrite = messagebox.askyesno(
                    self._t("dlg_tpl_overwrite_title"),
                    self._t("dlg_tpl_overwrite_msg", filename=filename),
                    parent=self,
                )
                if not overwrite:
                    self.log(self._t("log_tpl_create_no_overwrite"))
                    return

            try:
                screenshot = pyautogui.screenshot(region=(left, top, width, height))
                screenshot.save(save_path)
                self.log(self._t("log_tpl_saved", path=save_path))
                self._add_template_from_path(save_path)
            except Exception as e:
                messagebox.showerror(self._t("dlg_create_error_title"), self._t("dlg_create_error_msg", e=e))

        def on_release(event: tk.Event) -> None:
            if state["x1"] is None or state["y1"] is None:
                overlay.destroy()
                self.after(100, self.deiconify)
                return
            x1 = int(state["x1"])
            y1 = int(state["y1"])
            x2 = int(event.x_root)
            y2 = int(event.y_root)
            finish_selection(x1, y1, x2, y2)

        def on_escape(event: tk.Event) -> None:  # type: ignore[unused-argument]
            overlay.destroy()
            self.after(100, self.deiconify)
            self.log(self._t("log_tpl_create_cancelled"))

        overlay.bind("<ButtonPress-1>", on_press)
        overlay.bind("<B1-Motion>", on_move)
        overlay.bind("<ButtonRelease-1>", on_release)
        overlay.bind("<Escape>", on_escape)

        overlay.focus_set()

    def _move_template(self, src: int, dst: int) -> None:
        """Move the template at index src to index dst, keeping the selection on the moved item."""
        if src == dst or src < 0 or dst < 0:
            return
        if src >= len(self.templates) or dst >= len(self.templates):
            return
        item = self.templates.pop(src)
        self.templates.insert(dst, item)
        self._refresh_templates_listbox()
        self.templates_listbox.selection_clear(0, tk.END)
        self.templates_listbox.selection_set(dst)
        self.templates_listbox.see(dst)
        # Keep the template-settings panel in sync if it is open
        if self.template_settings_visible:
            self._load_selected_template_into_settings()
        self.log(self._t("log_tpl_moved", name=os.path.basename(item.path), src=src + 1, dst=dst + 1))

    def on_remove_selected_template(self) -> None:
        selection = list(self.templates_listbox.curselection())
        if not selection:
            return
        # Remove from the end to keep indices valid
        for index in reversed(selection):
            item = self.templates.pop(index)
            self.log(self._t("log_tpl_removed", path=item.path))
        self._refresh_templates_listbox()

    def on_open_templates_folder(self) -> None:
        """Open the Templates folder in the system file explorer."""
        try:
            if os.name == "nt":
                os.startfile(self.templates_dir)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.templates_dir])
            else:
                subprocess.Popen(["xdg-open", self.templates_dir])
        except Exception as e:
            messagebox.showerror(self._t("dlg_folder_error_title"), self._t("dlg_folder_error_msg", e=e))

    # ---------------- Template selection & settings -----------------
    def _get_selected_template_index(self) -> Optional[int]:
        selection = self.templates_listbox.curselection()
        if not selection:
            return None
        return int(selection[0])

    def on_template_selected(self, event: tk.Event) -> None:  # type: ignore[unused-argument]
        if self.template_settings_visible:
            self._load_selected_template_into_settings()

    def _load_selected_template_into_settings(self) -> None:
        idx = self._get_selected_template_index()
        if idx is None or idx >= len(self.templates):
            self.template_name_var.set(self._t("lbl_no_template"))
            self.template_enabled_var.set(True)
            for entry in (
                self.template_threshold_entry,
                self.template_cooldown_entry,
                self.template_max_clicks_entry,
                self.template_stop_after_entry,
            ):
                entry.delete(0, tk.END)
            self.template_preview_label.config(text=self._t("lbl_no_preview"), image="")
            self.template_preview_image = None
            return

        item = self.templates[idx]
        basename = os.path.basename(item.path)
        display_name = basename
        if item.image is None:
            display_name = f"{self._t('tpl_tag_missing')} {basename}"
        self.template_name_var.set(display_name)
        self.template_enabled_var.set(bool(item.enabled))

        # Threshold
        self.template_threshold_entry.delete(0, tk.END)
        if item.custom_threshold is not None:
            self.template_threshold_entry.insert(0, f"{item.custom_threshold:.3f}")

        # Cooldown
        self.template_cooldown_entry.delete(0, tk.END)
        if item.click_cooldown is not None:
            self.template_cooldown_entry.insert(0, f"{item.click_cooldown:.2f}")

        # Max clicks per run
        self.template_max_clicks_entry.delete(0, tk.END)
        if item.max_clicks_per_run is not None:
            self.template_max_clicks_entry.insert(0, str(item.max_clicks_per_run))

        # Stop run after clicks
        self.template_stop_after_entry.delete(0, tk.END)
        if item.stop_after_clicks is not None:
            self.template_stop_after_entry.insert(0, str(item.stop_after_clicks))

        # Preview (scaled to a fixed max size so large templates don't break layout)
        self.template_preview_label.config(text="", image="")
        self.template_preview_image = None
        if item.image is not None:
            try:
                img = tk.PhotoImage(file=item.path)
                max_w, max_h = 150, 150
                w, h = img.width(), img.height()
                if w > max_w or h > max_h:
                    # Compute integer subsample factor to fit within max_w x max_h
                    scale = max(w / max_w, h / max_h)
                    factor = max(1, int(scale))
                    img = img.subsample(factor, factor)
                self.template_preview_image = img
                self.template_preview_label.config(image=img)
            except Exception:
                self.template_preview_label.config(text=self._t("lbl_no_preview"))
        else:
            self.template_preview_label.config(text=self._t("lbl_missing_image"))

    def on_toggle_template_settings_panel(self) -> None:
        visible = self.template_settings_visible
        if not visible:
            # Show panel
            self.template_settings_frame.pack(fill=tk.X, expand=False, side=tk.TOP, padx=5, pady=5)
            self.template_settings_visible = True
            self._load_selected_template_into_settings()
        else:
            # Hide panel
            self.template_settings_frame.pack_forget()
            self.template_settings_visible = False

    def on_apply_template_settings(self) -> None:
        idx = self._get_selected_template_index()
        if idx is None or idx >= len(self.templates):
            messagebox.showwarning(self._t("dlg_no_tpl_selected_title"), self._t("dlg_no_tpl_selected_msg"))
            return

        item = self.templates[idx]

        # Enabled flag
        item.enabled = bool(self.template_enabled_var.get())

        # Match accuracy (per template)
        th_text = self.template_threshold_entry.get().strip()
        if th_text:
            try:
                th_val = float(th_text)
                if not (0.0 < th_val <= 1.0):
                    raise ValueError
                item.custom_threshold = th_val
            except ValueError:
                messagebox.showerror(self._t("dlg_tpl_threshold_title"), self._t("dlg_tpl_threshold_msg"))
                return
        else:
            item.custom_threshold = None

        # Wait time between clicks (per template)
        cd_text = self.template_cooldown_entry.get().strip()
        if cd_text:
            try:
                cd_val = float(cd_text)
                if cd_val < 0.0:
                    raise ValueError
                item.click_cooldown = cd_val
            except ValueError:
                messagebox.showerror(self._t("dlg_tpl_cooldown_title"), self._t("dlg_tpl_cooldown_msg"))
                return
        else:
            item.click_cooldown = None

        # Max clicks per run (per template)
        mc_text = self.template_max_clicks_entry.get().strip()
        if mc_text:
            try:
                mc_val = int(mc_text)
                if mc_val < 0:
                    raise ValueError
                item.max_clicks_per_run = mc_val if mc_val > 0 else None
            except ValueError:
                messagebox.showerror(self._t("dlg_tpl_maxclicks_title"), self._t("dlg_tpl_maxclicks_msg"))
                return
        else:
            item.max_clicks_per_run = None

        # Stop run after clicks (per template)
        stop_text = self.template_stop_after_entry.get().strip()
        if stop_text:
            try:
                stop_val = int(stop_text)
                if stop_val < 0:
                    raise ValueError
                item.stop_after_clicks = stop_val if stop_val > 0 else None
            except ValueError:
                messagebox.showerror(self._t("dlg_tpl_stopafter_title"), self._t("dlg_tpl_stopafter_msg"))
                return
        else:
            item.stop_after_clicks = None

        # Refresh listbox to reflect enabled/disabled and any [OFF] tag
        self._refresh_templates_listbox()
        self.log(self._t("log_tpl_settings_updated", path=item.path))

    def on_toggle_template_enabled(self) -> None:
        idx = self._get_selected_template_index()
        if idx is None or idx >= len(self.templates):
            messagebox.showwarning(self._t("dlg_tpl_toggle_title"), self._t("dlg_tpl_toggle_msg"))
            return
        item = self.templates[idx]
        item.enabled = not item.enabled
        self._refresh_templates_listbox()
        if self.template_settings_visible:
            self._load_selected_template_into_settings()
        key = "log_tpl_enabled" if item.enabled else "log_tpl_disabled"
        self.log(self._t(key, name=os.path.basename(item.path)))

    # ---------------- Search region control -----------------
    def on_set_search_region(self) -> None:
        """Let the user visually select a search region on screen."""
        if not messagebox.askokcancel(
            self._t("dlg_set_region_title"),
            self._t("dlg_set_region_msg"),
        ):
            return

        # Hide main window to keep it out of the way
        self.withdraw()

        overlay = tk.Toplevel(self)
        self._apply_icon(overlay)
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.25)
        overlay.attributes("-topmost", True)
        overlay.config(bg="black", cursor="cross")

        canvas = tk.Canvas(overlay, bg="black", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        state = {"x1": None, "y1": None, "rect": None}

        def on_press(event: tk.Event) -> None:
            state["x1"] = event.x_root
            state["y1"] = event.y_root
            state["rect"] = canvas.create_rectangle(
                event.x, event.y, event.x, event.y, outline="green", width=2
            )

        def on_move(event: tk.Event) -> None:
            if state["rect"] is not None and state["x1"] is not None and state["y1"] is not None:
                canvas.coords(
                    state["rect"],
                    state["x1"] - overlay.winfo_rootx(),
                    state["y1"] - overlay.winfo_rooty(),
                    event.x,
                    event.y,
                )

        def finish_selection(x1: int, y1: int, x2: int, y2: int) -> None:
            overlay.destroy()
            self.after(100, self.deiconify)

            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)

            if width < 10 or height < 10:
                self.log(self._t("log_region_too_small"))
                return

            self.search_region = (left, top, width, height)
            self._save_config()
            self.log(self._t("log_region_set", left=left, top=top, w=width, h=height))

        def on_release(event: tk.Event) -> None:
            if state["x1"] is None or state["y1"] is None:
                overlay.destroy()
                self.after(100, self.deiconify)
                return
            x1 = int(state["x1"])
            y1 = int(state["y1"])
            x2 = int(event.x_root)
            y2 = int(event.y_root)
            finish_selection(x1, y1, x2, y2)

        def on_escape(event: tk.Event) -> None:  # type: ignore[unused-argument]
            overlay.destroy()
            self.after(100, self.deiconify)
            self.log(self._t("log_region_cancelled"))

        overlay.bind("<ButtonPress-1>", on_press)
        overlay.bind("<B1-Motion>", on_move)
        overlay.bind("<ButtonRelease-1>", on_release)
        overlay.bind("<Escape>", on_escape)

        overlay.focus_set()

    def on_clear_search_region(self) -> None:
        """Clear any custom search region so the full monitor is used."""
        if self.search_region is None:
            self.log(self._t("log_region_none_to_clear"))
            return
        self.search_region = None
        self._save_config()
        self.log(self._t("log_region_cleared"))

    # ---------------- Start/Stop control -----------------
    def on_start(self) -> None:
        if not self.templates:
            messagebox.showwarning(self._t("dlg_no_templates_title"), self._t("dlg_no_templates_msg"))
            return

        if self.worker_thread and self.worker_thread.is_alive():
            return

        # Snapshot settings
        try:
            threshold = float(self.match_threshold_var.get())
            scan_min = float(self.scan_interval_min_var.get())
            scan_max = float(self.scan_interval_max_var.get())
            move_min = float(self.move_duration_min_var.get())
            move_max = float(self.move_duration_max_var.get())
        except ValueError:
            messagebox.showerror(self._t("dlg_invalid_settings_title"), self._t("dlg_invalid_settings_msg"))
            return

        # Clamp and validate match accuracy and timings to reasonable ranges
        if not (0.1 <= threshold <= 0.99):
            messagebox.showerror(self._t("dlg_threshold_title"), self._t("dlg_threshold_msg"))
            return

        if scan_min < 0.05 or scan_max < 0.05 or scan_min > scan_max:
            messagebox.showerror(self._t("dlg_scan_title"), self._t("dlg_scan_msg"))
            return

        if move_min < 0.01 or move_max < 0.01 or move_min > move_max:
            messagebox.showerror(self._t("dlg_move_title"), self._t("dlg_move_msg"))
            return

        if not MSS_AVAILABLE:
            if not messagebox.askyesno(self._t("dlg_mss_title"), self._t("dlg_mss_msg")):
                return

        # Warn if any templates are missing (image failed to load)
        missing_count = sum(1 for t in self.templates if t.image is None)
        if missing_count > 0:
            if not messagebox.askyesno(
                self._t("dlg_missing_tpl_title"),
                self._t("dlg_missing_tpl_msg", count=missing_count),
            ):
                return

        config = {
            "threshold": threshold,
            "scan_min": scan_min,
            "scan_max": scan_max,
            "move_min": move_min,
            "move_max": move_max,
        }

        # Optional confirmation
        if bool(self.confirm_on_start_var.get()):
            total = len(self.templates)
            enabled = sum(1 for t in self.templates if t.enabled and t.image is not None)
            if not messagebox.askyesno(
                self._t("dlg_confirm_start_title"),
                self._t("dlg_confirm_start_msg", enabled=enabled, total=total),
            ):
                return

        # Interpret additional limits
        try:
            auto_stop_min = float(self.auto_stop_minutes_var.get())
        except Exception:
            auto_stop_min = 0.0
        try:
            global_max_clicks = int(self.global_max_clicks_var.get())
        except Exception:
            global_max_clicks = 0
        try:
            idle_min = float(self.random_idle_minutes_var.get())
        except Exception:
            idle_min = 0.0

        config["auto_stop_minutes"] = auto_stop_min
        config["global_max_clicks"] = global_max_clicks
        config["idle_minutes"] = idle_min

        # Snapshot region and monitor index here (main thread) to avoid cross-thread access
        config["search_region"] = self.search_region
        config["monitor_index"] = int(self.monitor_index_var.get())

        # Reset run metrics and template runtime counters
        self.total_clicks_this_run = 0
        self.run_start_time = time.time()
        self.last_idle_time = self.run_start_time
        for t in self.templates:
            t.clicks_this_run = 0
            t.last_click_time = 0.0
            t.last_region = None

        # Clear paused state and start worker
        self.paused = False
        self.running_event.set()

        # Persist config whenever the bot actually starts
        try:
            self._save_config()
        except Exception:
            pass

        self.worker_thread = threading.Thread(target=self._worker_loop, args=(config,), daemon=True)
        self.worker_thread.start()

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.NORMAL, text=self._t("btn_pause"))
        self.log(self._t("log_started"))
        self._update_status(self._t("status_running"))

    def on_stop(self) -> None:
        if not self.running_event.is_set():
            return
        self.running_event.clear()
        self.paused = False
        self.log(self._t("log_stopping"))
        self._update_status(self._t("status_stopping"))

    def on_close(self) -> None:
        self._stop_hotkey_listener()
        self.running_event.clear()
        if self.worker_thread and self.worker_thread.is_alive():
            # Give the worker some time to stop
            self.log(self._t("log_worker_stopped_wait"))
            self.worker_thread.join(timeout=2.0)

        # Persist latest config (including window size) before closing
        try:
            self._save_config()
        except Exception:
            pass

        self.destroy()

    # ---------------- Logging (thread-safe) -----------------
    def log(self, message: str) -> None:
        timestamp = time.strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        # Append to on-screen log
        self.after(0, self._append_log, line)
        # Also write to a small rolling logfile for diagnostics
        self._write_log_file(line)

    def _append_log(self, line: str) -> None:
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        # Keep only the last 500 lines to prevent unbounded memory growth
        line_count = int(self.log_text.index("end-1c").split(".")[0])
        if line_count > 500:
            self.log_text.delete("1.0", f"{line_count - 500}.0")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _write_log_file(self, line: str) -> None:
        """Write a single log line to duel_helper.log, rotating to .bak if it grows too large."""
        try:
            path = self.log_file_path
            max_size = 1_000_000  # ~1 MB
            if os.path.exists(path) and os.path.getsize(path) > max_size:
                bak_path = path + ".bak"
                try:
                    if os.path.exists(bak_path):
                        os.remove(bak_path)
                    os.rename(path, bak_path)
                except Exception:
                    pass  # If rotation fails, just keep appending
            with open(path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception:
            # File logging failures are non-fatal and silently ignored
            pass

    # ---------------- Worker logic -----------------
    def _worker_loop(self, config: dict) -> None:
        threshold = config["threshold"]
        scan_min = config["scan_min"]
        scan_max = config["scan_max"]
        move_min = config["move_min"]
        move_max = config["move_max"]
        auto_stop_min = float(config.get("auto_stop_minutes", 0.0))
        global_max_clicks = int(config.get("global_max_clicks", 0))
        idle_min = float(config.get("idle_minutes", 0.0))
        search_region = config.get("search_region")  # snapshotted from main thread
        monitor_index = int(config.get("monitor_index", 1))  # snapshotted from main thread

        self.log(self._t("log_worker_started", threshold=f"{threshold:.2f}", scan_min=f"{scan_min:.2f}", scan_max=f"{scan_max:.2f}", move_min=f"{move_min:.2f}", move_max=f"{move_max:.2f}"))

        try:
            self._worker_inner(
                threshold, scan_min, scan_max, move_min, move_max,
                auto_stop_min, global_max_clicks, idle_min,
                search_region, monitor_index,
            )
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            self.log(self._t("log_crash", e=e))
            self.log(self._t("log_crash_tb", tb=tb))
        finally:
            self.running_event.clear()
            self.after(0, self._on_worker_stopped)

    def _worker_inner(
        self,
        threshold: float,
        scan_min: float,
        scan_max: float,
        move_min: float,
        move_max: float,
        auto_stop_min: float,
        global_max_clicks: int,
        idle_min: float,
        search_region,
        monitor_index: int,
    ) -> None:
        """Inner worker — runs the actual scan/click loop. Exceptions propagate to _worker_loop."""

        # Build the MSS context and resolve monitor once (or None for pyautogui fallback)
        sct_ctx = None
        mss_monitor = None
        if MSS_AVAILABLE:
            sct_ctx = mss()
            monitors = sct_ctx.monitors
            idx = monitor_index if 1 <= monitor_index < len(monitors) else 1
            mss_monitor = monitors[idx]

        def _grab_frame():
            """Capture one frame. Returns (frame_bgr, offset_x, offset_y)."""
            if sct_ctx is not None:
                if search_region is not None:
                    left, top, width, height = search_region
                    grab_region = {"left": left, "top": top, "width": width, "height": height}
                    offset_x, offset_y = left, top
                else:
                    grab_region = mss_monitor
                    offset_x = mss_monitor.get("left", 0)
                    offset_y = mss_monitor.get("top", 0)
                raw = np.array(sct_ctx.grab(grab_region))
                return raw[:, :, :3], offset_x, offset_y  # BGRA -> BGR
            else:
                # pyautogui fallback
                if search_region is not None:
                    left, top, width, height = search_region
                    shot = pyautogui.screenshot(region=(left, top, width, height))
                    frame = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
                    return frame, left, top
                else:
                    shot = pyautogui.screenshot()
                    frame = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2BGR)
                    return frame, 0, 0

        try:
            while self.running_event.is_set():
                # Pause handling
                if self.paused:
                    time.sleep(0.1)
                    continue

                # Global auto-stop / limits
                now = time.time()
                if auto_stop_min > 0.0 and (now - self.run_start_time) >= auto_stop_min * 60.0:
                    self.log(self._t("log_autostop_runtime"))
                    break
                with self._clicks_lock:
                    current_clicks = self.total_clicks_this_run
                if global_max_clicks > 0 and current_clicks >= global_max_clicks:
                    self.log(self._t("log_autostop_clicks"))
                    break

                frame_bgr, offset_x, offset_y = _grab_frame()
                self._process_frame_and_click(
                    frame_bgr, offset_x, offset_y, threshold, move_min, move_max
                )

                # Recalculate now after the click (which may have taken several seconds)
                # so the idle check reflects the actual elapsed time accurately.
                now = time.time()

                # Random idle behaviour
                if idle_min > 0.0 and (now - self.last_idle_time) >= idle_min * 60.0:
                    extra = random.uniform(3.0, 8.0)
                    self.log(self._t("log_idle_pause", secs=f"{extra:.1f}"))
                    time.sleep(extra)
                    self.last_idle_time = time.time()

                time.sleep(random.uniform(scan_min, scan_max))
        finally:
            if sct_ctx is not None:
                try:
                    sct_ctx.close()
                except Exception:
                    pass

    def _on_worker_stopped(self) -> None:
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.DISABLED, text=self._t("btn_pause"))
        self.log(self._t("log_stopped"))
        self._update_status(self._t("status_idle"))
        # Point 2: show session summary
        self._show_session_summary()

    def _show_session_summary(self) -> None:
        """Point 2: Show a popup with stats when the bot stops."""
        with self._clicks_lock:
            total = self.total_clicks_this_run
        if total == 0:
            return  # nothing interesting to report
        elapsed = time.time() - getattr(self, "run_start_time", time.time())
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        runtime = f"{mins}m {secs}s"
        lines = []
        for item in self.templates:
            if item.clicks_this_run > 0:
                name = os.path.basename(item.path)
                lines.append(f"  {name}: {item.clicks_this_run}")
        per_template = "\n".join(lines) if lines else "  —"
        messagebox.showinfo(
            self._t("dlg_session_title"),
            self._t("dlg_session_msg", total=total, runtime=runtime, per_template=per_template),
        )

    # ---------------- Clear log (point 1) -----------------
    def on_clear_log(self) -> None:
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

    # ---------------- Hotkey (point 6) -----------------
    def _apply_icon(self, window: tk.Toplevel) -> None:
        """Apply the app icon to any Toplevel dialog or window."""
        if self._tk_icon:
            try:
                window.iconphoto(False, self._tk_icon)
            except Exception:
                pass

    def _start_hotkey_listener(self) -> None:
        """Start a global (system-wide) hotkey listener using the keyboard library."""
        self._stop_hotkey_listener()
        if not self.hotkey:
            return
        try:
            import keyboard as kb

            # Map tkinter keysym names to what the keyboard library expects
            _KEYMAP = {
                "Prior": "page up",
                "Next": "page down",
                "BackSpace": "backspace",
                "Return": "enter",
                "Escape": "esc",
                "Print": "print screen",
                "space": "space",
            }
            key_name = _KEYMAP.get(self.hotkey, self.hotkey.lower())

            def _on_hotkey():
                self.after(0, self.on_toggle_pause)

            kb.add_hotkey(key_name, _on_hotkey, suppress=False)
            self._kb_hotkey_name = key_name

        except ImportError:
            # keyboard library not installed — fall back to tkinter binding
            self._kb_hotkey_name = None
            try:
                self.bind_all(f"<{self.hotkey}>", lambda e: self.on_toggle_pause())
            except Exception:
                pass
        except Exception:
            self._kb_hotkey_name = None
            try:
                self.bind_all(f"<{self.hotkey}>", lambda e: self.on_toggle_pause())
            except Exception:
                pass

    def _stop_hotkey_listener(self) -> None:
        # Stop keyboard library hotkey if active
        key_name = getattr(self, "_kb_hotkey_name", None)
        if key_name is not None:
            try:
                import keyboard as kb
                kb.remove_hotkey(key_name)
            except Exception:
                pass
            self._kb_hotkey_name = None
        # Also clean up any leftover tkinter binding
        try:
            self.unbind_all(f"<{self.hotkey}>")
        except Exception:
            pass

    def on_set_hotkey(self) -> None:
        """Open a small dialog that captures the next key press."""
        dialog = tk.Toplevel(self)
        self._apply_icon(dialog)
        dialog.title(self._t("dlg_hotkey_title"))
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.attributes("-topmost", True)
        try:
            dialog.geometry("340x120")
        except Exception:
            pass

        ttk.Label(dialog, text=self._t("dlg_hotkey_msg"), justify="center", wraplength=300).pack(pady=(18, 10))

        result = {"key": None, "done": False}

        def on_key(event: tk.Event) -> None:
            if result["done"]:
                return
            keysym = event.keysym
            # Escape = cancel
            if keysym == "Escape":
                result["done"] = True
                dialog.destroy()
                return
            # Reject modifier-only keys
            if keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R",
                          "Alt_L", "Alt_R", "Super_L", "Super_R", "Meta_L", "Meta_R"):
                return
            result["key"] = keysym
            result["done"] = True
            dialog.destroy()

        dialog.bind("<KeyPress>", on_key)
        dialog.focus_set()
        self.wait_window(dialog)

        if result["key"]:
            self._stop_hotkey_listener()
            self.hotkey = result["key"]
            self.hotkey_label.config(text=self.hotkey)
            self._start_hotkey_listener()
            self.log(self._t("log_hotkey_set", key=self.hotkey))
            try:
                self._save_config()
            except Exception:
                pass

    def _process_frame_and_click(
        self,
        frame_bgr: np.ndarray,
        offset_x: int,
        offset_y: int,
        threshold: float,
        move_min: float,
        move_max: float,
    ) -> None:
        # Convert once to grayscale
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        now = time.time()
        global_threshold = threshold

        for item in self.templates:
            # Skip disabled or missing templates
            if not item.enabled or item.image is None:
                continue

            # Respect per-template max clicks per run
            if item.max_clicks_per_run is not None and item.clicks_this_run >= item.max_clicks_per_run:
                continue

            tpl_threshold = item.custom_threshold if item.custom_threshold is not None else global_threshold
            cooldown = item.click_cooldown if item.click_cooldown is not None else 3.0

            last_region = item.last_region

            # First search: exclude last clicked region, if any
            exclude_region = last_region if last_region is not None else None
            found, region, score = self._find_template(gray, item.image, tpl_threshold, exclude_region)

            # If nothing else was found, consider last_region again (after cooldown)
            if not found and last_region is not None:
                if (now - item.last_click_time) >= cooldown:
                    found, region, score = self._find_template(gray, item.image, tpl_threshold, None)
                else:
                    continue

            if not found:
                continue

            x, y, w, h = region
            abs_x = offset_x + x
            abs_y = offset_y + y

            tx, ty = self._random_point_in_region(abs_x, abs_y, w, h)
            self.log(self._t("log_tpl_matched", x=abs_x, y=abs_y, w=w, h=h, score=f"{score:.3f}", tx=tx, ty=ty))
            self._human_like_move_and_click(tx, ty, move_min, move_max)

            # Record where and when we clicked, in frame coordinates
            item.last_region = (x, y, w, h)
            item.last_click_time = now
            item.clicks_this_run += 1
            with self._clicks_lock:
                self.total_clicks_this_run += 1

            # Schedule a status refresh so the UI shows updated click counts
            try:
                self.after(0, self._update_status, self._t("status_running"))
            except Exception:
                pass

            # If this template has a per-template stop-after-clicks limit,
            # and we have reached or exceeded it, stop the entire run.
            if item.stop_after_clicks is not None and item.clicks_this_run >= item.stop_after_clicks:
                self.log(self._t("log_stop_after_reached", name=os.path.basename(item.path), limit=item.stop_after_clicks))
                self.running_event.clear()
                break

            # After a successful click, wait a bit longer to avoid spam clicking
            extra_sleep = random.uniform(0.8, 1.8)
            time.sleep(extra_sleep)

    @staticmethod
    def _find_template(
        frame_gray: np.ndarray,
        template_gray: np.ndarray,
        threshold: float,
        exclude_region: Optional[Tuple[int, int, int, int]] = None,
    ) -> Tuple[bool, Tuple[int, int, int, int], float]:
        res = cv2.matchTemplate(frame_gray, template_gray, cv2.TM_CCOEFF_NORMED)

        # Optionally mask out a region (recently clicked area) so we can
        # prefer new occurrences of the same template elsewhere on the screen.
        if exclude_region is not None:
            x, y, w, h = exclude_region
            h_res, w_res = res.shape[:2]
            x0 = max(0, x)
            y0 = max(0, y)
            x1 = min(w_res, x + w)
            y1 = min(h_res, y + h)
            if x0 < x1 and y0 < y1:
                # For TM_CCOEFF_NORMED, lower is worse, so -1.0 effectively disables this area.
                res[y0:y1, x0:x1] = -1.0

        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val < threshold:
            return False, (0, 0, 0, 0), max_val

        h, w = template_gray.shape[:2]
        x, y = max_loc
        return True, (x, y, w, h), max_val

    @staticmethod
    def _random_point_in_region(x: int, y: int, w: int, h: int) -> Tuple[int, int]:
        # Center point
        cx = x + w // 2
        cy = y + h // 2

        # Bias toward center: only allow offsets in a smaller inner box
        max_offset_x = max(1, w // 4)
        max_offset_y = max(1, h // 4)

        rx = random.randint(-max_offset_x, max_offset_x)
        ry = random.randint(-max_offset_y, max_offset_y)

        return cx + rx, cy + ry

    def _compute_status_text(self, state: str) -> str:
        total = len(self.templates)
        enabled = sum(1 for t in self.templates if t.enabled and t.image is not None)
        preset = None
        if isinstance(self.config, dict):
            p = self.config.get("last_preset")
            if isinstance(p, str):
                preset = p
        if not preset:
            preset = "-"

        # Surface progress for every template that has a stop-after-clicks limit.
        stop_info = ""
        stop_templates = [t for t in self.templates if t.stop_after_clicks is not None]
        if stop_templates:
            parts = []
            for t0 in stop_templates:
                name = os.path.basename(t0.path)
                parts.append(f"{name}: {t0.clicks_this_run}/{t0.stop_after_clicks or 0}")
            stop_info = " | " + self._t("status_stop_label") + " " + ", ".join(parts)

        sp = self._t("status_prefix")
        pp = self._t("status_preset")
        tp = self._t("status_templates")
        cp = self._t("status_clicks")
        with self._clicks_lock:
            clicks = self.total_clicks_this_run
        return f"{sp}: {state}{stop_info} | {pp}: {preset} | {tp}: {enabled}/{total} | {cp}: {clicks}"

    def _update_status(self, state: str) -> None:
        self.status_var.set(self._compute_status_text(state))

    def on_toggle_advanced_settings(self) -> None:
        """Show or hide the advanced settings section to reduce UI clutter."""
        visible = self.advanced_visible
        if not visible:
            self.advanced_frame.pack(fill=tk.X, expand=False, side=tk.TOP, padx=5, pady=5)
            self.advanced_visible = True
            self.advanced_toggle_button.config(text=self._t("btn_hide_extra"))
        else:
            self.advanced_frame.pack_forget()
            self.advanced_visible = False
            self.advanced_toggle_button.config(text=self._t("btn_show_extra"))

    def on_toggle_pause(self) -> None:
        if not self.running_event.is_set():
            return
        # Toggle paused flag
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text=self._t("btn_resume"))
            self._update_status(self._t("status_paused"))
            self.log(self._t("log_paused"))
        else:
            self.pause_button.config(text=self._t("btn_pause"))
            self._update_status(self._t("status_running"))
            self.log(self._t("log_resumed"))

    @staticmethod
    def _human_like_move_and_click(
        target_x: int,
        target_y: int,
        move_min: float,
        move_max: float,
    ) -> None:
        duration = random.uniform(move_min, move_max)

        # Slight overshoot for more human-like movement
        overshoot_px = random.randint(3, 12)
        overshoot_sign_x = random.choice([-1, 1])
        overshoot_sign_y = random.choice([-1, 1])

        mid_x = target_x + overshoot_sign_x * overshoot_px
        mid_y = target_y + overshoot_sign_y * overshoot_px

        # Two-stage move: to mid point then to final
        pyautogui.moveTo(
            mid_x,
            mid_y,
            duration=duration * random.uniform(0.4, 0.7),
            tween=pyautogui.easeInOutQuad,
        )
        pyautogui.moveTo(
            target_x,
            target_y,
            duration=duration * random.uniform(0.3, 0.6),
            tween=pyautogui.easeOutQuad,
        )

        # Small random delay before click
        time.sleep(random.uniform(0.05, 0.15))
        pyautogui.click()


def main() -> None:
    app = TemplateClickerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
