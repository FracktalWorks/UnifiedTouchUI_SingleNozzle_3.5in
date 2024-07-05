import datetime

LOG_FILE = 'log.txt'

def write_to_log(file_path, message):
    with open(file_path, 'w') as file:
        file.write(message + '\n')

def append_to_log(file_path, message):
    with open(file_path, 'a') as file:
        file.write(message + '\n')

def log_debug(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_log(LOG_FILE, f'{timestamp} - DEBUG - {message}')

def log_info(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_log(LOG_FILE, f'{timestamp} - INFO - {message}')

def log_warning(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_log(LOG_FILE, f'{timestamp} - WARNING - {message}')

def log_error(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_log(LOG_FILE, f'{timestamp} - ERROR - {message}')

def log_critical(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_log(LOG_FILE, f'{timestamp} - CRITICAL - {message}')

def start_logger(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_to_log(LOG_FILE, f'{timestamp} - INFO - {message}')

# Example usage
# log_debug('This is a debug message')
# log_info('This is an info message')
# log_warning('This is a warning message')
# log_error('This is an error message')
# log_critical('This is a critical message')
