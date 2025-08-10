import os
import re
from decouple import config
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain

# Load DB connection from env or fallback
DB_URI = os.getenv("DB_URI", "postgresql+psycopg2://postgres:postgres@db:5432/postgres")
OPENAI_API_KEY = config("OPENAI_API_KEY")

# Setup once
db = SQLDatabase.from_uri(DB_URI)
llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=OPENAI_API_KEY)

def can_generate_sql(prompt: str) -> bool:
    try:
        sql_chain = create_sql_query_chain(llm, db)
        result = sql_chain.invoke({"question": prompt})

        raw_query  = result["result"]

        cleaned_query = clean_sql_query(raw_query)
        # output = db.run(cleaned_query)
        # print(output)
        schema = db.get_usable_table_names()
        if any(table.lower() in cleaned_query.lower() for table in schema):
            return True
        else:
            print("No known tables referenced in query.")
            return False

    except Exception as e:
        print(f"SQL generation failed: {e}")
        return False

def run_sql_chain(prompt: str):
    try:
        sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        result = sql_chain.invoke({"query": prompt})
        return result["result"]
    except Exception as e:
        print(f"SQL Chain failed: {e}")
        return None

def clean_sql_query(sql_text):
    cleaned = re.sub(r"```sql|```", "", sql_text).strip()
    return cleaned