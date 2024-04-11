#!/bin/python3
"""
Test script for MQTT connection to Meshtastic mqtt server.
"""
import random
import json
from google.protobuf.json_format import MessageToJson
import paho.mqtt.client as mqtt_client
import paho.mqtt.enums as mqtt_enums
#from meshtastic import mesh_pb2
#from meshtastic import mqtt_pb2

import mesh_stream

#SUBSCIBE_TOPICS = "msh/EU_868/2/e/LongFast/#"
SUBSCIBE_TOPICS = "msh/EU_868/2/e/LongFast/!da545314"

def on_connect(client, _userdata, _flags, result_code, _properties):
    """
    Called when connected to MQTT server
    """
    print("Connected with result code "+str(result_code))
    client.subscribe(SUBSCIBE_TOPICS)

def on_message(_client, _userdata, msg):
    """
    Called when a message is received from MQTT server
    """
    # Deserialize the protobuf message
    #mesh_packet = mesh_pb2.MeshPacket()
    #asDict = google.protobuf.json_format.MessageToDict(mesh_packet)
    #mesh_packet.ParseFromString(msg.payload)
    # Convert protobuf message to JSON
    #json_data = MessageToJson(mesh_packet)
    #fromRadio = mesh_pb2.FromRadio()
    #fromRadio.ParseFromString(msg.payload)
    #json_data = MessageToJson(fromRadio)
    #service_envelop = mqtt_pb2.ServiceEnvelope()
    #service_envelop.ParseFromString(msg.payload)
    #json_data = MessageToJson(service_envelop)
    #print(json_data)
    result = mesh_stream.decode.online(msg)
    if result is not None:
        if result == "online":
            print(f"> ONLINE '{msg.topic}'")
            return
        if result == "offline":
            print(f"> OFFLINE '{msg.topic}'")
            return
        # If result starts with { asume it is json.
        if result.startswith("{"):
            print(f"Received message on topic '{msg.topic}'")
            # Change smart quotes to normal double quotes.
            result = result.replace("“", "\"").replace("”", "\"")
            # Convert result string to json.
            print(f"Decoded message: '{result}'")
            data = json.loads(result)
            # Print the jason in a pritty way with indent 4.
            print(json.dumps(data, indent=4))
            return
        print(f"Received message on topic '{msg.topic}'")
        print(f"Decoded but not recognised?: '{result}'")
        return
    print(f"Received message on topic '{msg.topic}'")
    print(f"Received message: Unknown payload")
    # Safely print the result that may be ascii but may also contain binary.
    print(repr(msg.payload))
    service_envelope = mesh_stream.decode.service_envelope(msg)
    print(json.dumps(service_envelope, indent=4))

def main():
    """
    Main function
    """
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    client = mqtt_client.Client(client_id=client_id,
                                callback_api_version=mqtt_enums.CallbackAPIVersion.VERSION2 )
    # Set the username and password
    client.username_pw_set("meshdev", "large4cats")

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt.meshtastic.org", 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
