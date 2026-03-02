# Pacific Water SCADA Graph Database - Query Guide

## System Overview
- **System**: Pacific Water Distribution Network
- **City**: West Pacific  
- **Population**: 10,000
- **Database Type**: Graph Database (Nodes & Edges)

## Component Types

### Primary Infrastructure
- **Treatment Plant**: Water treatment facility
- **Pumping Stations**: Boost water pressure through network
- **Reservoirs**: Storage tanks for water supply

### Distribution Network
- **Distribution Mains**: Large pipes carrying water to zones
- **Customer Zones**: Service areas for residential/commercial/industrial customers
- **Service Lines**: Individual connections to customers

### Control & Monitoring
- **SCADA Server**: Central control hub
- **RTUs (Remote Terminal Units)**: Local controllers at pumping stations, reservoirs
- **PLCs**: Programmable logic controllers
- **Sensors**: Flow meters, level sensors, pressure gauges
- **Control Valves**: PRVs, check valves, isolation valves

## Connection Types

### Hydraulic Connections (Water Flow)
- Represent physical water flow through pipes
- Properties: capacity (gpm), diameter (inches), length (km), material
- Direction: Unidirectional (water flows one way)

### Control Connections (SCADA Commands)
- Represent control signals from SCADA to devices
- Bidirectional communication
- Properties: None (metadata optional)

### Monitoring Connections
- Data collection from sensors to RTUs
- Unidirectional (sensors → controllers)
- Properties: Data type, frequency, etc.

### Communication Connections
- Network communication between systems (PacCom backbone provides the physical/fiber/5G/5G link)
- The backbone is modeled as three hubs:
  - `paccom_001` - Central Gateway
  - `paccom_002` - West Hub
  - `paccom_003` - East Tower
- RTUs connect to the closest hub, and the hubs interconnect for redundancy.

### Example: Querying PacCom Network
```python
# list PacCom hubs and their direct neighbors
for hub in ['paccom_001','paccom_002','paccom_003']:
    print(hub, scada.get_neighbors(hub))

# find which RTUs attach to a given hub
west_rtu = [n for n in scada.get_neighbors('paccom_002') if n.startswith('rtu')]
print("RTUs on West Hub:", west_rtu)
```

- Bidirectional
- Properties: Bandwidth, protocol, etc.

## Sample Graph Queries

### 1. Find All Water Sources
```python
sources = [node for node in scada.graph.nodes() 
           if scada.graph.nodes[node]['component_type'] == 'treatment_plant']
```

### 2. Trace Water Path from Treatment to Customer
```python
paths = scada.find_paths("tp_001", "cz_001")
```

### 3. Get All Components Under SCADA Control
```python
neighbors = scada.get_neighbors("scada_srv_001")
```

### 4. Find Bottlenecks (High degree nodes)
```python
degrees = dict(scada.graph.degree())
bottlenecks = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
```

### 5. Analyze Network Redundancy
```python
# Find components with multiple paths to critical infrastructure
for node1 in scada.graph.nodes():
    for node2 in scada.graph.nodes():
        paths = scada.find_paths(node1, node2)
        if len(paths) > 1:
            print(f"Redundancy found: {node1} -> {node2}: {len(paths)} paths")
```

### 6. Get All Sensors in System
```python
sensors = scada.get_subgraph_by_type(ComponentType.FLOW_METER)
sensors.add_nodes_from(scada.get_subgraph_by_type(ComponentType.LEVEL_SENSOR).nodes())
sensors.add_nodes_from(scada.get_subgraph_by_type(ComponentType.PRESSURE_GAUGE).nodes())
```

### 7. Calculate System Capacity
```python
total_capacity = sum(
    scada.components[c].capacity 
    for c in scada.components 
    if scada.components[c].capacity
)
```

### 8. Find Isolated Components
```python
# Components with no connections
isolated = [node for node in scada.graph.nodes() 
            if scada.graph.degree(node) == 0]
```

## Neo4j Cypher Queries

### Create Relationships Between Zones
```cypher
MATCH (z1:customer_zone), (z2:customer_zone)
WHERE z1.name <> z2.name
CREATE (z1)-[:ADJACENT_TO]->(z2);
```

### Get All Components Within 2-Hop Distance
```cypher
MATCH (n:treatment_plant)-[*1..2]-(m)
RETURN DISTINCT m;
```

### Find Critical Nodes (Articulation Points)
```cypher
MATCH (n)
WITH n, size(()-[]->(n)) as inDegree, 
     size((n)-[]->()) as outDegree
WHERE inDegree > 2 AND outDegree > 2
RETURN n.name, inDegree, outDegree
ORDER BY (inDegree + outDegree) DESC;
```

### Calculate Total System Capacity
```cypher
MATCH (n)
WHERE n.capacity IS NOT NULL
RETURN sum(n.capacity) as total_capacity;
```

### Analyze Customer Zone Coverage
```cypher
MATCH (d:distribution_main)-[*1..2]-(c:customer_zone)
RETURN d.name, count(DISTINCT c) as zones_served
ORDER BY zones_served DESC;
```

## System Architecture

```
┌─────────────────────────────────────┐
│  Water Treatment Plant (tp_001)     │
│  Capacity: 5,000 gpm                │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
┌───────▼────┐  ┌─────▼───────┐
│PS North    │  │PS East      │
│3000 gpm    │  │2000 gpm     │
└───────┬────┘  └─────┬───────┘
        │             │
    ┌───▼─┐      ┌───▼─┐
    │Res N│      │Res E│
    └───┬─┘      └───┬─┘
        │             │
    ┌───▼──────────┬──▼───┐
    │              │      │
┌───▼──┐      ┌──▼──┐ ┌─▼──┐
│DM N  │      │DM C │ │DM E│
└───┬──┘      └──┬──┘ └─┬──┘
    │            │      │
 ┌──▼──┬─────┬──▼──┐   │
 │ CZ1 │ CZ4 │ CZ2 │ ┌─▼──┐
 └─────┴─────┴─────┘ │CZ3│
                     └───┘

Legend:
- tp: Treatment Plant
- PS: Pumping Station
- Res: Reservoir
- DM: Distribution Main
- CZ: Customer Zone
```

## Key Metrics

### Network Statistics
- **Total Components**: 32
- **Total Connections**: 35+
- **Average Path Length**: ~3-4 hops from source to customer
- **Network Diameter**: Maximum distance between any two nodes

### Capacity Analysis
- **Treatment Capacity**: 5,000 gpm
- **Peak Distribution**: 2,700 gpm (North + East pumping)
- **Peak Customer Demand**: 2,600 gpm (combined zones)
- **Reserve Capacity**: ~400 gpm (15.4% safety margin)

### Coverage
- **Service Population**: 10,000
- **Customer Zones**: 4
- **Distribution Mains**: 3
- **Monitoring Points**: 5 (flow, levels, pressure)
- **Control Points**: 3 (PRV, check valve, isolation valve)

## Extending the Graph

### Add New Component
```python
new_component = Component(
    id="cz_005",
    name="New Zone",
    component_type=ComponentType.CUSTOMER_ZONE,
    location="...",
    latitude=21.30,
    longitude=-157.85,
    metadata={"customers": 1000, "avg_consumption_gpm": 300}
)
scada.add_component(new_component)
```

### Add New Connection
```python
connection = Connection(
    source_id="dm_001",
    target_id="cz_005",
    connection_type=ConnectionType.HYDRAULIC,
    flow_direction="unidirectional",
    capacity=300,
    diameter_inches=6,
    length_km=0.5,
    material="PVC"
)
scada.add_connection(connection)
```

## System Resilience Analysis

### Single Point of Failures
1. **Treatment Plant**: Critical - no redundancy
2. **Pumping Stations**: Partial - two stations provide some redundancy
3. **Reservoirs**: Redundant system for two zones

### Recommended Improvements
1. Add tertiary treatment source
2. Add cross-connection valve between distribution mains
3. Install additional level sensors in North Reservoir
4. Implement automated failover for pump stations
5. Add backup SCADA server for disaster recovery

## Files in This Project

- `scada_graph_schema.py` - Main Python implementation with NetworkX
- `pacific_water_scada_data.json` - Exported graph data in JSON format
- `pacific_water_scada_neo4j.cypher` - Neo4j Cypher commands for database setup
- `pacific_water_scada_visualization.png` - Network topology visualization
- `SCADA_GRAPH_QUERIES.md` - This query guide

## Running the System

```bash
# Install dependencies
pip install networkx matplotlib

# Run the schema creation
python scada_graph_schema.py

# Output:
# - pacific_water_scada_data.json
# - pacific_water_scada_neo4j.cypher
# - pacific_water_scada_visualization.png
```

## Integration with Neo4j

1. Install Neo4j (Community or Enterprise)
2. Start Neo4j service
3. Open Neo4j Browser (localhost:7474)
4. Execute commands from `pacific_water_scada_neo4j.cypher`
5. Run Cypher queries for analysis

## Future Enhancements

- [ ] Time-series data integration (demand patterns)
- [ ] Real-time sensor data streaming
- [ ] Machine learning for demand forecasting
- [ ] Anomaly detection in flow/pressure patterns
- [ ] 3D map visualization of network
- [ ] Integration with GIS systems
- [ ] Water quality monitoring nodes
- [ ] Energy consumption analytics
