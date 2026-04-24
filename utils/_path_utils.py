"""
 utils/_path_utils.py
Path utilities for resource management and cross-platform compatibility
"""


import os
import sys
from pathlib import Path


class PathResolver:
    """Utility class for resolving paths in different deployment scenarios"""

    @staticmethod
    def get_base_path():
        """Get the base path for the application"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return os.path.dirname(sys.executable)
        else:
            # Running as script
            return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = PathResolver.get_base_path()

        return os.path.join(base_path, relative_path)

    @staticmethod
    def get_writable_path(relative_path):
        """Get a writable path for logs, configs, etc."""
        base_dir = PathResolver.get_base_path()
        return os.path.join(base_dir, relative_path)

    @staticmethod
    def ensure_directory(path):
        """Ensure a directory exists"""
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def get_dist_path():
        """Get the dist folder path"""
        return os.path.join(PathResolver.get_base_path(), "dist")

    @staticmethod
    def get_build_path():
        """Get the build folder path"""
        return os.path.join(PathResolver.get_base_path(), "build")

    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for cross-platform compatibility"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename

    @staticmethod
    def get_temp_path():
        """Get temporary directory path"""
        import tempfile
        return tempfile.gettempdir()
