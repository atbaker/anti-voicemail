FROM python:3.7.6

# Make our source directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install our requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY requirements-for-test.txt .
RUN pip install -r requirements-for-test.txt

# Copy our app source code
COPY . .

# Set the FLASK_APP environment variable
# ENV FLASK_APP=anti_voicemail

EXPOSE 5000

CMD ["gunicorn", "-c", "anti_voicemail/gunicorn.py", "anti_voicemail:app" ]
