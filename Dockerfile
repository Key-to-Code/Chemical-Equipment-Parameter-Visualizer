# Dockerfile for Django Backend
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY ChemicalEquipmentParameterVisualizer/ChemicalEquipmentParameterVisualizer/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY ChemicalEquipmentParameterVisualizer/ChemicalEquipmentParameterVisualizer/backend/ .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD python manage.py migrate --noinput && gunicorn equipment_api.wsgi:application --bind 0.0.0.0:$PORT
