FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy project definition and source code for installation
COPY pyproject.toml .
COPY src src

# Install dependencies and the package
RUN pip install --no-cache-dir .

# Copy the rest of the application
COPY . .

EXPOSE 8000

# Default command (can be overridden)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
