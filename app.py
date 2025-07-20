import os
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import create_sql_query_chain
from langchain_google_genai import GoogleGenerativeAI
import langchain_experimental.sql as sql
from langchain.chains import SQLDatabaseChain


# Load environment variables
load_dotenv()

# Database connection parameters
db_user = "root"
db_password = "12345"
db_host = "localhost"
db_name = "school_db"

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# Initialize SQLDatabase
db = SQLDatabase(engine)

# Initialize LLM
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=os.environ["GOOGLE_API_KEY"])

# Create SQL query chain and quwry
chain = create_sql_query_chain(llm, db)


def execute_query(question):
    try:
        response = chain.invoke({"question": question})

        # Clean the response 
        cleaned_query = response.strip("```sql\n").strip("\n```")

        # Run the SQL query
        result = db.run(cleaned_query)

        return cleaned_query, result

    except ProgrammingError as e:
        st.error(f"SQL Error: {e}")
        return None, None
    except Exception as e:
        st.error(f"Unexpected Error: {e}")
        return None, None

st.title("Natural Language to SQL Query App")

question = st.text_input("Ask your question about the database:")

if st.button("Execute"):
    if question:
        query, result = execute_query(question)
        if query and result is not None:
            st.subheader("Generated SQL Query")
            st.code(query, language="sql")

            st.subheader("Query Result")
            st.write(result)
        else:
            st.warning("No result returned or an error occurred.")
    else:
        st.warning("Please enter a question.")
