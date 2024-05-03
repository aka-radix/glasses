# Use an official Python runtime as a parent image
FROM python:3.12

# Install Poetry for managing dependencies
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2
ENV PATH="${PATH}:/root/.local/bin"

ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the project code into the container
COPY . /app/

# Install the dependencies
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR


EXPOSE 8000:8000
