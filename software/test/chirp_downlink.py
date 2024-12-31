import grpc
from chirpstack_api import api


# Configuration
server = "local host:8080"  # This should point to the ChirpStack API endpoint
dev_eui = "<add eui>"  # Replace with the DevEUI of your device
api_token = "<add key>"


def send_downlink():
    """Send a downlink message to the device."""
    try:
        # Connect to ChirpStack without TLS
        channel = grpc.insecure_channel(server)
        
        # Device queue API client
        client = api.DeviceQueueServiceStub(channel)
        
        # Define the API key meta-data
        auth_token = [("authorization", f"Bearer {api_token}")]
        
        # Construct the downlink request
        req = api.EnqueueDeviceQueueItemRequest()
        req.queue_item.confirmed = False
        req.queue_item.data = bytes([0x01, 0x02, 0x03])  # Replace with your payload
        req.queue_item.dev_eui = dev_eui
        req.queue_item.f_port = 10  # Replace with the appropriate FPort
        
        # Send the downlink
        resp = client.Enqueue(req, metadata=auth_token)
        
        # Print the downlink ID
        print("Downlink ID:", resp.id)
    
    except grpc.RpcError as e:
        print(f"Failed to send downlink: {e.details()}")

if __name__ == "__main__":
    #fetch_device_data()
    send_downlink()


# note
# script to send a dowlink to endnode using chirpstack api and gRPC"
# chirpstackv4 allows sending dowlink data as hex,BASE64 and JASON