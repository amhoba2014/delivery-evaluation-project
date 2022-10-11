## What is this?

This is the delivery evaluation project that I've created.

## Technologies

The python version used throughtout this application is `3.10.4`.

I've used `FastAPI` framework for creating the REST API endpoints, cause its modern and fast and contains many developer
and human friendly toolchains.

I've used `SQLAlchemy` for the database design and ORM, because it's a full-featured and mature framework for database
interaction and design.

The database is a `PostGreSQL` instance as denoted in the evaluation PDF file.

The whole project is containerized under docker, so you will need `docker` plus `docker compose` to be able to bring
this project up for yourself.

This source also includes an instance of `pgAdmin4` which can be used as a frontend to the PostGreSQL database.

Environment variables for configurations are stored in the `.env` file (like postgres username, password and database
name etc.)

The database is euphemeral, meaning that nothing is saved on disk. So if you bring the whole containers down, everything
is removed. This is done by intention (and can be changed at your will)

The CSV file is auto imported to the database on application startup. I've decided to put the `data.csv` file alongside
the `source` folder of the `main` service. This is done for simplicity although I myself do not like this idea and would
have created another api endpoint to consume the CSV file as an additional feature of this project.

## How to see this project live?

Its simple, Just clone this repository:

```shell
git clone https://github.com/amhoba2014/delivery-evaluation-project ;
cd delivery-evaluation-project ;
```

### Only `main`

If you want to only start the `main` service:

```shell
./do_start.sh ;
```

And then open your browser at this address to view the `Swagger` interface to directly interact with the service:

http://127.0.0.1:8000/docs

### `main` with `pgadmin` interface

If you want to both start the `main` and `pgadmin` service (to be able to browser the database in a graphical
interface):

```shell
./do_start_with_pgadmin.sh ;
```

This will run the `main` service on port `8000` and `pgadmin` on port `8001` (`pgadmin` service took 3 - 4 minutes to
start on my laptop, so it may do the same on your workstation).

After both services are up, open these urls in your browser:

http://127.0.0.1:8000/docs  
http://127.0.0.1:8001/

## Describing the source

First, this source is put under `delivery_app` python package folder to not conflict with other files with the same
names throughout the project.

Database models are stored under `models.py` file.  
We've got a one-to-many relatinship between the `Route` and `Deliverie` database tables.  
The `eta` field of `Deliverie` table is a **timezone-aware** postgres datetime field.

Database settings are stored in the `database.py`.  
The configuration is read from environment variables (which is shared with the `db` service).  
Postgres stores timezones in `UTC` internally. To change this behavior we have added the `"options": "-c timezone=Iran"`
option to `connect_args` which ensures that the database service will use the `Iran` timezone all the time.

The `importer.py` file contains the functionalities to read and import the CSV file.

The `schemas.py` file contains the pydantic REST API request and response models (with data validation).

The `main.py` includes the rest api endpoint definitions.

## License

MIT