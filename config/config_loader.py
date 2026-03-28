import os
from dotenv import load_dotenv


class Config:
    """Configuration class holding all environment variables."""

    def __init__(self):
        self.QWEN_API_KEY: str = os.getenv('QWEN_API_KEY', '')
        self.GMAIL_CLIENT_ID: str = os.getenv('GMAIL_CLIENT_ID', '')
        self.GMAIL_CLIENT_SECRET: str = os.getenv('GMAIL_CLIENT_SECRET', '')
        self.GMAIL_REFRESH_TOKEN: str = os.getenv('GMAIL_REFRESH_TOKEN', '')
        self.WHATSAPP_SESSION_PATH: str = os.getenv('WHATSAPP_SESSION_PATH', './whatsapp_session.json')
        self.LINKEDIN_ACCESS_TOKEN: str = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        self.LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')


def load_config() -> Config:
    """
    Load environment variables from .env file and validate required variables.

    Returns:
        Config: Instance of Config class with loaded environment variables

    Raises:
        ValueError: If required environment variables are missing
    """
    # Load environment variables from .env file
    load_dotenv()

    config = Config()

    # List of required environment variables
    required_vars = [
        'QWEN_API_KEY',
    ]

    # Check for missing required variables
    missing_vars = []
    for var_name in required_vars:
        var_value = getattr(config, var_name)
        if not var_value:
            missing_vars.append(var_name)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return config


def load_config_dict() -> dict:
    """
    Load configuration as a dictionary (for compatibility with older code).

    Returns:
        Dictionary containing configuration values
    """
    load_dotenv()

    config_dict = {
        'qwen_api_key': os.getenv('QWEN_API_KEY', ''),
        'linkedin_email': os.getenv('LINKEDIN_EMAIL', ''),
        'linkedin_password': os.getenv('LINKEDIN_PASSWORD', ''),
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    }

    return config_dict