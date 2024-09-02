FROM alpine:latest AS builder

# Set DEPLOY=1 environnement variable
ENV DEPLOY=1

# Install dependencies
RUN apk update
RUN apk upgrade --available
RUN apk add --no-cache git python3 python3-dev py-pip tzdata mariadb-client mariadb-connector-c-dev gcc musl-dev rust cargo libffi-dev mariadb-dev
RUN pip3 install --upgrade --break-system-packages virtualenv wheel

# Add an user
RUN adduser -D external_stats

# We copy the files from the parent directory
COPY . Upsilon-External-Stats-Server

# Remove the .git folder
RUN rm -rf Upsilon-External-Stats-Server/.git

# Change the owner of the files
RUN chown -R external_stats:external_stats Upsilon-External-Stats-Server

# Run as the user
USER external_stats

WORKDIR /Upsilon-External-Stats-Server

# Create a virtual environment
RUN virtualenv -p python3 venv

# Activate the virtual environment
ENV PATH="/Upsilon-External-Stats-Server/venv/bin:${PATH}"

# Install the dependencies
RUN pip3 install -r requirements.txt gunicorn

# RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput

RUN sed -i 's/ALLOWED_HOSTS: list\[str\] = \[\]/ALLOWED_HOSTS: list\[str\] = \["*"\]/g' external_stats/settings.py

# Expose the port
EXPOSE 80

# Entrypoint
CMD ["sh", "-c", "sh ./prepare_run.sh && python3 $(which gunicorn) external_stats.wsgi --bind 0.0.0.0:8000"]


# Deployment image (no build dependencies)
FROM alpine:latest

# Set DEPLOY=1 environnement variable
ENV DEPLOY=1

# Install dependencies
RUN apk update && apk upgrade --available && apk add --no-cache mariadb-client mariadb-connector-c tzdata python3

# Add an user
RUN adduser -D external_stats

# Copy the files from the builder image
COPY --from=builder /Upsilon-External-Stats-Server /home/external_stats/Upsilon-External-Stats-Server

# Activate the virtual environment
ENV PATH="/home/external_stats/Upsilon-External-Stats-Server/venv/bin:${PATH}"

# Change the owner of the files
RUN chown -R external_stats:external_stats /home/external_stats/Upsilon-External-Stats-Server

# Run as the user
USER external_stats

# Set the working directory
WORKDIR /home/external_stats/Upsilon-External-Stats-Server

# Expose the port
EXPOSE 80

# Entrypoint
CMD ["sh", "-c", "source venv/bin/activate && deactivate && source venv/bin/activate && sh ./prepare_run.sh && python3 $(which gunicorn) external_stats.wsgi --bind 0.0.0.0:8000"]
