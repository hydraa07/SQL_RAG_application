import streamlit as st
from sqlalchemy import create_engine
import os

from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from dotenv import load_dotenv

# --- Configuration ---
# For a robust solution, use environment variables for credentials.
# Set these in your operating system or a .env file.
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "12345")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "school_db")
OPENAI_API_KEY = os.environ.get("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")

# Check if the OpenAI API key is set
if not OPENAI_API_KEY:
    st.error("OpenAI API key is not set! Please set the OPENAI_API_KEY environment variable.")
    st.stop()
    
# --- Database Connection ---
try:
    # Create the database connection string
    db_uri = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Create the SQLAlchemy engine
    engine = create_engine(db_uri)
    
    # Instantiate the LangChain SQLDatabase
    db = SQLDatabase(engine=engine)

except Exception as e:
    st.error(f"Failed to connect to the database. Please check your credentials and that the database server is running. Error: {e}")
    st.stop()

# --- LLM and Agent Initialization ---
# Initialize the language model
llm = OpenAI(temperature=0, verbose=True, api_key=OPENAI_API_KEY)

# Create the SQL Agent
# This agent is equipped with tools to interact with the SQL database.
agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True
)

# --- Streamlit Chat UI ---
st.title("School Database Chatbot 🏫")
st.write("Ask me anything about the students, classes, marks, or scholarships!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input from chat box
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response while generating
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Invoke the agent to get the response
                response = agent_executor.invoke({"input": prompt})
                response_content = response["output"]
            except Exception as e:
                response_content = f"Sorry, I encountered an error: {e}"
            
            st.markdown(response_content)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})