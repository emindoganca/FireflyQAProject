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

def get_h3(lat, lon, res):
    return h3.geo_to_h3(lat, lon, res)

def run_query(query):
    job = client.query(query)
    output=[]
    for row in job:
        lat = row["pickup_latitude"]
        lon = row["pickup_longitude"]
        hex = get_h3(lat, lon, 9) #Burada seyahatin başlangıç koordinatının 9 resolution'a göre hangi hexagona denk geldiği bulunur. 
        output.append([row["pickup_datetime"], row["dropoff_datetime"], row["passenger_count"], row["trip_distance"], row["total_amount"], hex]) #Sonuç çıktısında tüm kolonları getirmek yerine sadece önemli bir kaç alan ve hex=hexagon kodu getirilmiştir.
    return output

@router.get("/test-case-1a")
def test_case_1a():
    case1a_query = "SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` where 1=1 AND DATETIME_DIFF(dropoff_datetime, pickup_datetime, second)=10 AND trip_distance>0.278 ORDER BY trip_distance DESC;"
    return run_query(case1a_query) #Test_case_1_a

@router.get("/test-case-1c")
def test_case_1c():
    case1c_query = "SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE dropoff_datetime < pickup_datetime;"
    return run_query(case1c_query) #Test_case_1_c


#aşağıdaki iki function'da 3. case'de istenen temizleme işlemi yapılır. Daha sonra kontrol amacıyla tekrar test_Case_1_a sorgusu çalıştırılır.
#Duplicate row hatası dışında DB'deki herhangi bir kaydı delete ederek temizlemek en doğru çözüm değil gibi ancak case'de istendiği için yazdım.
#(GCP'de faturalamayı açmadığım için delete işlemi yapılmıyor sanırım çok üzerinde duramadım.)
@router.get("/test-case-1a-clear")
def test_case_1a_clear():
    case1a_query = "DELETE FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` where 1=1 AND DATETIME_DIFF(dropoff_datetime, pickup_datetime, second)=10 AND trip_distance>0.278 ORDER BY trip_distance DESC;"
    client.query(case1a_query)
    return test_case_1a()

@router.get("/test-case-1c-clear")
def test_case_1c_clear():
    case1c_query="DELETE FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE dropoff_datetime < pickup_datetime;"
    client.query(case1c_query)
    return test_case_1c() #Get test_case_1c after delete process.

app = create_app()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
