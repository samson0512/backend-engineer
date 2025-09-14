# Use an official lightweight Python image as a base
FROM python:3.11-slim

# Set a neutral working directory
WORKDIR /code

# Copy the file with dependencies first to leverage Docker cache
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application folder and database into the container
# This makes 'app' a package inside /code
COPY ./app /code/app
COPY test.db .

# Expose the port your app runs on
EXPOSE 8000

# Command to run your application as a module
# This tells uvicorn to look for 'main' inside the 'app' folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]