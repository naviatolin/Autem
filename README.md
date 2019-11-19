# Autem - Productivity WebApp #

## Description  ##
This application is essentially a personalized planner. You input your regular events in the calendar (classes, weekly meetings, work, etc.) as events, then tell the app what you need to do (tasks), and how long you think it'll take. The app will then schedule times for the user to work on their task. Every few hours, the app will prompt you to rate your mood. If you rate that you're not feeling great, it'll suggest some self-care activities, and schedule some time for it. The app will prioritize self-care activities it knows you like.

## Authors ##
Maya Al-Ahmad and Navi Boyalakuntla

## Getting Started ##
Install all of the requirements using the following command.

```sudo pip install -r requirements.txt```

In addition to running this, install MongoDB using the instructions detailed at https://docs.mongodb.com/manual/installation/#mongodb-community-edition-installation-tutorials.

## Usage ## 
In order to view the webapp:
```
export FLASK_APP=application.py
flask run
```

## License ##
This repository is licensed under the GNU GPLv3 license.

