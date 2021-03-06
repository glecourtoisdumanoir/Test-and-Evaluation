import logging

# create logger with 'spam_application'
logger = logging.getLogger('PetterExample')
logger.setLevel(logging.DEBUG)
# create file handler 
fh = logging.FileHandler('/home/jeff/Desktop/Test/lowLevelTesting/temp/v2gross.csv', "w")
# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(message)s')
#fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

