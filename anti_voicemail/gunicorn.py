# gunicorn configuration for anti-voicemail

bind = '0.0.0.0:5000'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'
