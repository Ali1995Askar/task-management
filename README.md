** Tasks Management Django Application** <br />

**Steps to run locally:** <br />
1- Install all requirements using 'pip install -r requirements.txt'<br />
2- Add .env file next to .env.example file with same parameters you can copy the env.example (WORKING_SETTINGS) variable use 'LOCAL' to run it locally and 'DOCKER' to run it with docker <br />
3- Cd to root folder (to manage.py) then run migrate command 'python manage.py migrate' <br />
4- Run tests using 'python manage.py test' to test (or for each app (add the app name after the command)0<br /> <br />

**Steps to run with docker and docker-compose:** <br />
1- make sure you have docker and docker compose on your system<br />
2- we will use same .env file as file for web service so create .env file similar to env.example<br />
3- cd to docker-compose.yml file and run 'docker compose up' or with sudo if you don't have permission<br />

**Notes:** <br />

1- i kept two ways to run because pythonanywhere doesn't accept to deploy with docker images <br /> <br />
2- with docker we use postgres image for database instead of sqllite <br /> <br />
3- You will see instead of settings file a python module which is same but just to split the project to stages
development, staging and production (just files architecture)<br /> <br />
4- A html design is designed by bootstrap but we migrate it to jinja and django template.

**BY Eng. Ali Askar**