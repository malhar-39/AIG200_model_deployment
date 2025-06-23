FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size, and --upgrade pip is good practice
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copy the rest of your application's code to the working directory
COPY . .

# Expose port 8000 to allow communication with the application
EXPOSE 8000

# Define the command to run your app using uvicorn
# We use --host 0.0.0.0 to make it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]