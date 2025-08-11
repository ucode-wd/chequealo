import cv2
import easyocr
import re
import numpy as np

# Inicializamos el lector OCR
reader = easyocr.Reader(["es"], gpu=False)

# ---------- Normalización ----------
def normalizar_texto(texto_ocr):
    texto = " ".join(texto_ocr)
    reemplazos = {
        'o': '0', 'O': '0', 'd': '0',
        'l': '1', 'I': '1',
        's': '5', 'S': '5',
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    return texto

# ---------- Validación CUIT ----------
def validar_cuit(cuit):
    if len(cuit) != 11 or not cuit.isdigit():
        return False
    mult = [5,4,3,2,7,6,5,4,3,2]
    suma = sum(int(cuit[i]) * mult[i] for i in range(10))
    resto = 11 - (suma % 11)
    if resto == 11:
        resto = 0
    elif resto == 10:
        resto = 9
    return int(cuit[-1]) == resto

# ---------- Filtros ----------
def filtrar_cuit(texto):
    candidatos = re.findall(r'\b\d{11}\b', texto)
    return list({c for c in candidatos if validar_cuit(c)})

def filtrar_num_cheque(texto):
    return list(set(re.findall(r'\b\d{8}\b', texto)))

def filtrar_codigo_entidad(texto):
    completos = re.findall(r'\b\d{3}-\d{3}-\d{4}\b', texto)
    primeros_3 = [c.split('-')[0] for c in completos]
    return list(set(primeros_3))

# ---------- Función principal ----------
def extraer_datos_cheque(file):
    # Asegurarnos de leer desde el inicio del archivo
    file.seek(0)
    file_bytes = file.read()

    if not file_bytes:
        raise ValueError("La imagen recibida está vacía.")

    # Convertir a array y decodificar
    np_arr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("No se pudo decodificar la imagen con OpenCV.")

    # Redimensionar si es muy grande (mejora velocidad OCR)
    ancho_max = 1500
    if img.shape[1] > ancho_max:
        escala = ancho_max / img.shape[1]
        alto_nuevo = int(img.shape[0] * escala)
        img = cv2.resize(img, (ancho_max, alto_nuevo))

    # OCR
    texto_ocr = reader.readtext(img, detail=0)
    texto_normalizado = normalizar_texto(texto_ocr)

    # Filtrar datos
    cuit_detectado = filtrar_cuit(texto_normalizado)
    cheques_detectados = filtrar_num_cheque(texto_normalizado)
    entidades_detectadas = filtrar_codigo_entidad(texto_normalizado)

    return {
        "numero_entidad": entidades_detectadas,
        "numero_cheque": cheques_detectados,
        "cuit": cuit_detectado,
        "texto_ocr": texto_ocr  # Lo dejamos para depuración
    }
