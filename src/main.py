import uvicorn
from fastapi import FastAPI, APIRouter
import datetime
from google.cloud import bigquery
from tabulate import tabulate
import h3

router = APIRouter()
client = bigquery.Client()

def create_app():
    app = FastAPI(
	title="Test API",
	description="Test API descriptiom",
	version="0.1.0",
	openapi_url="/openapi.json",
	docs_url="/",
	redoc_url="/redoc",
    )
    app.include_router(router, prefix="/hello", tags=["hello"])
    return app
"""
@router.get("/world")
def hello_world():
    data = f"{datetime.datetime.now()} : Hello World"
    return data
"""
def run_query(query):
    job = client.query(query)
    output=[]
    for row in job:
        lat = row["pickup_latitude"]
        lon = row["pickup_longitude"]
        hex = get_h3(lat, lon, 9)
        output.append([row["pickup_datetime"], row["dropoff_datetime"], row["passenger_count"], row["trip_distance"], row["total_amount"], hex])
    return output

def get_h3(lat, lon, res):
    return h3.geo_to_h3(lat, lon, res)

@router.get("/test-case-1a")
def test_case_1a():
    case1a_query = "SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` where 1=1 AND DATETIME_DIFF(dropoff_datetime, pickup_datetime, second)=10 AND trip_distance>0.278 ORDER BY trip_distance DESC;"
    return run_query(case1a_query)

@router.get("/test-case-1c")
def test_case_1c():
    case1c_query = "SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE dropoff_datetime < pickup_datetime;"
    return run_query(case1c_query)

@router.get("/test-case-1a-clear")
def test_case_1a_clear():
    case1a_query = "delete from `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` where 1=1 AND DATETIME_DIFF(dropoff_datetime, pickup_datetime, second)=10 AND trip_distance>0.278 ORDER BY trip_distance DESC;"
    client.query(case1a_query)
    return test_case_1a()



app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
