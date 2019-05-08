from flask import Flask, url_for
import datetime
import jsonpickle as jsp
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from stc_classes import Client, Task, Seller, Tasks


app = Flask(__name__)
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
content_section = "@content"

# @app.route("/")
# def hello():
#     return read_file("Example.html")

# somefunc = app.route("/")
# hello = somefunc(hello)
@app.route("/seller")
def seller():
    return process_template("seller.frg")

@app.route("/client")
def client():
    return process_template("client.frg")

@app.route("/task")
def task():
    tasks_example = Tasks([])
    tasks_example.read_from_file()
    return process_template(tasks_example)

@app.route("/synchronize")
def synchronize():
    sync_with_calendar()
    return process_template("calendar.frg")

def read_file(file_path):
    f = open(file_path, "r")
    content = f.read()
    f.close()
    return content

def find_word_position(word, line):
    """
    Used to locate word in strings. Returns number of position.
    (str, str) --> (int)
    """
    line_position = 0
    line_length = len(line)
    word_length = len(word)
    while line_position <= (line_length - word_length):
        found = True
        word_position = 0
        for letter in word:
            if letter == line[line_position + word_position]:
                word_position += 1
            else:
                found = False
                break
        if found == True:
            return line_position
        line_position += 1
    return -1

def process_template(content_fragment):
    """
    Returns HTML-tagged string.
    (str) --> (str)
    """
    global content_section
    template = read_file("/home/galya/myweb/templates/main.tmpl")
    position = find_word_position(content_section, template)
    if position == -1:
        return "Error happened with finding content section"
    result = ""
    for i in range(position):
        result += template[i]
    if type(content_fragment) == Tasks:
        insert_table = content_fragment.render_as_html()
    else:
        insert_table = read_file("/home/galya/myweb/templates/" + content_fragment)
    result += insert_table
    for i in range((position + len(content_section)), len(template)):
        result += template[i]
    return result

def sync_with_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # f = open("your_events.json", "w+")
    # f.write(jsp.encode(events))
    # f.close()
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

    tasks_example = Tasks([])
    tasks_example.read_from_file()

    for task in tasks_example.lst_of_tasks:
        my_event1 = {
          'description': 'Pusta strichka',
          'start': {
            'dateTime': '2015-05-28T09:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
          'end': {
            'dateTime': '2015-05-28T17:00:00-07:00',
            'timeZone': 'America/Los_Angeles',
          },
        }
        my_event1["description"] = task.description
        my_event1["start"]["dateTime"] = '2019-05-28T09:00:00-07:00'
        my_event1["end"]["dateTime"] = '2019-05-29T09:00:00-07:00'
        my_event1 = service.events().insert(calendarId='primary', body=my_event1).execute()
        print('Event created: {}'.format(my_event1.get('htmlLink')))
