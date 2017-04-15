# recipes
Get recipe from available ingredients.

## ER diagram

![ER diagram](https://github.com/zigazupancic/recipes/blob/master/ER.png)


## Navodila

* Namesti Postgresql z ukazom `sudo apt-get install postgresql postgresql-contrib`
* Namesti psycopg2: `pip install psycopg2`
* Ustvari bazo ter uporabnika baze `recipesuser` z geslom `recipespass`:
```
sudo -i -u postgres
psql
create database recipes;
create user recipesuser with password 'recipespass';
grant all privileges on database recipes to recipesuser;
\q
exit
```

* Server se zažene z ukazom `python3 manage.py runserver`, do aplikacije pa lahko dostopamo na
[127.0.0.1:8000/getrecipe](http://127.0.0.1:8000/getrecipe).