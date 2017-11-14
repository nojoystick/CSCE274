import logging # Self explanatory

# If the file does not exist it will be created 
# Only logs for levels at and above what you set
# The levels in order are: DEBUG, INFO, WARNING, ERROR, CRITICAL
# In this example I set to DEBUG so every kind of log will be logged
# If you changed the log level to WARNING for ex, then only warning, error, and critical will be logged.

logging.basicConfig(filename='example.log', level=logging.DEBUG) # Configs the log by specifying what file to log to and what levels to write for.
x=5
if(x==5):
  logging.debug('DEBUG')
  logging.info('INFO')
  logging.warning('WARNING')
  logging.error('ERROR')
  logging.critical('CRITICAL')
