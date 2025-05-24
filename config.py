"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# AI API configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Default AI provider
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "anthropic")

# Database connection defaults
DEFAULT_SQLITE_PATH = os.getenv("DEFAULT_SQLITE_PATH", "")
DEFAULT_PG_HOST = os.getenv("DEFAULT_PG_HOST", "localhost")
DEFAULT_PG_PORT = os.getenv("DEFAULT_PG_PORT", "5432")
DEFAULT_PG_DB = os.getenv("DEFAULT_PG_DB", "")
DEFAULT_PG_USER = os.getenv("DEFAULT_PG_USER", "")

DEFAULT_MSSQL_HOST = os.getenv("DEFAULT_MSSQL_HOST", "localhost")
DEFAULT_MSSQL_PORT = os.getenv("DEFAULT_MSSQL_PORT", "1433")
DEFAULT_MSSQL_DB = os.getenv("DEFAULT_MSSQL_DB", "")
DEFAULT_MSSQL_USER = os.getenv("DEFAULT_MSSQL_USER", "")

DEFAULT_MYSQL_HOST = os.getenv("DEFAULT_MYSQL_HOST", "localhost")
DEFAULT_MYSQL_PORT = os.getenv("DEFAULT_MYSQL_PORT", "3306")
DEFAULT_MYSQL_DB = os.getenv("DEFAULT_MYSQL_DB", "")
DEFAULT_MYSQL_USER = os.getenv("DEFAULT_MYSQL_USER", "")

# Ollama settings
OLLAMA_URL = os.getenv("OLLAMA_URL")  # No default, must be provided in .env
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Application settings
MAX_ROWS_PREVIEW = int(os.getenv("MAX_ROWS_PREVIEW", "10"))
MAX_ROWS_EXPORT = int(os.getenv("MAX_ROWS_EXPORT", "10000"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")