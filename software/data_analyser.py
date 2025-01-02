import yaml
from os import path
import base64
import grpc
from datetime import datetime,timedelta
import time
from chirpstack_api import api
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


def load_config(filename: str, filepath:str) -> dict:
    """
    function to load and return config file in YAML format
    """
    with open(path.join(filepath, filename)) as file:
        return yaml.safe_load(file)

def fetch_data():
    """
    function to fetch device data from influxdb
    """
    url = config["url"]
    bucket = config["bucket"]
    org = config["org"]
    token = config["token"]
    field = "rain"

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    # Query script
    query_api = client.query_api()
    query = f'''from(bucket: "{bucket}")\
    |> range(start: -3m)\
    |> filter(fn:(r) => r._field == "{field}")'''
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    print(results)
    return results[0][1]

def send_downlink(msg: str):
    """
    Send a downlink message to the device
    """
    server = config["server"]
    dev_eui = config["dev_eui"]
    api_token = config["api_token"]
    port = 5
    payload = base64.b64decode(msg)

    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.DeviceServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueDeviceQueueItemRequest()
    req.queue_item.confirmed = True
    req.queue_item.data = payload
    req.queue_item.dev_eui = dev_eui
    req.queue_item.f_port = port

    resp = client.Enqueue(req, metadata=auth_token)

    # Print the downlink id
    print(resp.id)

def main():
    dt_start = datetime.now()
    critical_temp = 30.0
    min_misting_interval = 1 # in hour
    last_misting_time = dt_start

    while True:
        data = fetch_data()
        dt_now = datetime.now()
        if data > critical_temp and dt_now - timedelta(hours=1) >= last_misting_time:
            pass
            #send_downlink("CQ==")
            last_misting_time = dt_now
        time.sleep(9000)

if __name__ == "__main__":
    # loading config files
    config = load_config("keys.yaml",path.dirname(path.abspath(__file__)))
    main()


# Note:
# is there any other way to load keys safely,try .env file
# what difference can we expect in memory consuption and speed of execution, in loading yaml file as global variable and loading it as local in every function  
# do we need error handling for every function: not necessary
# once the springler operation is completed it should not turn ON for 1 hours period
# springler will works only for 3 min,this section is handled by actuator(coded in it) 
# send downlink when temperature is below 30c