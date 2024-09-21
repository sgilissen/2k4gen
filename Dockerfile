# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Make port 5000 available to the world outside this container
EXPOSE 5000

# Step 6: Define the environment variable to tell Flask it's in development mode
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Step 7: Run the app when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
