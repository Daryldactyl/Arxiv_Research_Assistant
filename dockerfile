# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /deployable_app

# Copy the current directory contents into the container at /app
COPY . /deployable_app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies for the app
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install the Streamlit-specific dependencies
RUN pip install streamlit

# Expose port 8501 for the Streamlit app
EXPOSE 8501

# Define environment variable
ENV STREAMLIT_SERVER_PORT 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]