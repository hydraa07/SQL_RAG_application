# SQL_RAG_application

Features

Easy Chat Interface: I used Streamlit to create a simple and user-friendly chat window.
Natural Language Questions: You can ask questions like "How many students are there?" instead of writing complicated code.
Connects to MySQL: The application connects directly to the MySQL database you provided.
Smart Answers: It uses LangChain and an AI model to figure out the user's question, write the correct SQL query, and then translate the database result back into plain English.

technology I Used
Python
LangChain 
Streamlit 
OpenAI for the AI model
MySQL for the database


Importing the Tools

import streamlit as st
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
streamlit: This is used to build the web page and the chat interface.

dotenv and os: These work together to load and read your secret API key and database password from the .env file.
sqlalchemy: This library helps Python connect to the MySQL database.
langchain libraries: These provide the "AI brains" for the application. They help connect the language model to the database.


Set Up the Application
Clone the repo: git clone <your-repo-url>
Go to the folder: cd <your-repo-name>
Create a virtual environment: python -m venv .venv and activate it.
Install packages: pip install -r requirements.txt
Add API Key: Create a .env file and add your OPENAI_API_KEY and database details.
Run it: streamlit run app.py
Setting Up the Connection
This section sets up the connection to your database and makes sure the API key is ready.

load_dotenv()

DB_USER = os.environ.get("DB_USER", "root")


db_uri = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_uri)
db = SQLDatabase(engine=engine)
load_dotenv(): This line executes the command to load the variables from your .env file.


Creating the AI 
This is the core logic of the application. Here, we create the AI "agent" that will do all the hard work.

llm = OpenAI(temperature=0, verbose=True, api_key=OPENAI_API_KEY)

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True
)
llm = OpenAI( ): This initializes the AI language model from OpenAI. temperature=0 makes the AI's answers more predictable and less random.

create_sql_agent( ): This is the most important function. It builds a specialized agent that:


