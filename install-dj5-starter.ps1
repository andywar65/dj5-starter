# This file is a list of powershell commands to install dj5-starter
# Copy it in your computer, make changes where required and run

# change root and directory name
cd X:/your/venv/root
mkdir dj5-starter
cd dj5-starter
# start and activate virtual environment
py -3.10 -m virtualenv env
env/Scripts/activate
# make some other directories
mkdir static
mkdir media
# install pip-tools
python -m pip install pip-tools
# clone the repository, then jump in the directory
git clone https://github.com/andywar65/dj5-starter
cd dj5-starter
# install requirements
python -m pip install -r requirements.txt
# I use pre-commit systemwide, so I just install it in the local repository
pre-commit install
# Here we generate secret key and save it in .env file
python generate_dotenv.py
# standard + custom commands
python manage.py migrate
python manage.py create_super_user
# this is a ps shortcut for runserver
.\run
# You should be able to login with "andywar65" and "P4s5W0r6"
