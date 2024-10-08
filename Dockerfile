FROM python:3.12.1

RUN useradd -m  azureuser

WORKDIR /app

# Copy the requirements file to the container
COPY . .
# Install the dependencies
RUN chown -R azureuser:azureuser /app

USER azureuser

RUN pip install --no-cache-dir -r requirements.txt


# Expose the port that Uvicorn will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0"]
