// Create SCADA Graph Database for Pacific Water
// Clear existing data
MATCH (n) DETACH DELETE n;

// Create components
CREATE (:TREATMENT_PLANT {id: "tp_001", name: "West Pacific Water Treatment Plant", component_type: "treatment_plant", location: "123 Water Works Road, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: 5000, unit: "gpm", operational_status: "active", installed_date: "2015-03-15", metadata: {}});
CREATE (:SCADA_SERVER {id: "scada_srv_001", name: "Central SCADA Server", component_type: "scada_server", location: "123 Water Works Road, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: "2018-06-20", metadata: {}});
CREATE (:COMMUNICATION_NODE {id: "paccom_001", name: "PacCom Central Gateway", component_type: "communication_node", location: "100 Power Rd, Kaunakakai, Molokai, HI", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "fiber/5G", "bandwidth_gbps": 100}});
CREATE (:COMMUNICATION_NODE {id: "paccom_002", name: "PacCom West Hub", component_type: "communication_node", location: "Maunaloa Ridge, Molokai, HI", latitude: 21.2156, longitude: -157.1298, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "fiber/5G", "bandwidth_gbps": 40}});
CREATE (:COMMUNICATION_NODE {id: "paccom_003", name: "PacCom East Tower", component_type: "communication_node", location: "East End Rd, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"provider": "PacCom", "type": "5G", "bandwidth_gbps": 20}});
CREATE (:PUMPING_STATION {id: "ps_001", name: "Primary Pumping Station - North", component_type: "pumping_station", location: "456 North Shore Road, Molokai, HI", latitude: 21.2482, longitude: -157.0623, capacity: 3000, unit: "gpm", operational_status: "active", installed_date: "2016-09-10", metadata: {}});
CREATE (:PUMPING_STATION {id: "ps_002", name: "Secondary Pumping Station - East", component_type: "pumping_station", location: "789 East End Road, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: 2000, unit: "gpm", operational_status: "active", installed_date: "2017-11-05", metadata: {}});
CREATE (:RESERVOIR {id: "res_001", name: "North Storage Reservoir", component_type: "reservoir", location: "500 North Shore Road, Molokai, HI", latitude: 21.2561, longitude: -157.0854, capacity: 1000000, unit: "gallons", operational_status: "active", installed_date: "2010-01-20", metadata: {}});
CREATE (:RESERVOIR {id: "res_002", name: "East Storage Reservoir", component_type: "reservoir", location: "800 East End Road, Molokai, HI", latitude: 21.1802, longitude: -156.8567, capacity: 500000, unit: "gallons", operational_status: "active", installed_date: "2012-05-15", metadata: {}});
CREATE (:DISTRIBUTION_MAIN {id: "dm_001", name: "Main Distribution Line - North", component_type: "distribution_main", location: "North Shore zone, Molokai, HI", latitude: 21.2312, longitude: -157.0736, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"diameter_inches": 12, "length_km": 4.5}});
CREATE (:DISTRIBUTION_MAIN {id: "dm_002", name: "Main Distribution Line - East", component_type: "distribution_main", location: "East End zone, Molokai, HI", latitude: 21.1834, longitude: -156.8756, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"diameter_inches": 10, "length_km": 3.2}});
CREATE (:DISTRIBUTION_MAIN {id: "dm_003", name: "Main Distribution Line - Central", component_type: "distribution_main", location: "Central zone, Kaunakakai, Molokai, HI", latitude: 21.1923, longitude: -157.0621, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"diameter_inches": 14, "length_km": 2.8}});
CREATE (:CUSTOMER_ZONE {id: "cz_001", name: "Residential Zone - North", component_type: "customer_zone", location: "Maunaloa, North Molokai, HI", latitude: 21.2156, longitude: -157.1298, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"customers": 2500, "avg_consumption_gpm": 800}});
CREATE (:CUSTOMER_ZONE {id: "cz_002", name: "Commercial Zone - Central", component_type: "customer_zone", location: "Kaunakakai Downtown, Molokai, HI", latitude: 21.1943, longitude: -157.0519, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"customers": 1500, "avg_consumption_gpm": 600}});
CREATE (:CUSTOMER_ZONE {id: "cz_003", name: "Industrial Zone - East", component_type: "customer_zone", location: "Pukoo, East Molokai, HI", latitude: 21.1745, longitude: -156.8234, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"customers": 800, "avg_consumption_gpm": 500}});
CREATE (:CUSTOMER_ZONE {id: "cz_004", name: "Residential Zone - South", component_type: "customer_zone", location: "Mapulehu, South Molokai, HI", latitude: 21.1621, longitude: -157.0345, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {"customers": 2200, "avg_consumption_gpm": 700}});
CREATE (:RTU {id: "rtu_001", name: "RTU - North Station", component_type: "rtu", location: "456 North Shore Road, Molokai, HI", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: "2018-03-10", metadata: {}});
CREATE (:RTU {id: "rtu_002", name: "RTU - East Station", component_type: "rtu", location: "789 East End Road, Molokai, HI", latitude: 21.1865, longitude: -156.8945, capacity: null, unit: null, operational_status: "active", installed_date: "2018-03-10", metadata: {}});
CREATE (:RTU {id: "rtu_003", name: "RTU - North Reservoir", component_type: "rtu", location: "500 North Shore Road, Molokai, HI", latitude: 21.2561, longitude: -157.0854, capacity: null, unit: null, operational_status: "active", installed_date: "2019-07-15", metadata: {}});
CREATE (:FLOW_METER {id: "fm_001", name: "Flow Meter - Treatment Plant Exit", component_type: "flow_meter", location: "Kaunakakai Treatment Plant", latitude: 21.1952, longitude: -157.0547, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:LEVEL_SENSOR {id: "ls_001", name: "Level Sensor - North Reservoir", component_type: "level_sensor", location: "North Shore Reservoir", latitude: 21.2561, longitude: -157.0854, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:LEVEL_SENSOR {id: "ls_002", name: "Level Sensor - East Reservoir", component_type: "level_sensor", location: "East End Reservoir", latitude: 21.1802, longitude: -156.8567, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:PRESSURE_GAUGE {id: "pg_001", name: "Pressure Gauge - North Line", component_type: "pressure_gauge", location: "North Shore Distribution Main", latitude: 21.2312, longitude: -157.0736, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:PRESSURE_GAUGE {id: "pg_002", name: "Pressure Gauge - East Line", component_type: "pressure_gauge", location: "East End Distribution Main", latitude: 21.1834, longitude: -156.8756, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:PRV {id: "prv_001", name: "Pressure Reducing Valve - North", component_type: "prv", location: "North Shore PRV Station, Molokai, HI", latitude: 21.2234, longitude: -157.0892, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:CHECK_VALVE {id: "cv_001", name: "Check Valve - Pump Station North", component_type: "check_valve", location: "North Pumping Station, Molokai, HI", latitude: 21.2482, longitude: -157.0623, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});
CREATE (:ISOLATION_VALVE {id: "iv_001", name: "Isolation Valve - North Main", component_type: "isolation_valve", location: "North Shore Main Valve Station, Molokai, HI", latitude: 21.2401, longitude: -157.0679, capacity: null, unit: null, operational_status: "active", installed_date: null, metadata: {}});

// Create connections
MATCH (a {id: 'paccom_001'}), (b {id: 'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'paccom_001'}), (b {id: 'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'paccom_001'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'tp_001'}), (b {id: 'ps_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'tp_001'}), (b {id: 'ps_002'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ps_001'}), (b {id: 'res_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ps_002'}), (b {id: 'res_002'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'res_001'}), (b {id: 'dm_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'res_002'}), (b {id: 'dm_002'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'res_001'}), (b {id: 'dm_003'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'dm_001'}), (b {id: 'cz_001'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'dm_003'}), (b {id: 'cz_002'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'dm_002'}), (b {id: 'cz_003'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'dm_001'}), (b {id: 'cz_004'}) CREATE (a)-[:HYDRAULIC {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'rtu_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'rtu_002'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'scada_srv_001'}), (b {id: 'rtu_003'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}), (b {id: 'paccom_002'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_003'}), (b {id: 'paccom_003'}) CREATE (a)-[:COMMUNICATION {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'ps_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_002'}), (b {id: 'ps_002'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'fm_001'}), (b {id: 'rtu_001'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ls_001'}), (b {id: 'rtu_003'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'ls_002'}), (b {id: 'rtu_002'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'pg_001'}), (b {id: 'rtu_001'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'pg_002'}), (b {id: 'rtu_002'}) CREATE (a)-[:MONITORING {flow_direction: 'unidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'prv_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'cv_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);
MATCH (a {id: 'rtu_001'}), (b {id: 'iv_001'}) CREATE (a)-[:CONTROL {flow_direction: 'bidirectional'}]->(b);