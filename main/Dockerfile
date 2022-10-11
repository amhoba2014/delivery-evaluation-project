FROM python:3.10.4-slim

# Add a non-root user
RUN useradd -ms /bin/bash python

# Install dependencies for compiling psycopg2
RUN apt update -y && apt install -y libpq-dev
RUN apt install -y build-essential gcc

# Installing wait-for-it.sh util which is used for waiting for postgres service to come up
RUN apt install -y wget
RUN cd /usr/local/bin \
    && wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x wait-for-it.sh

# Install python dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Setting non-root user as the default, setting the workdir and then its done
USER python
WORKDIR /app
CMD ["wait-for-it.sh", "-t", "20", "db:5432", "--", "uvicorn", "--host", "0.0.0.0", "--reload", "delivery_app.main:app"]
