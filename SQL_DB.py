import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Database credentials
username = "root"
password = "Krithiga@01"
host = "localhost"
database = "HotelReservation"

# Encode special characters in password
password_encoded = quote_plus(password)

# ✅ Use `pymysql` as the MySQL driver
engine = create_engine(f"mysql+pymysql://{username}:{password_encoded}@{host}/{database}")

# Read CSV file
df = pd.read_csv("Hotel Reservations (1).csv")

# ✅ Establish connection explicitly
with engine.connect() as connection:
    df.to_sql(name="booking", con=connection, if_exists="replace", index=False)
