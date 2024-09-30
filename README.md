# Training Planner

## About

This tool is meant to automate the repeating and tedious process of training session planning. During the planning, we want to focus on what is really important, collect data from previous sessions and create targets for upcoming period (Qs). What you always need to take into consideration each week is your personal/work calendar and align your free/available time with the weather forecast. It is indeed based on the assumption that you love spending time outside as much as I do, since the weather factor becomes redundant during indoor training. This tool could still be used, nevertheless, with either ignoring the weather input or with a combination of indoor and outdoor trainings.

## Setup

First we need to create a virtual env in the cloned folder with the following command

```bash
py -m venv venv/
```

Once done, we can activate it

```bash
source venv/bin/activate
```

Now we follow up with installing requirements

```bash
pip install -r requirements.txt
```

Now we need to connect our Google Calendar. In order to do that, we need to go to the Google API console, create OAuth Client ID secret of type `desktop app`, download the generated file, drop it in the root folder and rename it to `credentials.json`. On the first run, we will be prompted with authentication via triggered browser window. This action will cache the auth via `token.json` file in the root folder. To reset the auth, simply delete this file.

## Run

```bash
py main.py
```

## Test

TODO
those will follow up as soon as we have a PoC, together with linter

## Maintenance

Don't forget to update deps each time you make any changes. You can achieve that with the following

```bash
pip freeze > requirements.txt
```

To gracefully exit the virtual env make sure to deactivate it

```bash
deactivate
```

## Next Steps

### phase #1

- parse weather data ✅
- add AI assistant to evaluate upcoming week against my calendar and weather and create suggestions according to my target training ✅

### phase #2

- add firebase created events tracking, successful suggestions ratio (for later model training)
- make it all dynamic, based on input values from env/cli (location, training schedule)

### phase #3

- run in the could and have your schedule for the upcoming week (from now) reevaluated each day (according to weather change, canceled/deleted/added events)

### phase #4

- incorporate hourly weather conditions (bedrock knowledge base?)
