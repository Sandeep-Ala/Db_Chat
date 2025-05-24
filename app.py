"""
Main Streamlit application for natural language database querying.
"""
import streamlit as st
import os
import logging
import sys
import importlib
from typing import Dict, Any

# Setup dependency checking
def check_dependencies() -> Dict[str, bool]:
    """Check if all required dependencies are installed."""
    dependencies = {
        "streamlit": True,  # We're already running in Streamlit
        "sqlalchemy": False,
        "anthropic": False,
        "openai": False,
        "google.generativeai": False,
        "pandas": False,
        "plotly": False,
        "dotenv": False
    }
    
    for package in dependencies.keys():
        if package == "streamlit":
            continue
        try:
            importlib.import_module(package)
            dependencies[package] = True
        except ImportError:
            dependencies[package] = False
    
    return dependencies

# Import our modules if dependencies are available
dependencies = check_dependencies()

if all(v for k, v in dependencies.items() if k in ["sqlalchemy", "pandas", "plotly"]):
    from utils.db_connector import DatabaseConnector
    from utils.schema_parser import SchemaParser
    from components.db_connection import render_db_connection_ui
    from components.query_interface import render_query_interface, render_table_browser
    from components.visualization import render_visualization_interface
else:
    # We'll define these as None to prevent errors
    DatabaseConnector = None
    SchemaParser = None
    render_db_connection_ui = None
    render_query_interface = None
    render_table_browser = None
    render_visualization_interface = None

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="DB Chat - Natural Language Database Query Tool",
    page_icon="🗄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "db_connector" not in st.session_state:
    st.session_state.db_connector = None

if "schema_parser" not in st.session_state:
    st.session_state.schema_parser = None

if "connected" not in st.session_state:
    st.session_state.connected = False

def main():
    """Main application function"""
    # Check dependencies first
    dependencies = check_dependencies()
    missing_core = not all(dependencies[pkg] for pkg in ["sqlalchemy", "pandas", "plotly"])
    
    if missing_core:
        st.title("DB Chat - Installation Required")
        st.error("Some required packages are missing. Please install them to use DB Chat.")
        
        st.subheader("Missing Dependencies:")
        for pkg, installed in dependencies.items():
            if not installed:
                st.write(f"❌ {pkg}")
            else:
                st.write(f"✅ {pkg}")
        
        st.subheader("Installation Instructions")
        st.code("""
# Option 1: Install all dependencies (may require C++ compiler for Ollama support)
pip install -r requirements.txt

# Option 2: Install simplified version without Ollama support
pip install -r requirements-simplified.txt
        """)
        
        st.info("If you're having issues with the installation, particularly with `llama-cpp-python`, try the simplified version.")
        
        return
    
    # Sidebar
    with st.sidebar:
        st.title("DB Chat 🗄️💬")
        st.write("Query your databases with natural language")
        
        # Database connection section
        st.header("1. Connect to Database")
        
        # Reconnect button if already connected
        if st.session_state.get("connected", False):
            st.success("Connected to database")
            db_info = st.session_state.db_connector.db_type.capitalize()
            st.write(f"Type: {db_info}")
            
            if st.button("Disconnect"):
                # Close the connection and reset session state
                if st.session_state.db_connector:
                    st.session_state.db_connector.close()
                
                st.session_state.db_connector = None
                st.session_state.schema_parser = None
                st.session_state.connected = False
                
                # Rerun the app to reflect changes
                st.rerun()
            
            if st.button("Reconnect"):
                # Reset session state but don't close
                st.session_state.connected = False
                st.rerun()
        else:
            # Show connection UI if not connected
            db_connector = render_db_connection_ui()
            
            if db_connector and db_connector.connected:
                # Store the connector in session state
                st.session_state.db_connector = db_connector
                
                # Get schema information
                schema_info = db_connector.get_schema()
                
                if "error" not in schema_info:
                    # Parse the schema
                    schema_parser = SchemaParser(schema_info)
                    st.session_state.schema_parser = schema_parser
                    st.session_state.connected = True
                    
                    # Rerun the app to reflect connection
                    st.rerun()
                else:
                    st.error(f"Error retrieving schema: {schema_info['error']}")
        
        # Navigation when connected
        if st.session_state.get("connected", False):
            st.header("2. Choose Mode")
            app_mode = st.radio(
                "Select Mode",
                ["Query Database", "Table Browser", "Data Visualization"]
            )
            st.session_state.app_mode = app_mode
            
            # API key storage section
            with st.expander("API Key Settings"):
                st.write("Store your API keys for AI providers")
                
                # Check if AI packages are available
                ai_available = {
                    "anthropic": dependencies.get("anthropic", False),
                    "openai": dependencies.get("openai", False),
                    "gemini": dependencies.get("google.generativeai", False)
                }
                
                if not any(ai_available.values()):
                    st.warning("No AI provider packages detected. Install at least one to use natural language queries.")
                
                if ai_available.get("anthropic", False):
                    anthropic_key = st.text_input(
                        "Anthropic API Key",
                        type="password",
                        value=st.session_state.get("anthropic_api_key", ""),
                        key="anthropic_api_key_sidebar"
                    )
                    st.session_state["anthropic_api_key"] = anthropic_key
                else:
                    st.info("Anthropic package not installed. Install with: pip install anthropic")
                
                if ai_available.get("openai", False):
                    openai_key = st.text_input(
                        "OpenAI API Key",
                        type="password",
                        value=st.session_state.get("openai_api_key", ""),
                        key="openai_api_key_sidebar"
                    )
                    st.session_state["openai_api_key"] = openai_key
                else:
                    st.info("OpenAI package not installed. Install with: pip install openai")
                
                if ai_available.get("gemini", False):
                    gemini_key = st.text_input(
                        "Google Gemini API Key",
                        type="password",
                        value=st.session_state.get("gemini_api_key", ""),
                        key="gemini_api_key_sidebar"
                    )
                    st.session_state["gemini_api_key"] = gemini_key
                else:
                    st.info("Google Gemini package not installed. Install with: pip install google-generativeai")
                
                # OpenRouter is optional
                openrouter_key = st.text_input(
                    "OpenRouter API Key (Optional)",
                    type="password",
                    value=st.session_state.get("openrouter_api_key", ""),
                    key="openrouter_api_key_sidebar"
                )
                st.session_state["openrouter_api_key"] = openrouter_key
                
                st.write("Note: Ollama doesn't require an API key")
        
        # About section
        with st.expander("About"):
            st.write("""
            **DB Chat** is a natural language database query tool that allows you to:
            - Connect to various database types
            - Query your database using plain English
            - Visualize your data with interactive charts
            
            Built with Streamlit and AI.
            """)
    
    # Main content area
    if not st.session_state.get("connected", False):
        # Welcome screen when not connected
        st.title("Welcome to DB Chat 🗄️💬")
        st.write("Connect to your database to get started.")
        
        st.info("Please use the sidebar to connect to a database first.")
        
        # Feature highlights
        st.subheader("Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("### 🔌 Multiple Databases")
            st.write("Connect to SQLite, PostgreSQL, MS SQL Server, and MySQL.")
        
        with col2:
            st.write("### 💬 Natural Language")
            st.write("Query your data using plain English instead of SQL.")
        
        with col3:
            st.write("### 📊 Visualizations")
            st.write("Create charts and graphs from your query results.")
        
        # How it works
        st.subheader("How it works")
        st.write("""
        1. Connect to your database using the sidebar
        2. DB Chat analyzes your database schema
        3. Ask questions about your data in plain English
        4. Get results instantly with the option to visualize
        """)
    else:
        # Show the selected mode when connected
        app_mode = st.session_state.get("app_mode", "Query Database")
        
        if app_mode == "Query Database":
            render_query_interface(st.session_state.db_connector, st.session_state.schema_parser)
        elif app_mode == "Table Browser":
            render_table_browser(st.session_state.db_connector, st.session_state.schema_parser)
        elif app_mode == "Data Visualization":
            render_visualization_interface(st.session_state.db_connector, st.session_state.schema_parser)

if __name__ == "__main__":
    main()