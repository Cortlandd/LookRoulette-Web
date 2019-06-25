# Look Roulette

_The backend to Look Roulette. To allow transferring of makeup from one image to another._

# Usage
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- export FLASK_APP=roulette.py | _may not have to on windows_
- flask run

# TODO
- Improve security.
- Experiment with model for live makeup transfer

# Roadmap
- [ ] Initial 1.0 version to get users started
- [ ] Improved model
- [ ] Market place to sell looks and give users access to video content

# WAYYY down the line Roadmap
- [ ] Live makeup transfer

# Important documents to note
- https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957#51004957
- https://github.com/jeromevonk/flask_face_detection | Sample repo using opencv and heroku
- https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt | Used to install linux deps for python-opencv
