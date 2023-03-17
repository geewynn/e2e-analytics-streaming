from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel
from datetime import datetime
from kafka import KafkaProducer
import uvicorn


class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    Country: str


# This is important for general execution and the docker later
app = FastAPI()

# Base URL


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/invoiceitem")
# body awaits a json with invoice item information
async def post_invoice_item(item: InvoiceItem):
    print("Message received")
    try:
        date = datetime.strptime(item.InvoiceDate, "%d/%m/%Y %H:%M")

        print('Found a timestamp: ', date)
        item.InvoiceDate = date.strftime("%d-%m-%Y %H:%M:%S")
        print("New item date:", item.InvoiceDate)

        # Parse item back to json
        json_of_item = jsonable_encoder(item)

        # Dump the json out as string
        json_as_string = json.dumps(json_of_item)

        # Produce the string
        produce_kafka_string(json_as_string)

        # Encode the created customer item if successful into a JSON and return it to the client with 201
        return JSONResponse(content=json_of_item, status_code=201)
    except ValueError:
        return JSONResponse(content=jsonable_encoder(item), status_code=400)


def produce_kafka_string(json_as_string):
    # Create producer
    producer = KafkaProducer(bootstrap_servers='kafka:9092', acks=1)

    # Write the string as bytes because Kafka needs it this way
    producer.send('ingestion-topic', bytes(json_as_string, 'utf-8'))
    producer.flush()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8085, reload=True)
