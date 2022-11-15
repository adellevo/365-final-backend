import sqlalchemy
import urllib.parse

# Connection Parameters (you will sub in with your own databases values)
escapedPassword = urllib.parse.quote_plus("adelle123")
sqldialect = "mysql+pymysql"
username = "root"
database = "class_365"
host = "localhost"

# Build the connection string based on database specific parameters
connectionString = f"{sqldialect}://{username}:{escapedPassword}@{host}/{database}"

# Create a new DB engine based on our connection string
engine = sqlalchemy.create_engine(connectionString)

# Create a single connection to the database. Later we will discuss pooling connections.
conn = engine.connect()

# The sql we want to execute
sql = """
SHOW tables;
"""

# Run the sql and returns a CursorResult object which represents the SQL results
result = conn.execute(sqlalchemy.text(sql))

# Iterate over the CursorResult object row by row and just print.
# In a real application you would access the fields directly.
for row in result:
    print(row)