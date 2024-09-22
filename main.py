from app.services.google_calendar import GoogleCalendarService


def main():
    gc = GoogleCalendarService()

    # gc.create_event({
    #     'title': 'Test event',
    #     'description': 'This is a test event',
    #     'start': '2024-10-01T10:00:00',
    #     'end': '2024-10-01T11:00:00',
    # })
    gc.list_events()


if __name__ == "__main__":
    main()