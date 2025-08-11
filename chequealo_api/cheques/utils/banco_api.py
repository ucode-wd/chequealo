import requests
import certifi
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def consultar_cheque_denunciado(codigo_entidad, numero_cheque):
    url = f"https://api.bcra.gob.ar/cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}"
    try:
        response = requests.get(url, timeout=10, verify=certifi.where())
        return response.json() if response.status_code == 200 else {
            "error": f"Error del BCRA (denunciado): {response.status_code}"
        }
    except requests.exceptions.SSLError:
        try:
            response = requests.get(url, timeout=10, verify=False)
            return response.json() if response.status_code == 200 else {
                "error": f"Error del BCRA (fallback): {response.status_code}"
            }
        except Exception as e:
            return {"error": f"Fallo total al conectar (denunciado): {str(e)}"}
    except Exception as e:
        return {"error": f"Error inesperado (denunciado): {str(e)}"}


def consultar_cheques_rechazados(identificacion):
    url = f"https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/ChequesRechazados/{identificacion}"
    try:
        response = requests.get(url, timeout=10, verify=certifi.where())
        return response.json() if response.status_code == 200 else {
            "error": f"Error del BCRA (rechazados): {response.status_code}"
        }
    except requests.exceptions.SSLError:
        try:
            response = requests.get(url, timeout=10, verify=False)
            return response.json() if response.status_code == 200 else {
                "error": f"Error del BCRA (fallback): {response.status_code}"
            }
        except Exception as e:
            return {"error": f"Fallo total al conectar (rechazados): {str(e)}"}
    except Exception as e:
        return {"error": f"Error inesperado (rechazados): {str(e)}"}
    
    
def consultar_deudas(identificacion):
    url = f"https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/{identificacion}"
    try:
        response = requests.get(url, timeout=10, verify=certifi.where())
        return response.json() if response.status_code == 200 else {
            "error": f"Error del BCRA (rechazados): {response.status_code}"
        }
    except requests.exceptions.SSLError:
        try:
            response = requests.get(url, timeout=10, verify=False)
            return response.json() if response.status_code == 200 else {
                "error": f"Error del BCRA (fallback): {response.status_code}"
            }
        except Exception as e:
            return {"error": f"Fallo total al conectar (rechazados): {str(e)}"}
    except Exception as e:
        return {"error": f"Error inesperado (rechazados): {str(e)}"}