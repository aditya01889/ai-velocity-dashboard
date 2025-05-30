import logging
import sys
from typing import Optional
from pathlib import Path
from datetime import datetime

from app.utils.config import settings

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# File handler log format
FILE_FORMATTER = logging.Formatter(
    fmt=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT
)

# Console handler log format (colored)
class ColoredFormatter(logging.Formatter):
    """Custom formatter for colored console output."""
    
    # ANSI color codes
    GREY = "\x1b[38;21m"
    BLUE = "\x1b[38;5;39m"
    YELLOW = "\x1b[33;21m"
    RED = "\x1b[31;21m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: f"{GREY}{LOG_FORMAT}{RESET}",
        logging.INFO: f"{BLUE}%(levelname)s{RESET} - %(message)s",
        logging.WARNING: f"{YELLOW}{LOG_FORMAT}{RESET}",
        logging.ERROR: f"{RED}{LOG_FORMAT}{RESET}",
        logging.CRITICAL: f"{BOLD_RED}{LOG_FORMAT}{RESET}",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=LOG_DATE_FORMAT)
        return formatter.format(record)

# Console formatter
CONSOLE_FORMATTER = ColoredFormatter()

def get_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance.
    
    Args:
        name: Name of the logger (usually __name__)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Set log level
    if log_level:
        level = getattr(logging, log_level.upper(), logging.INFO)
    else:
        level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    logger.setLevel(level)
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    
    # Create file handler
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(FILE_FORMATTER)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Prevent logging from propagating to the root logger
    logger.propagate = False
    
    return logger

# Create root logger
logger = get_logger("ai_velocity")

def setup_logging():
    """Set up logging configuration."""
    # Configure root logger
    logging.basicConfig(
        level=settings.LOG_LEVEL.upper(),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(LOG_DIR / f"{datetime.now().strftime('%Y%m%d')}.log")
        ]
    )
    
    # Set log levels for third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("github").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
