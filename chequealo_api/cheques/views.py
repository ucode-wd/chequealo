from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .utils.ocr import extraer_datos_cheque
from .utils.banco_api import (
    consultar_cheque_denunciado,
    consultar_cheques_rechazados,
    consultar_deudas
)
from .models import ChequeProcesado
from .serializers import ChequeProcesadoSerializer


class ProcesarChequeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        imagen = request.FILES.get('imagen')
        if not imagen:
            return Response({'error': 'No se proporcionó una imagen'}, status=400)

        try:
            # Procesar OCR
            ocr = extraer_datos_cheque(imagen)

            numero_entidad_raw = ocr.get('numero_entidad', [])
            numero_cheque_raw = ocr.get('numero_cheque', [])
            cuit_raw = ocr.get('cuit', [])

            if not numero_entidad_raw or not numero_cheque_raw or not cuit_raw:
                return Response({
                    'error': 'Faltan datos esenciales: CUIT, número de cheque o código de entidad.',
                    'ocr': ocr
                }, status=400)

            # Ya vienen filtrados, tomo el primero
            codigo_entidad = numero_entidad_raw[0]
            numero_cheque = numero_cheque_raw[0]
            cuit = cuit_raw[0]

            # Consultas al BCRA
            datos_denunciado = consultar_cheque_denunciado(codigo_entidad, numero_cheque)
            datos_rechazado = consultar_cheques_rechazados(cuit)
            datos_deudas = consultar_deudas(cuit)

            # Guardar en base de datos
            cheque = ChequeProcesado.objects.create(
                imagen=imagen,
                numero_cheque=numero_cheque,
                codigo_entidad=codigo_entidad,
                cuit=cuit,
                datos_denunciado=datos_denunciado,
                datos_rechazado=datos_rechazado,
                datos_deudas=datos_deudas,
            )

            serializer = ChequeProcesadoSerializer(cheque)
            return Response(serializer.data)

        except Exception as e:
            return Response({'error': str(e)}, status=500)