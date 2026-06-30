FROM python:3.12-slim

# Create a non-root user (Hugging Face Spaces requires user 1000)
RUN useradd -m -u 1000 user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# Install Python requirements AS ROOT
# ----------------------------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files with ownership
COPY --chown=user:user . .

# Ensure necessary directories exist and are writable by the user
RUN mkdir -p /app/database /app/uploads /app/logs && \
    chown -R user:user /app/database /app/uploads /app/logs && \
    chmod -R 777 /app/database /app/uploads /app/logs

# Switch to the non-root user (Everything after this runs safely as user 1000)
USER user

# Hugging Face Spaces exposes port 7860
EXPOSE 7860

# Run Streamlit on port 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
