import json
import re
from pprint import pprint

from app.services.ai.bedrock import BedrockService
from app.services.calendar.google_calendar import GoogleCalendarService
from app.services.weather.open_meteo import OpenMeteoService


def main():
    training_config = {
        "activities": [
            {
                "type": "run",
                "title": "Short run",
                "distance_km": 8,
                "duration_h": 1
            },
            {
                "type": "bike",
                "title": "Longer bike ride with Michal",
                "distance_km": 65,
                "duration_h": 2.25
            },
            {
                "type": "swim",
                "title": "Chill swim at X",
                "distance_km": 1
            }
        ],
        "days": ["monday", "tuesday", "friday"],
        "day_start": "08:00",
        "day_end": "18:00",
        "allow_multiple_trainings_per_day": True,
        "min_time_gap_between_events_in_minutes": 30
    }
    plan_proposal_format = {
        "title": "${activity emoji} ${training title} - ${distance}",
        "description": "your reasoning why you believe this is the best possible time for that particular session",
        "start": "iso timestamp when to start",
        "end": "iso timestamp when to end",
    }

    gc = GoogleCalendarService()
    events = gc.list_events()

    smolenice_coordinates = [48.506211053607856, 17.43061034187817]
    om = OpenMeteoService()
    weather_data = om.get_weather_data(*smolenice_coordinates)
    
    ai = BedrockService()
    plan_proposal = ai.invoke_model(''.join([
        'You are a planning tool and you want to create a training plan from tomorrow onwards',
        'You want to base your plan on three data points: calendar (to avoid any event clashes), best weather conditions possible and desired training config.',
        f"Calendar: ```{events}```.",
        f"Weather conditions: ```{weather_data}```.",
        f"Training config: ```{training_config}```.",
        f"Return your plan proposal as an array of events, each even in this format ```{plan_proposal_format}``` and wrap your response in ```"
    ]))
    
    training_sessions_string = re.split(r'```', plan_proposal)
    training_sessions = json.loads(training_sessions_string[1])
    print('\nPlanned Sessions:\n')
    pprint(training_sessions)

    for session in training_sessions:
        gc.create_event({
            'title': session.get('title'),
            'description': session.get('description'),
            'start': session.get('start'),
            'end': session.get('end'),
        })


if __name__ == "__main__":
    main()