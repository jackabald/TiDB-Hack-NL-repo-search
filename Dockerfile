# Use the official Python image as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 8501

# Define environment variable for Streamlit to access secrets from .streamlit/secrets.toml
ENV STREAMLIT_SECRETS_PATH="/app/.streamlit/secrets.toml"

# Set the entrypoint for the application
ENTRYPOINT ["streamlit", "run"]

# Set the default command to run the app
CMD ["app.py"]
