import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarService():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self) -> None:
        self.service = build("calendar", "v3", credentials=self.__auth())

    def list_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        one_week_from_now = (datetime.date.today() + datetime.timedelta(days=7)).isoformat() + 'T00:00:00Z'
        
        try:
            events_result = (
                self.service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    timeMax=one_week_from_now,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])
            events = map(lambda x: mm(x), events)
            def mm(x):
                e = {
                    'id': x.get('id'),
                    # 'status': x.get('status'),
                    # 'created': x.get('created'),
                    'summary': x.get('summary'),
                    'start': x.get('start').get('date', x.get('start').get('dateTime')),
                    'end': x.get('end').get('date', x.get('end').get('dateTime')),
                }
                return e

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in events:
                print(event)
                # start = event["start"].get("dateTime", event["start"].get("date"))
                # print(start, event["summary"])

        except Exception as e:
            print(f"An error occurred while listing events", e)


    def create_event(self, event_input: dict[str, any]) -> object:
        # eventType:
        #   "birthday" - A special all-day event with an annual recurrence.
        #   "default" - A regular event or not further specified.
        #   "focusTime" - A focus-time event. Requires enterprise account.
        #   "fromGmail" - An event from Gmail. This type of event cannot be created.
        #   "outOfOffice" - An out-of-office event. Doesn't allow setting description
        #   "workingLocation
        event = {
            'summary': event_input.get('title'),
            'description': event_input.get('description'),
            'start': {
                'dateTime': event_input.get('start'),
                'timeZone': 'Europe/Berlin',
            },
            'end': {
                'dateTime': event_input.get('end'),
                'timeZone': 'Europe/Berlin',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'eventType': 'default'
        }

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f"Event<{event['id']}> created", event)
        except Exception as e:
            print("An error occurred while creating an Event", event, e)

        return event
    

    def update_event(self, event_id: str, event_input: dict[str, any]) -> None:
        try:
            # First retrieve the event from the API.
            event = self.service.events().get(calendarId='primary', eventId=event_id).execute()

            event['summary'] = event_input.get('title')

            updated_event = self.service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
            print(f"Event<{event_id}> updated", updated_event)
            return updated_event
        except Exception as e:
            print(f"An error occurred while updating Event<{event_id}>", event, e)
    

    def delete_event(self, event_id: str) -> None:
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            print(f"Event<{event_id}> deleted")
        except Exception as e:
            print(f"An error occurred while deleting Event<{event_id}>", e)


    def __auth(self) -> object:
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            credentials = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.SCOPES
                )
                credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(credentials.to_json())

        return credentials
            

if __name__ == '__main__':
    gc = GoogleCalendarService()

    # list events
    events = gc.list_events()
    print('Events listed: ', events)

    # crete an event
    event = gc.create_event({
        'title': 'Test event',
        'description': 'This is a test event',
        'start': '2024-10-01T10:00:00',
        'end': '2024-10-01T11:00:00',
    })
    print('Event created: %s', event.get('htmlLink'))

