# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
