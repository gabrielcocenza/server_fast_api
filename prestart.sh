#! /usr/bin/env bash

# Let the DB start
python ./backend_pre_start.py

# Run migrations
# alembic revision --autogenerate -m "Add User model"
# alembic upgrade head

# Create initial data in DB
python ./initial_data.py