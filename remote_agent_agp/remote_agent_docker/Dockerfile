# Use a full Python image for better debugging support
FROM python:3.12

# Set working directory inside the container
WORKDIR /server

# Install system dependencies including Rust
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    gcc \
    libssl-dev \
    pkg-config && \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH"

# Upgrade pip before installing dependencies
RUN python -m pip install --upgrade pip

# Copy requirements.txt from the parent directory
COPY ../requirements.txt /app/requirements.txt

# Copy the entire server source code from the parent directory
COPY ../server /server

# Ensure Rust is available in PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose necessary ports
# ENV PORT=46357
# EXPOSE ${PORT}

# Install debugging tools (optional)
RUN apt-get update && apt-get install -y vim curl net-tools iputils-ping && rm -rf /var/lib/apt/lists/*

# Start the application
CMD ["python", "main.py"]
