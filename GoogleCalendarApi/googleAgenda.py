from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from models.agendamentoModel import Agendamento
from fastapi import HTTPException,status
from Controllers.Controller_user import ControllerUser

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly"
]


class GoogleCalendar:
    
    def __init__(self):
        self.creds = None
        self.SCOPES = SCOPES
        self.token_path = "././token.json"
        self.credentials_path = "././credentials.json"

    def auth_api(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)


    def insert_event(self, evento: Agendamento, psicologo_logado: dict):
        nome = evento.nome
        descricao = evento.descricao
        data = evento.data
        hora_inicio = evento.hora_inicio + ":00"
        hora_fim = evento.hora_fim + ":00"
        email_cliente = evento.email_cliente
        data  = self.formatar_data(data)
        print(data)

        try:
            self.auth_api()
            event = {
                'summary': nome,
                'description': descricao,
                'start': {
                    'dateTime': f"{data}T{hora_inicio}",
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': f"{data}T{hora_fim}",
                    'timeZone': 'America/Sao_Paulo',
                },
                'attendees': [
                    {'email': email_cliente},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            print("chegou aqui")
            print("olha o evento:", event)

            id_calendar = self.retornar_psicologo(psicologo_logado)
            
            created_event = self.service.events().insert(calendarId=id_calendar, body=event).execute()
            print('Event created:', created_event.get('htmlLink'))
            return status.HTTP_200_OK
            
            """if ControllerCliente.getClienteAgendamento(email_convidado):
                
                copia_agendamento = event.copy()
                copia_agendamento["preco"] = evento.preco
                copia_agendamento["id"] = created_event['id']
                controller_agendamento = Controller_Copia_Agendamento()
                controller_agendamento.inserir_agendamento(copia_agendamento)
                
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cliente não encontrado nos registros do sistema")"""

        except HttpError as error:
            raise HTTPException(status_code=error.resp.status, detail=f"An error occurred: {error}")
        except Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"erro ao criar evento: {str(erro)}")

    def formatar_data(self, data: str):
        try:
            data_atual = data.split("-")
            print(data_atual)
            dia = data_atual[0]
            mes = data_atual[1]
            ano = data_atual[2]
            data_format_final = f"{ano}-{mes}-{dia}"
            
            return data_format_final
    
        except Exception as e:
          print(f"Erro ao formatar a data: {e}")
          raise e
        
    def retornar_psicologo(self,psicologo_logado: dict):
        psi = ControllerUser.getSingleUser(psicologo_logado["email"])
        return psi["google_calendar_id"]
    
          
    def listar_calendarios(self):
      try:
          self.auth_api()
          # List all calendars
          calendar_list = self.service.calendarList().list().execute()
          for calendar in calendar_list['items']:
              print(f"Calendar Summary: {calendar['summary']}, Calendar ID: {calendar['id']}")
      except HttpError as error:
          print(f"An error occurred: {error}")


    def listar_eventos(self, psicologo_logado: str):
        try:
            self.auth_api()

            calendar_id = self.retornar_psicologo(psicologo_logado)

            # Listando eventos do calendário
            eventos = self.service.events().list(calendarId=calendar_id).execute()
            eventos_lista = eventos.get('items', [])

            if not eventos_lista:
                print("Nenhum evento encontrado.")
                return []

            eventos_principais = []  # Lista para armazenar os dados principais

            for evento in eventos_lista:
                id = evento.get('id', 'Sem título')  # ID do evento
                nome = evento.get('summary', 'Sem título')  # Nome do evento
                descricao = evento.get('description', 'Sem descrição')  # Descrição
                inicio = evento['start'].get('dateTime', evento['start'].get('date'))  # Data/hora de início
                fim = evento['end'].get('dateTime', evento['end'].get('date'))  # Data/hora de fim
                email_cliente = evento['attendees'][0]['email'] if 'attendees' in evento and evento['attendees'] else 'Sem e-mail'  # Email do cliente

                # Converter o início e fim para o formato brasileiro
                inicio_br = self.formatar_data_hora(inicio)
                fim_br = self.formatar_data_hora(fim)

                # Armazenando os dados principais em um dicionário
                evento_principal = {
                    'id':id,
                    'nome': nome,
                    'descricao': descricao,
                    'inicio': inicio_br,
                    'fim': fim_br,
                    'email_cliente': email_cliente
                }

                eventos_principais.append(evento_principal)

            # Retornar apenas os dados principais
            return eventos_principais

        except HttpError as error:
            raise HTTPException(status_code=error.resp.status, detail=f"Ocorreu um erro ao listar eventos: {error}")
        except Exception as erro:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno: {str(erro)}")
        

    def formatar_data_hora(self, data_hora: str):
        try:
            # Converter string ISO 8601 para objeto datetime
            data_hora_obj = datetime.fromisoformat(data_hora)
            # Formatar para o padrão brasileiro (DD/MM/YYYY HH:MM)
            data_hora_br = data_hora_obj.strftime("%d/%m/%Y %H:%M")
            return data_hora_br
        except Exception as e:
            print(f"Erro ao formatar data e hora: {e}")
            return data_hora  # Retorna a string original em caso de erro

    def updateAgendamento(self, eventId: str, evento_atualizado: Agendamento, psicologo_logado:dict):
      try:
          self.auth_api()

          calendar_id = self.retornar_psicologo(psicologo_logado)

          event = self.service.events().get(calendarId= calendar_id, eventId=eventId).execute()
          event['summary'] = evento_atualizado.nome
          event['description'] = evento_atualizado.descricao

          data_formatada = datetime.strptime(evento_atualizado.data, '%d-%m-%Y').strftime('%Y-%m-%d')
          event['start']['dateTime'] = f"{data_formatada}T{evento_atualizado.hora_inicio}:00"
          event['end']['dateTime'] = f"{data_formatada}T{evento_atualizado.hora_fim}:00"
          event['attendees'][0]['email'] = evento_atualizado.email_cliente

          self.service.events().update(calendarId= calendar_id, eventId=eventId, body=event).execute()
          return status.HTTP_200_OK
          
      except HttpError as error:
          raise HTTPException(status_code=error.resp.status, detail=f"Ocorreu um erro ao atualizar o agendamento: {error}")
    

    def deletarAgendamento(self, event_ID, psicologo_logado:dict):
        try:
            self.auth_api()

            calendar_id = self.retornar_psicologo(psicologo_logado)

            self.service.events().delete(calendarId= calendar_id, eventId=event_ID).execute()
            return status.HTTP_200_OK
          
        except HttpError as error:
          raise HTTPException(status_code=error.resp.status, detail=f"Ocorreu um erro ao deletar o agendamento: {error}")
    


"""def main():
  Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()"""