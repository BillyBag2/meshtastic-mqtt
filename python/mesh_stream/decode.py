"""
Decode the messages from MQTT server.
"""
from meshtastic import mesh_pb2, mqtt_pb2, portnums_pb2, telemetry_pb2, storeforward_pb2
from google.protobuf.json_format import MessageToJson
import json

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

    Parameters:
    msg (mqtt.MQTTMessage): The MQTT message to decode.

    Returns:
    json_data (str): The decoded message in JSON format, or None if an error occurred.
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
        raise
        print(f"Error decoding message: {exception}")
        return None

def unpack_payload(service_envelope):
    """
    Unpack the payload from the service envelope

    Parameters:
    service_envelope: The service envelope to unpack.

    Returns:
    payload (object): The payload, or None if an error occurred.
    """
    packet = service_envelope.packet
    if not packet.HasField("decoded"):
        return None
    #print(f"Packet: {packet}")  
    payload = packet.decoded.payload
    portnum = packet.decoded.portnum
    if portnum == portnums_pb2.TEXT_MESSAGE_APP:
        unpacked_payload = packet.decoded.payload.decode("utf-8")
        return { "TEXT_MESSAGE": unpacked_payload }   
    if portnum == portnums_pb2.NODEINFO_APP:
        info = mesh_pb2.User()
        info.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(info)
        json_data = json.loads(json_string)
        # Convert json to dictionary ?
        return json_data
    if portnum == portnums_pb2.POSITION_APP:
        position = mesh_pb2.Position()
        position.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(position)
        json_data = json.loads(json_string)
        return { "POSITION": json_data }
    if portnum == portnums_pb2.TELEMETRY_APP:
        telemetry = telemetry_pb2.Telemetry()
        telemetry.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(telemetry)
        json_data = json.loads(json_string)
        return { "TELEMETRY": json_data }
    if portnum == portnums_pb2.MAP_REPORT_APP:
        map_report = mqtt_pb2.MapReport()
        map_report.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(map_report)
        json_data = json.loads(json_string)
        return { "MAP_REPORT": json_data }
    if portnum == portnums_pb2.NEIGHBORINFO_APP:
        neighbor = mesh_pb2.Neighbor()
        neighbor.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(neighbor)
        json_data = json.loads(json_string)
        return { "NEIGHBORINFO": json_data }
    if portnum == portnums_pb2.ROUTING_APP:
        routing = mesh_pb2.Routing()
        routing.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(routing)
        json_data = json.loads(json_string)
        return { "ROUTING": json_data }
    if portnum == portnums_pb2.STORE_FORWARD_APP:
        store_forward = storeforward_pb2.StoreAndForward()
        store_forward.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(store_forward)
        json_data = json.loads(json_string)
        return { "STORE_FORWARD": json_data }
    if portnum == portnums_pb2.TRACEROUTE_APP:
        traceroute = mesh_pb2.RouteDiscovery()
        traceroute.ParseFromString(packet.decoded.payload)
        json_string = MessageToJson(traceroute)
        json_data = json.loads(json_string)
        return { "TRACEROUTE": json_data }
    # error
    print(f"Unknown portnum: {portnum}")
    return None


def service_envelope(msg):
    """
    Decode the service envelop

    Parameters:
    msg (mqtt.MQTTMessage): The MQTT message to decode.

    Returns:
    service_envelope (json): The decoded message, or None if an error occurred.
    """
    # Deserialize the protobuf message
    service_envelop = mqtt_pb2.ServiceEnvelope()
    try:
        service_envelop.ParseFromString(msg.payload)
        json_string = MessageToJson(service_envelop)
        # Convert protobuf message to JSON
        json_data = json.loads(json_string)
        unpacked_payload = unpack_payload(service_envelop)
        if unpacked_payload is not None:
            #packet = json_data["packet"]
            json_data["packet"]["decoded"].update(unpacked_payload)
        return json_data
    except Exception as exception:
        raise
        print(f"Error decoding message: {exception}")
        return None