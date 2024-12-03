#! /bin/sh
echo "\n\n---------------------------------------------------------------------------"
echo "\n\tWelcome to to the setup. This will setup the local virtual env." 
echo "\tAnd then it will install all the required python libraries."
echo "\tYou can rerun this without any issues."
echo "\n---------------------------------------------------------------------------"
if [ -d ".env" ];
then
    echo "\n\t.env folder exists. Running your Application"
else
    echo "\n\tcreating .env and install using pip wait"
    python3.12 -m venv .env
    
    # Activate virtual env
    . .env/bin/activate

    # Upgrade the PIP
    pip install --upgrade pip
    pip install -r requirements.txt

fi
echo "\n---------------------------------------------------------------------------"
echo "\n\t Welcome to Household Services Application\n"
echo "---------------------------------------------------------------------------"

export FLASK_ENV=development
python3 main.py

# Work done. so deactivate the virtual env
deactivate
