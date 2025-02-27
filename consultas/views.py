from django.shortcuts import render, HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import consult
from .querys import consultAsociado

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def consulta_asociado(request, cedula=None):
  """ Vista API para la consulta de asociado por el numero de cedula """
  try:
    cedula = int(cedula)
  except (ValueError, TypeError):
    return Response({'success': False, 'message': 'Debe ingresar un valor numerico'}, status=400)
    
  if cedula is None:
    return Response({'success': False, 'message': 'Cédula no proporcionada'}, status=400)
  
  queryAsociado = consultAsociado(cedula)
  print(queryAsociado)
  # return
  data = consult(queryAsociado)
  print(data)
  if data:
    # setData = {
    #   'nombre': f"{data[0]['P_NOMBRE']} {data[0]['S_NOMBRE']} {data[0]['P_APELLIDO']} {data[0]['S_APELLIDO']}",
    #   'dirección': data[0]['DIRECCION_CORRES'],
    #   'correo': data[0]['EMAIL_CORRES'],
    #   'telefono_fijo': data[0]['CELULAR_CORRES'],
    #   'telefono_celular': data[0]['CELULAR_CORRES'],
    #   'asociado': True
    # }
    return Response({'success': True, 'data': data}, status=200)
  return Response({'success': False, 'message': 'No se encontro informacion del asociado'}, status=404)
