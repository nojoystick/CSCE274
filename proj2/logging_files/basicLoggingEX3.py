import logging

# This will be a demonstration of passing variables to your log file
# This assumes you have looked at example 1 and example 2 first

# Creating logger
l1 = logging.getLogger('example3')
l1.setLevel(logging.DEBUG)

# Creating handler

fh = logging.FileHandler('example3.log')
fh.setLevel(logging.DEBUG)

# Creating formatter

form = logging.Formatter('%(asctime)s, %(message)s')

# Add formatter to handler

fh.setFormatter(form)

# Add handler to logger

l1.addHandler(fh)

# Test logs
v1=5
v2='I\'m a single pringle'
v3=10.5
v4=False
v5='C'

l1.debug(v1)
l1.info(v2)
l1.warn(v3)
l1.error(v4)
l1.critical(v5)
