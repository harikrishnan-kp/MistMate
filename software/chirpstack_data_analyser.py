import paho.mqtt.client as mqtt
import json
import grpc
import base64
from datetime import datetime, timedelta, timezone
from chirpstack_api import api

# Documentation for the global variables
# The MQTT broker address
broker_address = ""
# The username for the MQTT broker
username = ""
# The password for the MQTT broker
password = ""
# The topic to subscribe to
topic = "application/application-id/device/+/event/up/"
# Initial status variable
status = 0
# The start time for the elapsed time check
start_time = datetime.now(timezone.utc) - timedelta(hours=1)

# Documentation for the external URL for the ChirpStack API
# The ChirpStack API URL
chirpstack_url = ""
# The API token for the ChirpStack API
api_token = ""

# Documentation for the base64-encoded downlink data
# The base64-encoded downlink data
downlink_b64_data = "CQ=="
# The decoded payload from the base64-encoded data
payload = base64.b64decode(downlink_b64_data)

# The End Device EUI
end_device_EUI = ""

# The Temperature Device EUI
temperature_device_EUI = ""

# Critical Temperature
critical_temperature = 30.0

# Documentation for the helper function that checks if the elapsed time is greater than 1 hour
def time_status(start_time):
    """
    Checks if the elapsed time from the start_time is greater than 1 hour.

    Args:
    start_time (datetime): The start time for the elapsed time check.

    Returns:
    bool: True if the elapsed time is greater than 1 hour, False otherwise.
    """
    if (datetime.now(timezone.utc) - start_time) >= timedelta(hours=1):
        return True
    else:
        return False

# Documentation for the function that sends a downlink to turn on a device
def send_downlnk_to_turnon(self):
    """
    Sends a downlink to turn on a device using the ChirpStack API.

    Args:
    None

    Returns:
    None
    """
    channel = grpc.insecure_channel(chirpstack_url)
    client = api.DeviceServiceStub(channel)
    auth_token = [("authorization", "Bearer %s" % api_token)]
    req = api.EnqueueDeviceQueueItemRequest()
    req.queue_item.confirmed = True
    req.queue_item.data = payload
    req.queue_item.dev_eui = end_device_EUI
    req.queue_item.f_port = 5	#provide the port number that you want to send the downlink through

    resp = client.Enqueue(req, metadata=auth_token)
    print(f"Downlink ID: {resp.id}")

# Documentation for the callback function that is called when the MQTT client connects to the broker
def on_connect(client, userdata, flags, rc):
    """
    Callback function that is called when the MQTT client connects to the broker.

    Args:
    client (mqtt.Client): The MQTT client object.
    userdata (object): User-defined data that is passed to the callback function.
    flags (int): The flags that indicate the connection result.
    rc (int): The result code of the connection attempt.

    Returns:
    None
    """
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe(topic)

# Documentation for the callback function that is called when a message is received on the subscribed topic
def on_message(client, userdata, msg):
    """
    Callback function that is called when a message is received on the subscribed topic.

    Args:
    client (mqtt.Client): The MQTT client object.
    userdata (object): User-defined data that is passed to the callback function.
    msg (mqtt.Message): The message object that contains the received message.

    Returns:
    None
    """
    global start_time
    try:
        output = json.loads(msg.payload.decode())  # Decode the message payload
        print(output)
        elapsed_time = datetime.now(timezone.utc) - start_time
        if (time_status(start_time) == True):  # Check if the elapsed time is greater than 1 hour
            
            devEui = output["deviceInfo"]["devEui"]  # Get the device EUI from the message payload
            if (devEui == temperature_device_EUI):  # Check if the device EUI matches the expected EUI
                temperature = output["object"]["temperature"]  # Get the temperature value from the message payload
                if (temperature >= float(critical_temperature)):  # Check if the temperature is greater than or equal to 30
                    send_downlnk_to_turnon()  # Send a downlink to turn on the device
                    start_time = datetime.now(timezone.utc)  # Update the start time for the elapsed time check
                else:
                    print("Lower than threshold temperature value")  # Print a message if the temperature is below the threshold
            else:
                print("unknown device : " + str(devEui))  # Print a message if the device EUI is unknown
        else:
            print("elapsed time : " + str(elapsed_time))  # Print the elapsed time if it is less than 1 hour
    except Exception as e:
        print(e)  # Print any exceptions that occur during the execution of the callback function

# Documentation for the MQTT client object
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"Sprinkler_Client")
# Documentation for the function that sets the username and password for the MQTT client
client.username_pw_set(username, password)
# Documentation for the callback function that is called when a message is received on the subscribed topic
client.on_connect = on_connect
# Documentation for the callback function that is called when a message is received on the subscribed topic
client.on_message = on_message
# Documentation for the function that connects the MQTT client to the broker
client.connect(broker_address, 1883, 60)
# Documentation for the function that starts the MQTT client loop
client.loop_forever()
