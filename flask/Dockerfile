# Use the official Playwright image
FROM mcr.microsoft.com/playwright:v1.42.1-focal

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run app.py when the container launches
CMD ["python3", "-m", "flask", "run"]
