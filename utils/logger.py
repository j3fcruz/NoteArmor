"""
utils/logger.py
Logging utilities for the application
"""

import os
import logging
import datetime
from utils._path_utils import PathResolver
from config.app_config import APP_NAME

class Logger:
    """Application logger with file and console output"""

    _initialized = False  # Prevent duplicate handlers

    def __init__(self, log_level=logging.INFO):
        self.logger = logging.getLogger(f"{APP_NAME}")
        self.logger.setLevel(log_level)
        self.logger.propagate = False  # Avoid duplicate logs in console

        # Only initialize once
        if not Logger._initialized:
            # Create logs directory
            log_dir = PathResolver.get_writable_path("logs")
            PathResolver.ensure_directory(log_dir)

            # Create log file with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_file = os.path.join(log_dir, f"app_log_{timestamp}.log")

            # File handler
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(log_level)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # Attach handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

            Logger._initialized = True  # Prevent re-adding handlers

    def log_info(self, message):
        """Log info message"""
        self.logger.info(message)

    def log_warning(self, message):
        """Log warning message"""
        self.logger.warning(message)

    def log_error(self, message):
        """Log error message"""
        self.logger.error(message)

    def log_debug(self, message):
        """Log debug message"""
        self.logger.debug(message)

    def log_build_start(self, tool_name, command):
        """Log build process start"""
        self.log_info(f"==> Starting '{tool_name}' build process")
        self.log_info(f"Command: {command}")

    def log_build_finish(self, tool_name, success, elapsed_time):
        """Log build process completion"""
        status = "SUCCESS" if success else "FAILED"
        self.log_info(f"<== {tool_name} build {status} in {elapsed_time:.2f} seconds")

    def log_exception(self, exception):
        """Log exception with traceback"""
        self.logger.exception(f"Exception occurred: {exception}")

    def get_log_file_path(self):
        """Get the path of the current log file"""
        return getattr(self, "log_file", None)

