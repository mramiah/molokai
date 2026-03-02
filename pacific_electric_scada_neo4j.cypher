// Pacific Electric SCADA Database
MATCH (n) DETACH DELETE n;

// Create components
CREATE (:SUBSTATION {id: "sub_001", name: "Kaunakakai Substation", component_type: "substation", location: "100 Power Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: 5000, unit: "kW", operational_status: "active", installed_date: "2013-04-01", metadata: {}});
CREATE (:SUBSTATION {id: "sub_002", name: "East End Substation", component_type: "substation", location: "1400 East End Rd, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: 3000, unit: "kW", operational_status: "active", installed_date: "2013-04-01", metadata: {}});
CREATE (:DISTRIBUTION_FEEDER {id: "fd_001", name: "Feeder - North Shore", component_type: "distribution_feeder", location: "North Shore corridor", latitude: 21.2312, longitude: -157.0736, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"voltage_kv": 12, "length_km": 5}});
CREATE (:DISTRIBUTION_FEEDER {id: "fd_002", name: "Feeder - Central", component_type: "distribution_feeder", location: "Kaunakakai town", latitude: 21.1923, longitude: -157.0621, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"voltage_kv": 12, "length_km": 3}});
CREATE (:DISTRIBUTION_FEEDER {id: "fd_003", name: "Feeder - East End", component_type: "distribution_feeder", location: "East End corridor", latitude: 21.1834, longitude: -156.8756, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"voltage_kv": 12, "length_km": 4}});
CREATE (:TRANSFORMER {id: "tr_001", name: "Transformer - Maunaloa", component_type: "transformer", location: "Maunaloa", latitude: 21.2156, longitude: -157.1298, capacity: 1000, unit: "kVA", operational_status: "active", installed_date: null, metadata: {}});
CREATE (:TRANSFORMER {id: "tr_002", name: "Transformer - Pukoo", component_type: "transformer", location: "Pukoo", latitude: 21.1745, longitude: -156.8234, capacity: 800, unit: "kVA", operational_status: "active", installed_date: null, metadata: {}});
CREATE (:BREAKER {id: "br_001", name: "Breaker - Kaunakakai Substation", component_type: "breaker", location: "Kaunakakai Substation", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:BREAKER {id: "br_002", name: "Breaker - East Substation", component_type: "breaker", location: "East End Substation", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:METER {id: "mt_001", name: "Meter - Maunaloa Residential", component_type: "meter", location: "Maunaloa", latitude: 21.2156, longitude: -157.1298, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:METER {id: "mt_002", name: "Meter - Kaunakakai Commercial", component_type: "meter", location: "Kaunakakai Downtown", latitude: 21.1943, longitude: -157.0519, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:VOLTAGE_SENSOR {id: "vs_001", name: "Voltage Sensor - North Feeder", component_type: "voltage_sensor", location: "North Feeder", latitude: 21.2312, longitude: -157.0736, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:CURRENT_SENSOR {id: "cs_001", name: "Current Sensor - East Feeder", component_type: "current_sensor", location: "East Feeder", latitude: 21.1834, longitude: -156.8756, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:TEMPERATURE_SENSOR {id: "ts_001", name: "Temperature Sensor - Transformer Pukoo", component_type: "temperature_sensor", location: "Pukoo Transformer", latitude: 21.1745, longitude: -156.8234, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:SCADA_SERVER {id: "scada_srv_001", name: "Central SCADA Server", component_type: "scada_server", location: "100 Power Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2017-01-15", metadata: {}});
CREATE (:COMMUNICATION_NODE {id: "paccom_001", name: "PacCom Central Gateway", component_type: "communication_node", location: "100 Power Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "fiber/5G", "bandwidth_gbps": 100}});
CREATE (:COMMUNICATION_NODE {id: "paccom_002", name: "PacCom North Relay", component_type: "communication_node", location: "North Shore Rd, Molokai, HI", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "5G", "bandwidth_gbps": 30}});
CREATE (:COMMUNICATION_NODE {id: "paccom_003", name: "PacCom East Relay", component_type: "communication_node", location: "East End Rd, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "5G", "bandwidth_gbps": 30}});
CREATE (:RTU {id: "rtu_001", name: "RTU - Kaunakakai Substation", component_type: "rtu", location: "Kaunakakai Substation", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2017-01-15", metadata: {}});
CREATE (:RTU {id: "rtu_002", name: "RTU - East Substation", component_type: "rtu", location: "East End Substation", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: "2017-01-15", metadata: {}});

// Create connections
MATCH (a {id: 'paccom_001'}),(b {id:'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'paccom_001'}),(b {id:'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}),(b {id:'paccom_001'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}),(b {id:'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}),(b {id:'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}),(b {id:'rtu_001'}) CREATE (a)-[:CONTROL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}),(b {id:'rtu_002'}) CREATE (a)-[:CONTROL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}),(b {id:'br_001'}) CREATE (a)-[:CONTROL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}),(b {id:'br_002'}) CREATE (a)-[:CONTROL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'vs_001'}),(b {id:'rtu_001'}) CREATE (a)-[:MONITORING {flow_direction:'unidirectional'}]->(b);
MATCH (a {id: 'cs_001'}),(b {id:'rtu_002'}) CREATE (a)-[:MONITORING {flow_direction:'unidirectional'}]->(b);
MATCH (a {id: 'ts_001'}),(b {id:'rtu_002'}) CREATE (a)-[:MONITORING {flow_direction:'unidirectional'}]->(b);
MATCH (a {id: 'sub_001'}),(b {id:'fd_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'sub_001'}),(b {id:'fd_002'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'sub_002'}),(b {id:'fd_003'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'fd_001'}),(b {id:'tr_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'fd_003'}),(b {id:'tr_002'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'fd_001'}),(b {id:'mt_001'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);
MATCH (a {id: 'fd_002'}),(b {id:'mt_002'}) CREATE (a)-[:ELECTRICAL {flow_direction:'bidirectional'}]->(b);