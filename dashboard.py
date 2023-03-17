import os
import streamlit as st
from pandas import DataFrame
import pymongo
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('USERNAMES')
password = os.getenv('PASSWORD')
database= os.getenv('DATABASE')
collection = os.getenv('COLLECTION')

print(username, password, database, collection)


myclient = pymongo.MongoClient(
    "mongodb://localhost:27018/", username=username, password=password)
my_db = myclient[database]
my_collection = my_db[collection]

cust_id = st.sidebar.text_input("CustomerID:")

if cust_id:

    myquery = {"CustomerID": cust_id}
    mydoc = my_collection.find(myquery, {"_id": 0, "StockCode": 0,
                       "Description": 0, "Quantity": 0, "Country": 0, "UnitPrice": 0})
    df = DataFrame(mydoc)
    df.drop_duplicates(subset="InvoiceNo", keep='first', inplace=True)
    st.header("Output Customer Invoices")
    table2 = st.dataframe(data=df)

inv_no = st.sidebar.text_input("InvoiceNo:")
if inv_no:

    myquery = {"InvoiceNo": inv_no}
    mydoc = my_collection.find(
        myquery, {"_id": 0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0})
    df = DataFrame(mydoc)
    reindexed = df.reindex(sorted(df.columns), axis=1)
    st.header("Output by Invoice ID")
    table2 = st.dataframe(data=reindexed)
