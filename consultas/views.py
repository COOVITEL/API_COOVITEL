from django.shortcuts import render, HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .services import consult
from .querys import *
from .decorators import restrict_ip
import datetime
from .models import PagaduriasLinix
from rest_framework.views import APIView
from .serializer import PagaduriasSerializer
from rest_framework import status

# @restrict_ip
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

  data = consult(queryAsociado)
  if data:
    data[0]['ASOCIADO'] = "Si" if data[0]['ASOCIADO'] == "A" else "No"
    return Response({'success': True, 'data': data}, status=200)
  return Response({'success': False, 'message': 'No se encontro informacion del asociado'}, status=404)


class PagaduriasLinixApiView(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    data =  {
      'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      'numeroDePagadurias': PagaduriasLinix.objects.count(),
      'data': PagaduriasSerializer(PagaduriasLinix.objects.all(), many=True).data
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crear_pagadurias(request):
  query1 = consultPagaduria()
  numero_pagaduria = consult(query1)
  query2 = infoPagaduria()
  info_pagaduria = consult(query2)
  for num_pagaduria in numero_pagaduria:
    for info in info_pagaduria:
      if num_pagaduria['K_NOMINA'] == info['K_NOMINA']:
        pagaduria_exist = PagaduriasLinix.objects.filter(k_nomina=info['K_NOMINA']).first()
        pagaduria = {
          "n_nomina": info['N_NOMINA'],
          "nit": info['A_NUMNIT'] if info['A_NUMNIT'] else '',
          "n_razon": info['N_RAZONS'] if info['N_RAZONS'] else '',
          "f_creacion": info['F_CREACION'] if info['F_CREACION'] else '',
          "sigla": info['SIGLA'] if info['SIGLA'] else '',
          "k_tipoem": info['K_TIPOEM'] if info['K_TIPOEM'] else '',
          "pais": info['K_PAIS_IDE'] if info['K_PAIS_IDE'] else '',
          "departamento": info['K_DEPART_IDE'] if info['K_DEPART_IDE'] else '',
          "ciudad": info['K_CIUDAD_IDE'] if info['K_CIUDAD_IDE'] else '',
          "num_representante": info['O_NUMNIT_REP'] if info['O_NUMNIT_REP'] else '',
          "representante": info['N_REPLEG'] if info['N_REPLEG'] else '',
          "k_nomina": info['K_NOMINA'],
          "num_asociados": num_pagaduria['NUM_ASOCIADOS'] if num_pagaduria['NUM_ASOCIADOS'] else '',
          "num_cdat": num_pagaduria['NUM_CDAT'] if num_pagaduria['NUM_CDAT'] else '',
          "num_cooviahorros": num_pagaduria['NUM_COOVIAHORO'] if num_pagaduria['NUM_COOVIAHORO'] else '',
          "num_creditos": num_pagaduria['NUM_CREDITOS'] if num_pagaduria['NUM_CREDITOS'] else '',
          "num_ahorroVista": num_pagaduria['NUM_HVISTA'] if num_pagaduria['NUM_HVISTA'] else ''
        }
        if pagaduria_exist:
          cambios = False
          for campo, valor in pagaduria.items():
              if getattr(pagaduria_exist, campo) != valor:
                  setattr(pagaduria_exist, campo, valor)
                  cambios = True
          
          if cambios:
              print("Guardando cambios")
              pagaduria_exist.save()
          else:
              print("No hay cambios")
        else:
          print("Creando pagaduria")
          PagaduriasLinix.objects.create(**pagaduria)
  return Response({'success': True, 'message': 'Pagadurias creadas correctamente'}, status=200)