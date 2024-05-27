FROM python:3.11-slim

WORKDIR /workspace

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip

# Copy everything to /workspace
COPY ./requirements.txt /workspace
COPY ./app /workspace/app

# Install required Python packages from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application with uvicorn
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]