# Stage 1: Build stage
FROM python:3.10-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to the container
COPY ./app/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.10-slim AS production

# Set the working directory in the container
WORKDIR /app

# Copy the installed Python dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy the Flask application code to the container
COPY ./app/. .

# Set the environment variables
ENV PATH=/root/.local/bin:$PATH
#ENV API_KEY="your-api-key-value"
ENV PYTHONUNBUFFERED=1

# Install Gunicorn
RUN pip install gunicorn[gevent]

# Expose the port that the WSGI server will listen on
EXPOSE 8080

# Start the WSGI server (Gunicorn) with the Flask application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--worker-class", "gevent", "api_flask:app"]