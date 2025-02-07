# Use the official Python image as the base
FROM python:3.12.4-slim

# Set environment variables to prevent the generation of .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first for dependency installation
#COPY requirements.txt /app/

# Install Python dependencies
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files (code, assets, .env, etc.)
#COPY . /app/

# Expose the port if the bot uses any server (e.g., webhook)
# EXPOSE 8080

# The default command to run the bot
CMD ["python", "main.py"]