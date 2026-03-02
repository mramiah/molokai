// Pacific Power SCADA Database
MATCH (n) DETACH DELETE n;

// Create components
CREATE (:WIND_FARM {id: "pp_001", name: "Kaunakakai Wind Farm", component_type: "wind_farm", location: "West Molokai ridge", latitude: 21.205, longitude: -157.07, capacity: 2000, unit: "kW", operational_status: "active", installed_date: "2015-06-01", metadata: {"turbines": 20}});
CREATE (:SOLAR_ARRAY {id: "pp_002", name: "Maunaloa Solar Array", component_type: "solar_array", location: "Maunaloa plains", latitude: 21.2156, longitude: -157.1298, capacity: 1500, unit: "kW", operational_status: "active", installed_date: "2016-09-15", metadata: {"panels": 5000}});
CREATE (:HYDRO_PLANT {id: "pp_003", name: "East End Hydro Plant", component_type: "hydro_plant", location: "East Molokai stream", latitude: 21.182, longitude: -156.88, capacity: 800, unit: "kW", operational_status: "active", installed_date: "2014-11-20", metadata: {}});
CREATE (:OCEAN_PLANT {id: "pp_004", name: "Ocean Current Generator", component_type: "ocean_plant", location: "Kaunakakai bay", latitude: 21.195, longitude: -157.055, capacity: 500, unit: "kW", operational_status: "active", installed_date: "2018-03-05", metadata: {}});
CREATE (:POWER_SENSOR {id: "ps_001", name: "Power Sensor - Wind Farm", component_type: "power_sensor", location: "West Molokai ridge", latitude: 21.205, longitude: -157.07, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:POWER_SENSOR {id: "ps_002", name: "Power Sensor - Solar Array", component_type: "power_sensor", location: "Maunaloa plains", latitude: 21.2156, longitude: -157.1298, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:SUBSTATION {id: "sub_001", name: "Generation Substation", component_type: "substation", location: "100 Power Rd, Kaunakakai", latitude: 21.1952, longitude: -157.0547, capacity: 5000, unit: "kW", operational_status: "active", installed_date: null, metadata: {}});
CREATE (:TRANSMISSION_LINE {id: "line_001", name: "Transmission Line - West Corridor", component_type: "transmission_line", location: "West route", latitude: 21.205, longitude: -157.07, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"length_km": 7, "voltage_kv": 69}});
CREATE (:SCADA_SERVER {id: "scada_srv_001", name: "Power SCADA Server", component_type: "scada_server", location: "100 Power Rd, Kaunakakai", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2015-01-10", metadata: {}});
CREATE (:COMMUNICATION_NODE {id: "paccom_001", name: "PacCom Central Gateway", component_type: "communication_node", location: "100 Power Rd, Kaunakakai", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "fiber/5G", "bandwidth_gbps": 100}});
CREATE (:COMMUNICATION_NODE {id: "paccom_002", name: "PacCom West Relay", component_type: "communication_node", location: "Maunaloa Ridge", latitude: 21.2156, longitude: -157.1298, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "5G", "bandwidth_gbps": 25}});
CREATE (:COMMUNICATION_NODE {id: "paccom_003", name: "PacCom East Relay", component_type: "communication_node", location: "East End Rd", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "5G", "bandwidth_gbps": 25}});
CREATE (:RTU {id: "rtu_001", name: "RTU - Generation Substation", component_type: "rtu", location: "Generation Substation", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2015-01-10", metadata: {}});

// Create connections
MATCH (a {id: 'paccom_001'}),(b {id:'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'paccom_001'}),(b {id:'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}),(b {id:'paccom_001'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}),(b {id:'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}),(b {id:'rtu_001'}) CREATE (a)-[:CONTROL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}),(b {id:'ps_001'}) CREATE (a)-[:MONITORING {flow_direction:'unidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}),(b {id:'ps_002'}) CREATE (a)-[:MONITORING {flow_direction:'unidirectional'}]->(b);
MATCH (a {id: 'pp_001'}),(b {id:'line_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'pp_002'}),(b {id:'line_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'pp_003'}),(b {id:'sub_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'pp_004'}),(b {id:'sub_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'line_001'}),(b {id:'sub_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);