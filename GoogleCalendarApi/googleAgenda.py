import datetime
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

            id = self.retornar_psicologo(psicologo_logado)
            
            created_event = self.service.events().insert(calendarId=id, body=event).execute()
            print('Event created:', created_event.get('htmlLink'))
            return 200
            
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