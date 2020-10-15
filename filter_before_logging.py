import logging

from opencensus.ext.azure.log_exporter import AzureLogHandler

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger('log-app')
logger.setLevel(logging.DEBUG)

def filter_log(envelope):
    print('In callback function')
    logMessage = envelope.data.baseData.message
    if(logMessage.find('secret') >= 0):
        print('log message contains sensitive information')
        return False
    return True

fileHandler = logging.FileHandler("{0}/{1}.log".format('.', 'test'))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

#use valid Application Insights instrumentation key
insightsHandler = AzureLogHandler(connection_string='InstrumentationKey=06e8****-****-****-****-********a701') 
insightsHandler.setFormatter(logFormatter)
insightsHandler.add_telemetry_processor(filter_log)
logger.addHandler(insightsHandler)

app_properties = {'app_name': 'log_filter', 'api_key': 'ertsyulkhgjhgf', 'api_secret': 'CYUJKLJKHGFHVB3456YHG89GHJ4567VB'}

print('Sending logs to app insights')
logger.info("Log statment without any sensitive information")
logger.debug('Log statement with sensitive information: %s', app_properties)
print('End sending logs to app insights')
