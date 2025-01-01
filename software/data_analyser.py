import yaml
from os import path
import base64
import grpc
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
    |> range(start: -16m)\
    |> filter(fn:(r) => r._field == "{field}")'''
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    print(results)

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
    pass   
    #fetch_data()
    send_downlink("CQ==")


if __name__ == "__main__":
    # loading config files
    config = load_config("keys.yaml",path.dirname(path.abspath(__file__)))
    main()


# Note:
# is there any other way to load keys safely,try .env file
# what difference can we expect in memory consuption and speed of execution, if we load yaml file as global variable and load it as local in every function  
# do we need error handling for every function
# include a argument "data to be send" in downlink function
# once the springler operation is completed it should not turn ON for 1 hours period
# springler will works only for 3 min,this section is handled by actuator(coded in it) 
# send downlink when temperature is below 30c