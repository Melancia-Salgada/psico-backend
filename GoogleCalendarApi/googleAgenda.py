from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from models.agendamentoModel import Agendamento
from fastapi import HTTPException,status
from Controllers.Controller_user import ControllerUser
from Controllers.controller_paciente import ControllerPaciente
from services.Email import ControllerEmail

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly",
    'https://www.googleapis.com/auth/meetings.space.created'
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

            client = meet_v2.SpacesServiceClient(credentials=self.creds)
            request = meet_v2.CreateSpaceRequest()
            response = client.create_space(request=request)
            link_meet = response.meeting_uri
            descricao = descricao+ " |  "+link_meet

            evento.link_meet = link_meet

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
                'recurrence': [
                    'RRULE:FREQ=WEEKLY;UNTIL=20241115T170000Z',
                ],
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
                'extendedProperties': { # o link da meet deve ser acessado pelo botão aqui
                    'shared': {
                        'link_meet': link_meet
                    }   
                }
            }
            print("chegou aqui")
            print("olha o evento:", event)
            
            controller_user = ControllerUser()
            id_calendar = controller_user.retornar_psicologo(psicologo_logado)
            
            created_event = self.service.events().insert(calendarId=id_calendar, body=event).execute()
            print('Event created:', created_event.get('htmlLink'))

            return status.HTTP_200_OK
            
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
    

    async def enviarLembreteConfirmacao(self,evento:Agendamento):
        emailPaciente = evento.email_cliente
        link_meet = evento.link_meet
        print(f"extraindo link da meet: {link_meet}, email do cliente: {emailPaciente}")
        controller = ControllerEmail()
        await controller.emailLembreteConsulta(emailPaciente,link_meet)
        

    
          
    def listar_calendarios(self):
      try:
          self.auth_api()
          # List all calendars
          calendar_list = self.service.calendarList().list().execute()
          for calendar in calendar_list['items']:
              print(f"Calendar Summary: {calendar['summary']}, Calendar ID: {calendar['id']}")
      except HttpError as error:
          print(f"An error occurred: {error}")


    def listar_eventos(self, psicologo: dict):
        try:
            self.auth_api()
            psicologo_logado = psicologo["email"]
            print(psicologo_logado)
            controller_user = ControllerUser()
            id_calendar = controller_user.retornar_psicologo(psicologo_logado)
            
            # Listando eventos do calendário
            eventos = self.service.events().list(calendarId=id_calendar).execute()
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
                 # Extraindo o link do meet, se existir
                link_meet = evento.get('extendedProperties', {}).get('shared', {}).get('link_meet', 'sem link')

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
                    'email_cliente': email_cliente,
                    'link meet':link_meet
                }

                eventos_principais.append(evento_principal)

            # Backend - Alteração do formato de resposta
            return {"Consultas": eventos_principais}


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

          controller_user = ControllerUser()
          id_calendar = controller_user.retornar_psicologo(psicologo_logado)

          event = self.service.events().get(calendarId= id_calendar, eventId=eventId).execute()
          event['summary'] = evento_atualizado.nome
          event['description'] = evento_atualizado.descricao

          data_formatada = datetime.strptime(evento_atualizado.data, '%d-%m-%Y').strftime('%Y-%m-%d')
          event['start']['dateTime'] = f"{data_formatada}T{evento_atualizado.hora_inicio}:00"
          event['end']['dateTime'] = f"{data_formatada}T{evento_atualizado.hora_fim}:00"
          event['attendees'][0]['email'] = evento_atualizado.email_cliente

          self.service.events().update(calendarId= id_calendar, eventId=eventId, body=event).execute()
          return status.HTTP_200_OK
          
      except HttpError as error:
          raise HTTPException(status_code=error.resp.status, detail=f"Ocorreu um erro ao atualizar o agendamento: {error}")
    

    def deletarAgendamento(self, event_ID, psicologo_logado:dict):
        try:
            self.auth_api()

            controller_user = ControllerUser()
            id_calendar = controller_user.retornar_psicologo(psicologo_logado)

            self.service.events().delete(calendarId= id_calendar, eventId=event_ID).execute()
            return status.HTTP_200_OK
          
        except HttpError as error:
          raise HTTPException(status_code=error.resp.status, detail=f"Ocorreu um erro ao deletar o agendamento: {error}")
    


