import cx_Oracle
from dotenv import load_dotenv
import os

load_dotenv()

def consult(query: str):
  """"""
  dsn_tns = cx_Oracle.makedsn(os.getenv('IP'), os.getenv('PORT'), os.getenv('NAMEDB'))

  try:
      with cx_Oracle.connect(
          user=os.getenv('USERDB'),
          password=os.getenv('PASSWORDDB'),
          dsn=dsn_tns
      ) as conn:
          with conn.cursor() as cursor:
              cursor.execute(query)
              data = cursor.fetchall()
              if not data:
                  return None  # Si no hay datos, devolvemos None
              columns = [desc[0] for desc in cursor.description]
              users = [dict(zip(columns, row)) for row in data]
              return users
  except cx_Oracle.DatabaseError as e:
      error, = e.args
      print(f'Error en la base de datos: {error.message}')
      return None
  except Exception as e:
      print(f'Error inesperado: {e}')
      return None
