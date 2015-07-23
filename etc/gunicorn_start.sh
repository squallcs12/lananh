#!/bin/bash

DEPLOY_DIR=/var/www
CURRENT_DIR=$DEPLOY_DIR/current
NAME="www"                                # Name of the application
DJANGODIR=$CURRENT_DIR         		              # Django project directory
SOCKFILE=$DEPLOY_DIR/run/gunicorn.sock	  # we will communicte using this unix socket
USER=www                                          # the user to run as
GROUP=www                                         # the group to run as
NUM_WORKERS=8                                     # how many worker processes should Gunicorn spawn
DJANGO_WSGI_MODULE=root.wsgi                      # WSGI module name

echo "Starting $NAME"

# Activate the virtual environment
workon www
cd $DJANGODIR
source .config/env.sh
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --bind=unix:$SOCKFILE
