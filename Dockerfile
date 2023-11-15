# Use python:3.9-slim
FROM python:3.9-slim

# Set the working dir in the container
WORKDIR /app

# Set env variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the dependency file to the working dir of the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Delete the keys dir
RUN rm -rf /keys

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Generate keys
RUN mkdir -p /app/keys && openssl genpkey -algorithm RSA -out /app/keys/private_key.pem
RUN openssl rsa -pubout -in /app/keys/private_key.pem -out /app/keys/public_key.pem

# Copy the contents of the current dir (your project) into the container
COPY . /app/

# Launch the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
