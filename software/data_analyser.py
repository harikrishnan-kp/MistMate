import yaml
from os import path
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
    |> range(start: -10m)\
    |> filter(fn:(r) => r._field == "{field}")'''
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
    print(results)

def send_downlink():
    """
    Send a downlink message to the device
    """
    server = config["server"]
    dev_eui = config["dev_eui"]
    api_token = config["api_token"]

    try:
                # Connect without using TLS.
        channel = grpc.insecure_channel(server)

        # Device-queue API client.
        client = api.DeviceServiceStub(channel)

        # Define the API key meta-data.
        auth_token = [("authorization", "Bearer %s" % api_token)]

        # Construct request.
        req = api.EnqueueDeviceQueueItemRequest()
        req.queue_item.confirmed = False
        req.queue_item.data = bytes([0x01, 0x02, 0x03])
        req.queue_item.dev_eui = dev_eui
        req.queue_item.f_port = 10

        resp = client.Enqueue(req, metadata=auth_token)

        # Print the downlink id
        print(resp.id)
    
    except grpc.RpcError as e:
        print(f"Failed to send downlink: {e.details()}")

if __name__ == "__main__":
    # loading config files
    config = load_config("keys.yaml",path.dirname(path.abspath(__file__)))
    #fetch_data()
    send_downlink()


# Note:
# is there any other way to load keys safely
# do we need error handling for every function
# include a argument "data to be send" in downlink function
# once the springler operation is completed it should not turn ON for 1 hours period
# springler will works only for 3 min,this section is handled by actuator(coded in it) 