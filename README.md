## Tango Recruitment Project

### Random thoughts
There are definitely some concessions made here and there to save time. For example the authorization
system is a very basic one utilizing simple username and password login, while for production I would
opt for fe. a JWT token based auth or even a separate authorization service. I would also use caching
for the `get_user` to avoid unnecessary database queries. I would have also opted for a completely
different approach to timezone awareness (in short having BE operate and store times in UTC only and
have FE display times using the user's timezone from either the User model or browser context) but
this particular case has to fulfill the business requirements using only BE.

I also realize that methods from SQLAlchemy ORM I am using are "deprecated" so to speak (even though
they are not planning on ever removing the support), but it was easier to work for me with what I 
used last time I worked with SQLAlchemy (more than 2 years ago) instead of the new ORM V.2 they implemented.

I am open for any discussion and questions as to the choices made and if I would do something 
differently for a production grade app.

### Usage guide
To run the application just use
```bash
docker-compose up
```
from the project root. You can then test the endpoints out by going to `http://127.0.0.1:8000/docs#`

To run the app locally you will need to run a PostgreSQL database, set up your env variables accordingly
(all the necessary ones are in `.env` file) and then run FastAPI server with
```bash
fastapi dev app/main.py
```

### Creating Test Data
There is a Python script that will help to fill in the database with some test data.
**It is important to generate the data in the order of Users -> Conference Rooms -> Calendar Events**.

The options are as follows:

#### Generating Users
To generate a single User with a pre-specified data run:
```bash
python generate_data.py --generate-users --username someuser --password somepassword --email test@gmail.com --company_id 6196fcb5-062d-4d4c-84b7-c8bb7bd40b9b --timezone Europe/Warsaw
```
To create multiple randomized Users run:
```bash
python generate_data.py --generate-users --count 20
```
with the `--count` flag specifying how many users you want to generate (as this is just a helper script there is no limit on the number so be careful ;)).

#### Generating Rooms
To generate Conference Rooms run:
```bash
python generate_data.py --generate-rooms --count 20
```

#### Generating Calendar Events
To generate Calendar Events run:
```bash
python generate_data.py --generate-events --count 20
```
