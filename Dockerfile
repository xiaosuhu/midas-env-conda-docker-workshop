FROM python:3.10-slim

WORKDIR /app

COPY pip_requirements.txt .
RUN pip install --no-cache-dir -r pip_requirements.txt

COPY analysis.py .

CMD ["python", "analysis.py"]
