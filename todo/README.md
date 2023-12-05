# Blip ToDo

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

ToDo app developed in Django for the Flutter UKI CTF.

App done for the exercise Vulnerable Dependency Lib.

App functions like your standard ToDo app you saw a million times before.

This CTF requires you to do a bit of recon, analyze the libs it uses and explore for potential flaws (exploit-db, snyk etc....)

Analyze the instances where the function is used, see where it can cause more damage.

Understand the logic implemented and use the exploit.py to craft the payload.

App can be run locally:

```shell
pip install -r requirements.txt
cd /todo_list
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py runserver
```

Or much easier using docker:

```shell
docker-compose up
```

P.S Do not forget the set the values in the **.env** file in the root of the project

The file should look something like this:

```
DJANGO_SECRET_KEY="YOUR_SECRET_KEY"
FLAG="YOUR_SECRET_FLAG"
```

Made with ❤️ for the craft

Feel free to use and adapt this for any CTF you may think of hosting.
