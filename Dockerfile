FROM python:3.12-alpine

# Set the working directory
WORKDIR /

# Create and activate a virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy all the files
COPY /app /app/
COPY *.py ./
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN ls -la /app/*
RUN rm -rf /var/cache/apk/* && \
rm -rf /root/.cache

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]