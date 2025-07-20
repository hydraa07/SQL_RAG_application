# SQL_RAG_application

 Features
Easy Chat Interface: Built with Streamlit for a clean and interactive experience.
MySQL Connectivity: Connects directly to your school_db MySQL database.
Smart Query Generation: Uses LangChain + Google Gemini Pro to convert natural language into SQL and return meaningful answers.

Technologies
Python
Streamlit – For frontend UI
LangChain – For chaining and query conversion
Google Gemini Pro – As the Large Language Model (LLM)
SQLAlchemy + PyMySQL – For MySQL database connectivity
dotenv – To manage API keys securely

Required Imports (from your code)
python
Copy
Edit
import os
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import create_sql_query_chain
from langchain_google_genai import GoogleGenerativeAI
What They Do:
streamlit: Creates the web interface.
dotenv + os: Load your secret credentials from .env.
sqlalchemy: Connects Python to MySQL.
langchain_experimental.sql: Contains the chain to generate SQL queries.
GoogleGenerativeAI: Integrates Gemini Pro as the AI brain.

Create a Virtual Environment

python -m venv venv
venv\Scripts\activate  # On Windows


pip install -r requirements.txt


Set Up Environment Variables
Create a .env file in the root folder:

GOOGLE_API_KEY="mykey"



# Database connection details
db_user = "root"
db_password = "12345"
db_host = "localhost"
db_name = "school_db"


# SQLAlchemy connection
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
db = SQLDatabase(engine)
This connects your Python app to a MySQL database using SQLAlchemy and wraps it with LangChain’s SQLDatabase utility.

Creating the AI Logic
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ["GOOGLE_API_KEY"])
chain = create_sql_query_chain(llm, db)
GoogleGenerativeAI: Loads Gemini Pro with your API key.


Final Flow Summary

response = chain.invoke({"question": question})
cleaned_query = response.strip("```sql\n").strip("\n```")
result = db.run(cleaned_query)



Flow in plain English:
invoke() → Ask Gemini Pro to generate SQL
strip() → Clean the result so it’s ready to execute
db.run() → Run the query and get the data

then return query and query result
