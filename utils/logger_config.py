import logging
import os
from datetime import datetime

class TestLogger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not TestLogger._initialized:
            # Create logs directory if it doesn't exist
            self.logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
            os.makedirs(self.logs_dir, exist_ok=True)

            # Generate unique log filename based on timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_filename = f'test_run_{timestamp}.log'
            self.log_file_path = os.path.join(self.logs_dir, log_filename)

            # Configure logging
            self.logger = logging.getLogger('TestAutomation')
            self.logger.setLevel(logging.INFO)

            # Clear any existing handlers (important for singleton pattern)
            if self.logger.handlers:
                self.logger.handlers.clear()

            # File handler
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(logging.INFO)
            file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(file_format)
            self.logger.addHandler(console_handler)

            TestLogger._initialized = True

    def get_logger(self):
        return self.logger