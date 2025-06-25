# Python Virtual environment
# https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

# Install virtual env
# If it doesn't work, try python3
python -m pip install virtualenv

# Create virtual env
py -m venv venv

# Activate venv on CMD
.\venv\Scripts\activate

# Activate venv on Power Shell
.\venv\Scripts\activate.bat

# Activate venv on Bash
./venv/Scripts/activate

# requirements.txt file is for managing dependencies for each python project.
# After you have installed the needed dependencies for a new project, create a requirements.txt file.
pip freeze > requirements.txt

# install dependencies from requirements.txt file
pip install -r requirements.txt