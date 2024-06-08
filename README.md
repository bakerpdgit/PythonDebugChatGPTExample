This is a small demo FLASK server to illustrate ChatGPT 4o API calls to assist in debugging in a small Python snippet of code e.g. for educational purposes to assist students.

You will need:
- somewhere to host your FLASK server e.g. sign up for free at eu.pythonanywhere.com
- to add a .env file which has a single API_KEY=<value> where value is your OpenAI API project key which you can generate by signing up at OpenAI and adding some credit e.g. $5
- make sure you check out their API pricing rate per input/output tokens (but it is a lot cheaper for GPT 4o)

To setup your Flask Server on pythonanywhere, follow instructions: can just use activate a default Flask app and then make adjustments:
https://help.pythonanywhere.com/pages/Flask/#:~:text=There%20are%20two%20main%20ways%20to%20set%20up,app%20using%20Manual%20configuration%2C%20and%20using%20a%20virtualenv
- add a web app
- upload these files and folders into your mysite folder
- use the BASH console to install the needed modules (requirements.txt)
- configure your WSGI file to load in your environment variables e.g. add

...

# process secret env vars
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/mysite')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

...

- click the RELOAD button on the web app to update it whenever you make changes
