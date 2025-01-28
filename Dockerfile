# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory inside the container
WORKDIR /app

# Remove the existing /app/logs directory to allow the volume mount
RUN rm -rf /app/logs

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]