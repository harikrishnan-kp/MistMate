import grpc
import api.device_pb2 as device_pb2
import api.device_pb2_grpc as device_pb2_grpc

# Replace with your ChirpStack gRPC server address and port
CHIRPSTACK_SERVER = "61.1.185.134:8080"

# Replace with your ChirpStack API token
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjaGlycHN0YWNrIiwiaXNzIjoiY2hpcnBzdGFjayIsInN1YiI6IjQ3YmIxN2UyLTkwNGEtNDYzMC1hZTc3LTA5YWFkNDgzYmMxMSIsInR5cCI6ImtleSJ9.ChvrrMXxSpimWMzZbtY7LAKQPp5Qcc25NsPZIdj4MX0"

# Replace with the Device EUI you want to fetch data for
DEVICE_EUI = "0d20c5322b918d0c"

def get_device_data(device_eui):
    # Create a channel to connect to the ChirpStack server
    channel = grpc.insecure_channel(CHIRPSTACK_SERVER)

    # Create a stub (client) for the DeviceService
    stub = device_pb2_grpc.DeviceServiceStub(channel)

    # Metadata for authentication
    metadata = [("authorization", f"Bearer {API_TOKEN}")]

    # Create the request
    request = device_pb2.GetDeviceRequest(dev_eui=device_eui)

    try:
        # Call the Get method to fetch device data
        response = stub.Get(request, metadata=metadata)

        # Process and print the response
        print("Device Data:")
        print(f"- Device EUI: {response.device.dev_eui}")
        print(f"- Name: {response.device.name}")
        print(f"- Description: {response.device.description}")
        print(f"- Application ID: {response.device.application_id}")

    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    get_device_data(DEVICE_EUI)
