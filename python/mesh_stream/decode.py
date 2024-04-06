"""
Decode the messages from MQTT server.
"""
from meshtastic import mesh_pb2
from meshtastic import mqtt_pb2
from google.protobuf.json_format import MessageToJson

def online(msg):
    """
    Decode the online/offline
    """
    try:
        data = msg.payload.decode()
        return data
    except Exception as exception:
        #print(f"Error decoding message: {exception}")
        return None

def mesh_packet(msg):
    """
    Decode the mesh packet (Is this still needed ?)
    """
    # Deserialize the protobuf message
    try:
        mesh_packet = mesh_pb2.MeshPacket()
        mesh_packet.ParseFromString(msg.payload)
        #asDict = google.protobuf.json_format.MessageToDict(mesh_packet)
        # Convert protobuf message to JSON
        json_data = MessageToJson(mesh_packet)
        return json_data
    except Exception as exception:
        print(f"Error decoding message: {exception}")
        return None
    
def service_envelope(msg):
    """
    Decode the service envelop
    """
    # Deserialize the protobuf message
    service_envelop = mqtt_pb2.ServiceEnvelope()
    try:
        service_envelop.ParseFromString(msg.payload)
        return service_envelop
    except Exception as exception:
        print(f"Error decoding message: {exception}")
        return None