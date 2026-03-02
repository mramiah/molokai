// Pacific Treatment SCADA Database
MATCH (n) DETACH DELETE n;

// Create components
CREATE (:TREATMENT_PLANT {id: "tp_001", name: "Molokai Wastewater Treatment Plant", component_type: "treatment_plant", location: "500 Treatment Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: 3000, unit: "gpm", operational_status: "active", installed_date: "2014-07-01", metadata: {}});
CREATE (:SCADA_SERVER {id: "scada_srv_001", name: "Central SCADA Server", component_type: "scada_server", location: "500 Treatment Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2017-02-10", metadata: {}});
CREATE (:COMMUNICATION_NODE {id: "paccom_001", name: "PacCom Central Gateway", component_type: "communication_node", location: "100 Power Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "fiber/5G", "bandwidth_gbps": 100}});
CREATE (:COMMUNICATION_NODE {id: "paccom_002", name: "PacCom North Tower", component_type: "communication_node", location: "North Shore Rd, Molokai, HI", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "5G", "bandwidth_gbps": 30}});
CREATE (:COMMUNICATION_NODE {id: "paccom_003", name: "PacCom East Hub", component_type: "communication_node", location: "East End Rd, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "fiber/5G", "bandwidth_gbps": 20}});
CREATE (:LIFT_STATION {id: "ls_001", name: "Lift Station - North Shore", component_type: "lift_station", location: "900 North Shore Rd, Molokai, HI", latitude: 21.2482, longitude: -157.0623, capacity: 1500, unit: "gpm", operational_status: "active", installed_date: "2016-05-20", metadata: {}});
CREATE (:LIFT_STATION {id: "ls_002", name: "Lift Station - East End", component_type: "lift_station", location: "1200 East End Rd, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: 1000, unit: "gpm", operational_status: "active", installed_date: "2016-05-20", metadata: {}});
CREATE (:SEWER_MAIN {id: "sm_001", name: "Sewer Main - North", component_type: "sewer_main", location: "North Shore corridor", latitude: 21.2312, longitude: -157.0736, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"diameter_inches": 36, "length_km": 5.0}});
CREATE (:SEWER_MAIN {id: "sm_002", name: "Sewer Main - Central", component_type: "sewer_main", location: "Kaunakakai town", latitude: 21.1923, longitude: -157.0621, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"diameter_inches": 42, "length_km": 3.0}});
CREATE (:SEWER_MAIN {id: "sm_003", name: "Sewer Main - East", component_type: "sewer_main", location: "East End corridor", latitude: 21.1834, longitude: -156.8756, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"diameter_inches": 30, "length_km": 4.0}});
CREATE (:MANHOLE {id: "mh_001", name: "Manhole - Maunaloa Residential", component_type: "manhole", location: "Maunaloa", latitude: 21.2156, longitude: -157.1298, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:MANHOLE {id: "mh_002", name: "Manhole - Kaunakakai Commercial", component_type: "manhole", location: "Kaunakakai Downtown", latitude: 21.1943, longitude: -157.0519, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:MANHOLE {id: "mh_003", name: "Manhole - Pukoo Industrial", component_type: "manhole", location: "Pukoo", latitude: 21.1745, longitude: -156.8234, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:MANHOLE {id: "mh_004", name: "Manhole - Mapulehu South", component_type: "manhole", location: "Mapulehu", latitude: 21.1621, longitude: -157.0345, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:FLOW_METER {id: "fm_001", name: "Flow Meter - North Main", component_type: "flow_meter", location: "North Shore main", latitude: 21.2312, longitude: -157.0736, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:LEVEL_SENSOR {id: "ls_003", name: "Level Sensor - North Lift Station", component_type: "level_sensor", location: "North Shore lift", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:TURBIDITY_SENSOR {id: "ts_001", name: "Turbidity Sensor - Treatment Plant Exit", component_type: "turbidity_sensor", location: "Treatment Plant", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:PRESSURE_GAUGE {id: "pg_001", name: "Pressure Gauge - East Main", component_type: "pressure_gauge", location: "East corridor", latitude: 21.1834, longitude: -156.8756, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:ISOLATION_VALVE {id: "iv_001", name: "Isolation Valve - North Main", component_type: "isolation_valve", location: "North main junction", latitude: 21.2401, longitude: -157.0679, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:CHECK_VALVE {id: "cv_001", name: "Check Valve - North Lift", component_type: "check_valve", location: "North lift station", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:RTU {id: "rtu_001", name: "RTU - Treatment Plant", component_type: "rtu", location: "Treat Plant", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2017-02-10", metadata: {}});
CREATE (:RTU {id: "rtu_002", name: "RTU - North Lift", component_type: "rtu", location: "North Shore", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: "2017-02-10", metadata: {}});
CREATE (:RTU {id: "rtu_003", name: "RTU - East Lift", component_type: "rtu", location: "East End", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: "2017-02-10", metadata: {}});

// Create connections
MATCH (a {id: 'paccom_001'}), (b {id: 'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'paccom_001'}), (b {id: 'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'paccom_001'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'rtu_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'rtu_002'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'rtu_003'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}), (b {id: 'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_003'}), (b {id: 'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}), (b {id: 'ls_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_003'}), (b {id: 'ls_002'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'iv_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}), (b {id: 'cv_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'fm_001'}), (b {id: 'rtu_001'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ls_003'}), (b {id: 'rtu_002'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ts_001'}), (b {id: 'rtu_001'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'pg_001'}), (b {id: 'rtu_003'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'tp_001'}), (b {id: 'ls_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'tp_001'}), (b {id: 'ls_002'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ls_001'}), (b {id: 'sm_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ls_002'}), (b {id: 'sm_003'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'sm_001'}), (b {id: 'mh_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'sm_002'}), (b {id: 'mh_002'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'sm_003'}), (b {id: 'mh_003'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'sm_001'}), (b {id: 'mh_004'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);