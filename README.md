# Project Goal:
* Deploy phone application that can identify flesh and blood cards reliably from the phone's camera
* Display the cost at time of scan
* Store a separate image of the card within a virtual collection

# How to run:
* SETUP `pipenv`, pipenv is awesome and combines virtual environments and package management into one tool for python that works similarly to `yarn` or `npm`. Basically `brew install pipenv` and then `pipenv install` inside the project folder... then run `pipenv shell` (I think)... google for the particular setup: helpful article https://realpython.com/pipenv-guide/ ... also pipenv dev effort is kind of dead, but who cares :) 
  
* RUN `src/scraper.py` to populate the postgresql database with monarch cards
* MODIFY `src/main.py` depending on what you'd like to test, invoking the following in global scope:
  * `rd.example` - turns on laptop camera and will show boxes around the text that's identified, a messy display of that text is shown in real time on the top left of the camera feed
  * `rd.process` has functions for both reading an image from the camera (eventually to mirror the `rd.example` code) and reading an image from the source photo within the repo (uncomment read_image_from_src, comment_out read_image_from_cam)

# Useful Commands
## kill postgres
* `sudo pkill -u postgres`
## check posts in use
* `ps -ef | grep postgres`