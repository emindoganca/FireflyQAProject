# Problem Definition

Given New York Taxi trips answer the questions below to identify each problematic data and
prepare the reporting queries for each item requested below;

	1. Write a sql query for each validation rule to find the records that are considered
	problematic.
		a. Rule 1: wrong gps readings within 10 seconds window. 
		b. Rule 2: Vehicles that has duplicate gps records.
		c. Rule 3: Invalid Start and End Datetimes.
		d. Rule 4: Using the coordinates given, detect the out-of-market vehicles 
		that are considered problematic.
		
	2. Do you think there are any other erroneous data conditions, please list them with your
	statements on why and prepare sql queries to detect them.

	3. Clear any erroneous data using the rules above to find out errors in that data.
		a. Write necessary test codes for each problematic data that you find in step 1 and
		execute them using the python API template (python bigQuery Client is a good
		starting point).(unit-tests,integration tests to maximize the test coverage)
		b. Using the same API code can you also answer the following questions;
			i. What are the most erroneous vehicles ?
			ii. What are the most erroneous routes ?
			
			
[Environment](https://console.cloud.google.com/bigquery?project=ml-workshop-195114&folder&organizationId&p=bigquery-public-data&d=new_york_taxi_trips&t=tlc_green_trips_2014&page=table)

# 1. Statements						

		a. Rule 1: A taxi can travel only 0.278 miles in 10 seconds if it travels 100 mph as max. speed.
		
			SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` where 1=1 AND DATETIME_DIFF(dropoff_datetime, pickup_datetime, second)=10 AND trip_distance>0.278 ORDER BY trip_distance DESC;
		
		b. Rule 2: This case has been cancelled because there is no unique value that defines the vehicle. 
		
		c. Rule 3: It is an invalid row if pickup_datetime greater than dropoff_datetime.
			
			SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE dropoff_datetime < pickup_datetime;
			
		d. Rule 4: 
		
		
		
		
# 2. Erroneous Data Conditions That I Detected;	


		Are there any trips with less than 1 passenger?
		
			```python 
			SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE passenger_count<1;
			```
		
		Are there any rows with the TOTAL_AMOUNT column less than 0? 
		
			```python
			SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE total_amount <0;
			```
			
		Rows with a fare_amount column greater than 0 even though the TRIP_DISTANCE=0;
		
			```python
			SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2014` WHERE trip_distance=0 AND fare_amount>0;
			```
			
			
# 3. a. Find and Clear Any Erroneous Data

	## Libraries for Writing API Codes: 
	
	```bash
		pip install fastapi
		pip install uvicorn
		pip install tabulate (as a table view in cmd)
	```	

	## Using BigQuery Client:

		Library:
		
		```bash
			pip install google-cloud-bigquery
		```	
		
		## Authentication Settings (Command Line):
		
		[Guide](https://cloud.google.com/bigquery/docs/reference/libraries#command-line)

		Service account creating;
			gcloud iam service-accounts create emindoganca

		Granting Permissions to the Service Account;
			gcloud projects add-iam-policy-binding spotlight-analytics-280723 --member="serviceAccount:emindoganca@spotlight-analytics-280723.iam.gserviceaccount.com" --role="roles/owner"
			
		Key File Generating;
			gcloud iam service-accounts keys create eminproject.json --iam-account=emindoganca@spotlight-analytics-280723.iam.gserviceaccount.com

		Environment Variable Settings
			set GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Emin\AppData\Local\Google\Cloud SDK\eminproject.json"

## 3. b.i. This case has been changed as "What are the most erroneous Hexagon?"

		[Guide](https://h3geo.org/docs/quickstart/)
		
		Library:
		
		```bash
			pip install h3
		```