# DB Chat - Natural Language Database Query Tool

DB Chat is a powerful tool that allows you to query your databases using natural language instead of SQL. It supports multiple database types and provides data visualization capabilities.

## Features

- **Multiple Database Support**: Connect to SQLite, PostgreSQL, Microsoft SQL Server, and MySQL databases.
- **Natural Language Queries**: Ask questions about your data in plain English.
- **AI-Powered SQL Generation**: Leverages AI models from Anthropic, OpenAI, Ollama, or OpenRouter to convert natural language to SQL.
- **Schema Visualization**: View your database schema as an ER diagram.
- **Interactive Data Visualization**: Create various charts and graphs from your query results.
- **Table Browser**: Explore your database tables and preview their contents.

## Requirements

- Python 3.8 or higher
- Required Python packages (see `requirements.txt`)
- Access to at least one of the supported AI models:
  - Anthropic Claude API key
  - OpenAI API key
  - Google Gemini API key
  - Ollama running locally
  - OpenRouter API key

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/db-chat.git
   cd db-chat
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file for your API keys and defaults (optional):
   ```bash
   # AI API keys
   ANTHROPIC_API_KEY=your_anthropic_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPENROUTER_API_KEY=your_openrouter_api_key
   GEMINI_API_KEY=your_gemini_api_key
   
   # Ollama settings
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   
   # Default database connection settings
   DEFAULT_PG_HOST=localhost
   DEFAULT_PG_PORT=5432
   DEFAULT_PG_DB=your_default_db
   DEFAULT_PG_USER=your_default_user
   
   # Ollama settings
   OLLAMA_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   ```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501).

3. Use the sidebar to connect to your database.

4. Once connected, you can:
   - Query your database using natural language
   - Browse tables and preview data
   - Create visualizations from query results

## Using Ollama (Local LLM)

If you want to use Ollama (a local LLM) instead of cloud APIs:

1. Install Ollama from [https://ollama.ai/](https://ollama.ai/)

2. Start the Ollama service:
   ```bash
   ollama serve
   ```

3. Set the Ollama URL in your `.env` file (required):
   ```
   OLLAMA_URL=http://localhost:11434
   ```
   Note: If running Ollama on a different machine, use that machine's IP or hostname.

4. Pull a compatible model:
   ```bash
   ollama pull llama3
   ```

5. Select "Ollama (Local)" in the AI provider dropdown in the application

## How It Works

1. **Database Connection**: The application connects to your database and analyzes its schema.

2. **Natural Language Processing**: When you enter a query in natural language, the application sends it to the selected AI model along with the database schema.

3. **SQL Generation**: The AI model generates the appropriate SQL query based on your natural language request.

4. **Query Execution**: The generated SQL query is executed against your database, and the results are displayed.

5. **Visualization**: You can visualize the query results using various chart types.

## Project Structure

```
project/
├── app.py               # Main Streamlit application
├── requirements.txt     # Dependencies
├── utils/
│   ├── db_connector.py  # Database connection handlers
│   ├── schema_parser.py # For understanding database schema
│   └── ai_interface.py  # Interface with AI models
├── components/
│   ├── db_connection.py # UI components for db connection
│   ├── query_interface.py # Natural language query interface
│   └── visualization.py # Data visualization components
└── config.py           # Configuration and settings
```

## AI Provider Support

- **Anthropic Claude**: High-quality natural language understanding with the Claude API
- **OpenAI**: Powerful language models with GPT-4
- **Google Gemini 2.0 Flash**: Google's advanced language model with the Gemini API
- **Ollama**: Local large language models for privacy and offline use
- **OpenRouter**: Access to various language models through a single API

## Troubleshooting

- **Database Connection Issues**: Make sure you have the correct host, port, username, and password.
- **SQL Generation Errors**: Try rephrasing your query to be more specific.
- **API Key Issues**: Check that you've entered the correct API keys in the application or .env file.
- **Ollama Connection**: Ensure the Ollama service is running locally at the default port.

## License

This project is licensed under the MIT License - see the LICENSE file for details.