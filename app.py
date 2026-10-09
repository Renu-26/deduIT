import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.title("User Engagement Dashboard")

# Connect to SQLite
connection = sqlite3.connect(r"C:\Users\ray\Desktop\Data\practice.db")

# SQL query
query1 = """
SELECT
    CASE
        WHEN substr(time, instr(time, ',') + 2)
             BETWEEN '00:00:00' AND '06:00:00'
            THEN '12 AM - 6 AM'

        WHEN substr(time, instr(time, ',') + 2)
             BETWEEN '06:00:01' AND '12:00:00'
            THEN '6 AM - 12 PM'

        WHEN substr(time, instr(time, ',') + 2)
             BETWEEN '12:00:01' AND '18:00:00'
            THEN '12 PM - 6 PM'

        WHEN substr(time, instr(time, ',') + 2)
             BETWEEN '18:00:01' AND '23:59:59'
            THEN '6 PM - 12 AM'
    END AS time_range,

    COUNT(*) AS total

FROM logs_BLFOM_for_analysis lbfa
GROUP BY time_range
ORDER BY total DESC;
"""

# Run query
df = pd.read_sql_query(query1, connection)

# Show data
st.subheader("Engagement by Time of Day")
st.dataframe(df)

# Bar chart
st.bar_chart(
    df.set_index("time_range")["total"]
)


query2 = """ SELECT
    lbfa."User full name",
    COUNT(*) AS total_activity
FROM logs_BLFOM_for_analysis lbfa
GROUP BY lbfa."User full name"
ORDER BY total_activity DESC;
"""
# Run query
df = pd.read_sql_query(query2, connection)

# Show data
st.subheader("Activity of users")
st.dataframe(df)

# Bar chart
st.bar_chart(
    df.set_index("User full name")["total_activity"]
)

connection.close()