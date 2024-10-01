FROM python:3.5

# Update and clean apt-get cache
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user and group for gongyitong
RUN groupadd -g 799 gongyitong && \
    useradd -r -u 999 -g gongyitong gongyitong

# Set working directory
WORKDIR /app

# Install Flask with a specific version
RUN pip install Flask==1.1.2

# Set the user to gongyitong
USER gongyitong

# Copy the application files, adjusting ownership
COPY --chown=gongyitong:gongyitong . .

# Set the default command to run the application
CMD ["python", "run.py"]
