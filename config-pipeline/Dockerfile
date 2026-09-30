FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY generate.py template.j2 devices.yml ./
CMD ["python", "generate.py"]