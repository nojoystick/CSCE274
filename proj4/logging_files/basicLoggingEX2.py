import logging
import time

# Log objects consist of four main parts:
# 1. The actually Logger class (AKA loggers), which exposes the interface to application code.
# 2. Handlers which determine where to to send the log records (created by loggers)
# 3. Filters which provide for finer tuning of determining where logs output (we will be ignoring this)
# 4. Formatters which specify how you want the log record to look: Ex: <timestamp><datum>

# Lets go through each of the steps one by one

# 1. Creating logger objects 

# This creates a logger object corresponding to 'example2' and sets its level to DEBUG
logger1 = logging.getLogger('example2')
logger1.setLevel(logging.DEBUG)

# 2. Create a handler which logs the messages

# This creates a handler that will log to the file example2.log
fh = logging.FileHandler('example2.log')
fh.setLevel(logging.DEBUG)

# 3. We are skipping over filters

# 4. Creating a formatter

formatter1 = logging.Formatter('%(asctime)s - %(message)s')

# Now that everything is created there are a few more steps to go through
# First add the formatter to the handler
# This means that the handler will now log as we have defined it

fh.setFormatter(formatter1)

# Finally, add the handler to the actual logger object
logger1.addHandler(fh)

# Time to test out that it works as intended
# First, it should log all levels of logs from DEBUG - CRITICAL
# Second, it should format it <time><message/datum>
# Third it should be stored inside the file example2.log

logger1.debug('DEBUG')
logger1.info('INFO')
logger1.warn('WARN')
logger1.error('ERROR')
logger1.critical('CRITICAL')
