import grpc
from chirpstack_api import api

# Configuration
server = "local host:8080"  # This should point to the ChirpStack API endpoint
dev_eui = "<add eui>"  # Replace with the DevEUI of your device
api_token = "<add key>"

   # Replace with your API token

def fetch_device_data():
    """Fetch device data from ChirpStack."""
    try:
        # Connect to ChirpStack without TLS
        channel = grpc.insecure_channel(server)
        
        # Device API client
        device_client = api.DeviceServiceStub(channel)
        
        # Define the API key meta-data
        auth_token = [("authorization", f"Bearer {api_token}")]
        
        # Construct request to get device information
        req = api.GetDeviceRequest(dev_eui=dev_eui)
        resp = device_client.Get(req, metadata=auth_token)
        
        # Print the fetched device data
        print("Device Data:", resp.device)
        return resp.device
    
    except grpc.RpcError as e:
        print(f"Failed to fetch device data: {e.details()}")
        return None

if __name__ == "__main__":
    fetch_device_data()
