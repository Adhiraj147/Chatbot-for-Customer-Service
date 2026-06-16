import logging
import os
from datetime import datetime

def setup_logger():
    """
    Sets up a configured logger for the application.
    Writes logs to the 'logs' directory and outputs to console.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = datetime.now().strftime("%Y-%m-%d") + "_chatbot.log"
    log_filepath = os.path.join(log_dir, log_filename)

    logger = logging.getLogger("ChatbotLogger")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()

def format_error(message: str) -> dict:
    """
    Formats standard error responses for the API.
    """
    return {"error": True, "message": message}
