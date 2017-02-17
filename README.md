# NeuroPy
[![Build Status](https://travis-ci.org/NeuroPyPlanner/NeuroPy.svg?branch=development)](https://travis-ci.org/NeuroPyPlanner/NeuroPy)

Personalized CBT-based priority planner

## Creators:

[Amos Bolder](https://github.com/amosboldor) | [Claire Gatenby](https://github.com/clair3st) | [Patrick Saunders](https://github.com/pasaunders) | [Sera Smith](https://github.com/serashioda)

### URL: [HERE](http://ec2-52-14-126-118.us-east-2.compute.amazonaws.com/)

### About the App:
A personalized priority app to support a *Cognitive Behavioral Therapy* (CBT) approach to efficiently organize your day according to a struggle/disorder that is effectively treated by CBT. CBT is a goal-oriented pyschotherapy treatment, taking a hands-on approach to problem solving. Goal of CBT is to change the patterns of thinking or behavior that are behind a person's difficulties, modifying their feelings and therefore their thinking and behavior overtime.

*Neuropy* Considers what the habit/disorder the user wants to treat with CBT, along with medication, it's half-life and peak periods. Also works around black-out periods on user's schedule by syncing with Google Calender, personal preference or most productive period of the day for user, and finally considers time commitments for each activity. Each "TO-DO" will be ranked considering these aspects and will be worked into periods of the day.

##### version-0.1 (in active development)
##### Keywords:

No medical data is stored by NeuroPy

##Getting Started

Clone this repository into whatever directory you want to work from.
```
https://github.com/NeuroPyPlanner/NeuroPy.git
```
Assuming that you have access to Python 3 at the system level, start up a new virtual environment.
```
$ cd NeuroPy
$ python3 -m venv ENV
$ source ENV/bin/activate
```
Once your environment has been activated, make sure to install Django and all of this project's required packages.
```
(NeuroPy) $ pip install -r requirements.pip
```
Navigate to the project root, imagersite, and apply the migrations for the app.
```
(NeuroPy) $ cd imagersite

(NeuroPy) $ ./manage.py migrate
```
Finally, run the server in order to server the app on localhost
```
(NeuroPy) $ ./manage.py runserver
```
Django will typically serve on port 8000, unless you specify otherwise. You can access the locally-served site at the address http://localhost:8000.


##Current Models (outside of Django built-ins):

This application allow users to store and organize photos.

**The `Profile` model contains:**

- The period which the user is up and active
- The time of day when a user is best able to focus and work
- The time of day when a user takes their medication
- A __str__ method which returns the user's username.

**The `Todo` model contains:**

- Date
- Ease of accomplishing the task
- Duration of task
- Owner of the task
- Title of the task
- Description
- Priority level
- A __str__ method which returns the task title

**The `Medication` model contains:**

- Name
- Medication Type
- Use (on or off label)
- Half life
- Ramp-up time
- Peak Period
- Start and end times for the easy, medium and peak energy periods
    represented as a comma seperated set of integers where the first
    integer represents the number of hours since the user took the
    medicaion, and the second integer representing the number of extra
    minutes.
- A __str__ method which returns the medication's name

##Current URL Routes

- `/oauth2/` Google calendar request authorization
- `/admin` Superuser admin page.
- `/` Home page.
- `/login` Login page.
- `/logout` Logout route, no view.
- `/accounts/register` Register a user form.
- `/accounts/activate/complete/` Activation complete view.
- `/accounts/register/complete/` Registration complete, email sent.
- `/profile/` Links to the following routes:
    - `/` Shows the user their profile data.
    - `/edit/` Allows the user to edit their profile
- `/profile/todo/ Links to the following routes:
    - `/calendar/` Allows the user to view their schedule
    - `/schedule/` Shows the user's to-do list ordered by priority and difficulty
    - `/[todo_id]/edit/` Allows the user to edit their to-do items
    - `/[todo_id]/` Detail view for an individula to-do item
    - `/add/` Allows the user to create a new to-do item
    - `/` Shows the user a summary of all their to-do items


##Running Tests

Running tests for the NeuroPy is fairly straightforward. Navigate to the same directory as the manage.py file and type:
```
(NeuroPy) $ coverage run manage.py test
```
This will show you which tests have failed, which tests have passed. If you'd like a report of the actual coverage of your tests, type
```
(NeuroPy) $ coverage report
```
This will read from the included .coverage file, with configuration set in the .coveragerc file. Currently the configuration will show which lines were missing from the test coverage.


### USER STORIES:

#### User Stories

- As a user I want the app to use good CBT principles so that I can effectively manage my energy.
- As a user I want the app to take my medications into account so that I can work at my highest-focus time of day.
- As a user I want the app to take in my personal preferences into account so that I don’t work on easy tasks when I have energy and hard tasks when I’m tired.
- As a user I want the app to preserve my preferences so that I can conveniently generate new schedules.
- As a user I want to be able to input my personal preferences and data easily and accurately so that the app can prioritize my day effectively.
- As a user I want my medical data to be secure so that I can avoid fraud and identity theft.
- As a user I want to be able to quickly generate schedules with minimal clicks so that I don’t have to spend all my energy organizing.
- As a user I want my newly generated schedule to be integrated into my google calendar with notifications.
- As a user I want the app to take into account my sleep schedule so that I can work when I have the most energy.


#### Developer Stories

- As a developer I want readable and well documented code to make maintenance easier.
- As a developer I want to practise test driven development in building my app and spotting bugs early on.
- As a developer I want to avoid storing any medical data so that I don’t have to deal with HIPAA violations.
- As a developer I want to store data of users in appropriate models, with logical relationships.
- As a developer I want to build for one disorder before expanding so that I can build on a strong foundation.
- As a developer I want a narrow open source license so that we retain plenty of rights to our work.
- As a developer I want to write an algorithm that prioritises todos based on a user’s profile.
- As a developer I want to integrate the google calendars with my app using an api.
