FROM python:3.10 

# Setting the working directory
WORKDIR /app

# Copying and instaling the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Copying the source code
COPY . .

# using -p 8000:8000 to run this container
EXPOSE 8000 

# Command to run application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

