"""
SCADA Graph Database Schema for Pacific Water Distribution Network
System for West Pacific (Population: 10,000)
"""

import networkx as nx
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class ComponentType(Enum):
    """Types of components in the SCADA system"""
    TREATMENT_PLANT = "treatment_plant"
    PUMPING_STATION = "pumping_station"
    RESERVOIR = "reservoir"
    PRESSURE_REDUCING_VALVE = "prv"
    FLOW_METER = "flow_meter"
    LEVEL_SENSOR = "level_sensor"
    RTU = "rtu"
    PLCCONTROLLER = "plc_controller"
    SCADA_SERVER = "scada_server"
    MONITORING_STATION = "monitoring_station"
    DISTRIBUTION_MAIN = "distribution_main"
    SERVICE_LINE = "service_line"
    CUSTOMER_ZONE = "customer_zone"
    PRESSURE_GAUGE = "pressure_gauge"
    CHECK_VALVE = "check_valve"
    ISOLATION_VALVE = "isolation_valve"
    COMMUNICATION_NODE = "communication_node"


class ConnectionType(Enum):
    """Types of connections between components"""
    HYDRAULIC = "hydraulic"  # Physical water flow
    CONTROL = "control"  # SCADA control signal
    MONITORING = "monitoring"  # Data collection
    COMMUNICATION = "communication"  # Network communication


@dataclass
class Component:
    """Represents a SCADA component"""
    id: str
    name: str
    component_type: ComponentType
    location: str
    latitude: float
    longitude: float
    capacity: float = None
    unit: str = None
    operational_status: str = "active"
    installed_date: str = None
    metadata: Dict = None

    def to_dict(self):
        data = asdict(self)
        data['component_type'] = self.component_type.value
        if self.metadata is None:
            data['metadata'] = {}
        return data


@dataclass
class Connection:
    """Represents a connection between two components"""
    source_id: str
    target_id: str
    connection_type: ConnectionType
    flow_direction: str = "bidirectional"  # directional, unidirectional, bidirectional
    capacity: float = None
    length_km: float = None
    diameter_inches: float = None
    material: str = None
    metadata: Dict = None

    def to_dict(self):
        data = asdict(self)
        data['connection_type'] = self.connection_type.value
        if self.metadata is None:
            data['metadata'] = {}
        return data


class SCADAGraphDatabase:
    """
    Graph database for Pacific Water SCADA system
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.components: Dict[str, Component] = {}
        self.connections: List[Connection] = []

    def add_component(self, component: Component) -> None:
        """Add a component node to the graph"""
        self.components[component.id] = component
        self.graph.add_node(
            component.id,
            **component.to_dict()
        )

    def add_connection(self, connection: Connection) -> None:
        """Add a connection edge to the graph"""
        self.connections.append(connection)
        self.graph.add_edge(
            connection.source_id,
            connection.target_id,
            **connection.to_dict()
        )

    def get_component(self, component_id: str) -> Component:
        """Retrieve a component by ID"""
        return self.components.get(component_id)

    def get_neighbors(self, component_id: str) -> List[str]:
        """Get all connected components"""
        return list(self.graph.neighbors(component_id))

    def get_subgraph_by_type(self, component_type: ComponentType) -> nx.DiGraph:
        """Get subgraph containing only components of a specific type"""
        nodes = [
            node_id for node_id, node_data in self.graph.nodes(data=True)
            if node_data.get('component_type') == component_type.value
        ]
        return self.graph.subgraph(nodes)

    def find_paths(self, source_id: str, target_id: str) -> List[List[str]]:
        """Find all paths between two components"""
        try:
            return list(nx.all_simple_paths(self.graph, source_id, target_id))
        except nx.NetworkXNoPath:
            return []

    def get_graph_statistics(self) -> Dict:
        """Get statistics about the graph"""
        return {
            'total_components': self.graph.number_of_nodes(),
            'total_connections': self.graph.number_of_edges(),
            'network_diameter': nx.diameter(self.graph.to_undirected()) 
                if nx.is_connected(self.graph.to_undirected()) else None,
            'average_clustering_coefficient': nx.average_clustering(
                self.graph.to_undirected()
            ),
            'component_types': self._count_by_type(),
            'connection_types': self._count_connections_by_type()
        }

    def _count_by_type(self) -> Dict[str, int]:
        """Count components by type"""
        counts = {}
        for component in self.components.values():
            type_name = component.component_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def _count_connections_by_type(self) -> Dict[str, int]:
        """Count connections by type"""
        counts = {}
        for conn in self.connections:
            type_name = conn.connection_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts

    def to_json(self) -> str:
        """Export graph to JSON format"""
        data = {
            'metadata': {
                'system': 'Pacific Water SCADA',
                'city': 'West Pacific',
                'population': 10000,
                'created_date': datetime.now().isoformat(),
                'graph_statistics': self.get_graph_statistics()
            },
            'components': [component.to_dict() for component in self.components.values()],
            'connections': [conn.to_dict() for conn in self.connections]
        }
        return json.dumps(data, indent=2, default=str)

    def export_to_neo4j_cypher(self) -> str:
        """Generate Neo4j Cypher commands"""
        cypher_commands = [
            "// Create SCADA Graph Database for Pacific Water",
            "// Clear existing data",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// Create components"
        ]

        for component in self.components.values():
            props = component.to_dict()
            props_str = ", ".join([
                f"{k}: {json.dumps(v)}" if not isinstance(v, (int, float))
                else f"{k}: {v}"
                for k, v in props.items()
            ])
            cypher_commands.append(
                f"CREATE (:{component.component_type.value.upper()} {{{props_str}}});"
            )

        cypher_commands.append("\n// Create connections")
        for i, conn in enumerate(self.connections):
            cypher_commands.append(
                f"MATCH (a {{id: '{conn.source_id}'}}), (b {{id: '{conn.target_id}'}}) "
                f"CREATE (a)-[:{conn.connection_type.value.upper()} {{"
                f"flow_direction: '{conn.flow_direction}'"
                f"}}]->(b);"
            )

        return "\n".join(cypher_commands)

    def visualize(self, output_file: str = None):
        """Visualize the graph (requires matplotlib and networkx)"""
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(16, 12))
            pos = nx.spring_layout(self.graph, k=2, iterations=50)
            
            # Color nodes by type
            color_map = {
                'treatment_plant': '#FF6B6B',
                'pumping_station': '#4ECDC4',
                'reservoir': '#45B7D1',
                'distribution_main': '#96CEB4',
                'customer_zone': '#FFEAA7',
                'rtu': '#DFE6E9',
                'scada_server': '#A29BFE',
                'monitoring_station': '#FD79A8'
            }
            
            colors = [
                color_map.get(self.graph.nodes[node].get('component_type'), '#95E1D3')
                for node in self.graph.nodes()
            ]
            
            nx.draw_networkx_nodes(self.graph, pos, node_color=colors, 
                                  node_size=800, alpha=0.9)
            nx.draw_networkx_edges(self.graph, pos, edge_color='gray', 
                                  arrows=True, arrowsize=20, alpha=0.6)
            nx.draw_networkx_labels(self.graph, pos, font_size=8)
            
            plt.title("Pacific Water SCADA System Network Graph", fontsize=16, fontweight='bold')
            plt.axis('off')
            
            if output_file:
                plt.savefig(output_file, dpi=300, bbox_inches='tight')
                print(f"Graph saved to {output_file}")
            else:
                plt.show()
                
        except ImportError:
            print("Visualization requires matplotlib. Install with: pip install matplotlib")


def create_pacific_water_scada() -> SCADAGraphDatabase:
    """
    Create a complete SCADA graph for Pacific Water serving West Pacific
    """
    scada = SCADAGraphDatabase()

    # Create Treatment Plant
    scada.add_component(Component(
        id="tp_001",
        name="West Pacific Water Treatment Plant",
        component_type=ComponentType.TREATMENT_PLANT,
        location="123 Water Works Road, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        capacity=5000,  # gallons per minute
        unit="gpm",
        installed_date="2015-03-15"
    ))

    # Create SCADA Server
    scada.add_component(Component(
        id="scada_srv_001",
        name="Central SCADA Server",
        component_type=ComponentType.SCADA_SERVER,
        location="123 Water Works Road, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2018-06-20"
    ))

    # PacCom communication backbone nodes (multi‑hub model)
    scada.add_component(Component(
        id="paccom_001",
        name="PacCom Central Gateway",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="100 Power Rd, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        metadata={"provider":"PacCom", "type":"fiber/5G", "bandwidth_gbps":100}
    ))
    scada.add_component(Component(
        id="paccom_002",
        name="PacCom West Hub",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="Maunaloa Ridge, Molokai, HI",
        latitude=21.2156,
        longitude=-157.1298,
        metadata={"provider":"PacCom", "type":"fiber/5G", "bandwidth_gbps":40}
    ))
    scada.add_component(Component(
        id="paccom_003",
        name="PacCom East Tower",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="East End Rd, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        metadata={"provider":"PacCom", "type":"5G", "bandwidth_gbps":20}
    ))

    # interconnect the PacCom nodes
    scada.add_connection(Connection(
        source_id="paccom_001",
        target_id="paccom_002",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional",
        metadata={"link":"fiber_trunk"}
    ))
    scada.add_connection(Connection(
        source_id="paccom_001",
        target_id="paccom_003",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional",
        metadata={"link":"fiber_trunk"}
    ))

    # link SCADA server to central gateway
    scada.add_connection(Connection(
        source_id="scada_srv_001",
        target_id="paccom_001",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional"
    ))

    # Create Primary Pumping Stations
    scada.add_component(Component(
        id="ps_001",
        name="Primary Pumping Station - North",
        component_type=ComponentType.PUMPING_STATION,
        location="456 North Shore Road, Molokai, HI",
        latitude=21.2482,
        longitude=-157.0623,
        capacity=3000,
        unit="gpm",
        installed_date="2016-09-10"
    ))

    scada.add_component(Component(
        id="ps_002",
        name="Secondary Pumping Station - East",
        component_type=ComponentType.PUMPING_STATION,
        location="789 East End Road, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        capacity=2000,
        unit="gpm",
        installed_date="2017-11-05"
    ))

    # Create Reservoirs
    scada.add_component(Component(
        id="res_001",
        name="North Storage Reservoir",
        component_type=ComponentType.RESERVOIR,
        location="500 North Shore Road, Molokai, HI",
        latitude=21.2561,
        longitude=-157.0854,
        capacity=1000000,  # gallons
        unit="gallons",
        installed_date="2010-01-20"
    ))

    scada.add_component(Component(
        id="res_002",
        name="East Storage Reservoir",
        component_type=ComponentType.RESERVOIR,
        location="800 East End Road, Molokai, HI",
        latitude=21.1802,
        longitude=-156.8567,
        capacity=500000,
        unit="gallons",
        installed_date="2012-05-15"
    ))

    # Create Distribution Mains
    scada.add_component(Component(
        id="dm_001",
        name="Main Distribution Line - North",
        component_type=ComponentType.DISTRIBUTION_MAIN,
        location="North Shore zone, Molokai, HI",
        latitude=21.2312,
        longitude=-157.0736,
        metadata={"diameter_inches": 12, "length_km": 4.5}
    ))

    scada.add_component(Component(
        id="dm_002",
        name="Main Distribution Line - East",
        component_type=ComponentType.DISTRIBUTION_MAIN,
        location="East End zone, Molokai, HI",
        latitude=21.1834,
        longitude=-156.8756,
        metadata={"diameter_inches": 10, "length_km": 3.2}
    ))

    scada.add_component(Component(
        id="dm_003",
        name="Main Distribution Line - Central",
        component_type=ComponentType.DISTRIBUTION_MAIN,
        location="Central zone, Kaunakakai, Molokai, HI",
        latitude=21.1923,
        longitude=-157.0621,
        metadata={"diameter_inches": 14, "length_km": 2.8}
    ))

    # Create Customer Zones
    scada.add_component(Component(
        id="cz_001",
        name="Residential Zone - North",
        component_type=ComponentType.CUSTOMER_ZONE,
        location="Maunaloa, North Molokai, HI",
        latitude=21.2156,
        longitude=-157.1298,
        metadata={"customers": 2500, "avg_consumption_gpm": 800}
    ))

    scada.add_component(Component(
        id="cz_002",
        name="Commercial Zone - Central",
        component_type=ComponentType.CUSTOMER_ZONE,
        location="Kaunakakai Downtown, Molokai, HI",
        latitude=21.1943,
        longitude=-157.0519,
        metadata={"customers": 1500, "avg_consumption_gpm": 600}
    ))

    scada.add_component(Component(
        id="cz_003",
        name="Industrial Zone - East",
        component_type=ComponentType.CUSTOMER_ZONE,
        location="Pukoo, East Molokai, HI",
        latitude=21.1745,
        longitude=-156.8234,
        metadata={"customers": 800, "avg_consumption_gpm": 500}
    ))

    scada.add_component(Component(
        id="cz_004",
        name="Residential Zone - South",
        component_type=ComponentType.CUSTOMER_ZONE,
        location="Mapulehu, South Molokai, HI",
        latitude=21.1621,
        longitude=-157.0345,
        metadata={"customers": 2200, "avg_consumption_gpm": 700}
    ))

    # Create Monitoring RTUs
    scada.add_component(Component(
        id="rtu_001",
        name="RTU - North Station",
        component_type=ComponentType.RTU,
        location="456 North Shore Road, Molokai, HI",
        latitude=21.2482,
        longitude=-157.0623,
        installed_date="2018-03-10"
    ))

    scada.add_component(Component(
        id="rtu_002",
        name="RTU - East Station",
        component_type=ComponentType.RTU,
        location="789 East End Road, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        installed_date="2018-03-10"
    ))

    scada.add_component(Component(
        id="rtu_003",
        name="RTU - North Reservoir",
        component_type=ComponentType.RTU,
        location="500 North Shore Road, Molokai, HI",
        latitude=21.2561,
        longitude=-157.0854,
        installed_date="2019-07-15"
    ))

    # Create Sensors and Instruments
    scada.add_component(Component(
        id="fm_001",
        name="Flow Meter - Treatment Plant Exit",
        component_type=ComponentType.FLOW_METER,
        location="Kaunakakai Treatment Plant",
        latitude=21.1952,
        longitude=-157.0547
    ))

    scada.add_component(Component(
        id="ls_001",
        name="Level Sensor - North Reservoir",
        component_type=ComponentType.LEVEL_SENSOR,
        location="North Shore Reservoir",
        latitude=21.2561,
        longitude=-157.0854
    ))

    scada.add_component(Component(
        id="ls_002",
        name="Level Sensor - East Reservoir",
        component_type=ComponentType.LEVEL_SENSOR,
        location="East End Reservoir",
        latitude=21.1802,
        longitude=-156.8567
    ))

    scada.add_component(Component(
        id="pg_001",
        name="Pressure Gauge - North Line",
        component_type=ComponentType.PRESSURE_GAUGE,
        location="North Shore Distribution Main",
        latitude=21.2312,
        longitude=-157.0736
    ))

    scada.add_component(Component(
        id="pg_002",
        name="Pressure Gauge - East Line",
        component_type=ComponentType.PRESSURE_GAUGE,
        location="East End Distribution Main",
        latitude=21.1834,
        longitude=-156.8756
    ))

    # Create Control Valves
    scada.add_component(Component(
        id="prv_001",
        name="Pressure Reducing Valve - North",
        component_type=ComponentType.PRESSURE_REDUCING_VALVE,
        location="North Shore PRV Station, Molokai, HI",
        latitude=21.2234,
        longitude=-157.0892
    ))

    scada.add_component(Component(
        id="cv_001",
        name="Check Valve - Pump Station North",
        component_type=ComponentType.CHECK_VALVE,
        location="North Pumping Station, Molokai, HI",
        latitude=21.2482,
        longitude=-157.0623
    ))

    scada.add_component(Component(
        id="iv_001",
        name="Isolation Valve - North Main",
        component_type=ComponentType.ISOLATION_VALVE,
        location="North Shore Main Valve Station, Molokai, HI",
        latitude=21.2401,
        longitude=-157.0679
    ))

    # Create Connections (Hydraulic - water flow)
    # Treatment Plant to Distribution
    scada.add_connection(Connection(
        source_id="tp_001",
        target_id="ps_001",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=3000,
        diameter_inches=12,
        length_km=1.2,
        material="PVC"
    ))

    scada.add_connection(Connection(
        source_id="tp_001",
        target_id="ps_002",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=2000,
        diameter_inches=10,
        length_km=1.8,
        material="PVC"
    ))

    # Pump Stations to Reservoirs
    scada.add_connection(Connection(
        source_id="ps_001",
        target_id="res_001",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=3000,
        diameter_inches=10,
        length_km=0.3,
        material="Steel"
    ))

    scada.add_connection(Connection(
        source_id="ps_002",
        target_id="res_002",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=2000,
        diameter_inches=8,
        length_km=0.5,
        material="Steel"
    ))

    # Reservoirs to Distribution Mains
    scada.add_connection(Connection(
        source_id="res_001",
        target_id="dm_001",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=2500,
        diameter_inches=12,
        length_km=0.4,
        material="PVC"
    ))

    scada.add_connection(Connection(
        source_id="res_002",
        target_id="dm_002",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=1500,
        diameter_inches=10,
        length_km=0.3,
        material="PVC"
    ))

    scada.add_connection(Connection(
        source_id="res_001",
        target_id="dm_003",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=2000,
        diameter_inches=12,
        length_km=0.6,
        material="PVC"
    ))

    # Distribution Mains to Customer Zones
    scada.add_connection(Connection(
        source_id="dm_001",
        target_id="cz_001",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=800,
        diameter_inches=8,
        length_km=1.2,
        material="PVC"
    ))

    scada.add_connection(Connection(
        source_id="dm_003",
        target_id="cz_002",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=600,
        diameter_inches=6,
        length_km=0.8,
        material="PVC"
    ))

    scada.add_connection(Connection(
        source_id="dm_002",
        target_id="cz_003",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=500,
        diameter_inches=6,
        length_km=1.5,
        material="PVC"
    ))

    scada.add_connection(Connection(
        source_id="dm_001",
        target_id="cz_004",
        connection_type=ConnectionType.HYDRAULIC,
        flow_direction="unidirectional",
        capacity=700,
        diameter_inches=8,
        length_km=1.8,
        material="PVC"
    ))

    # SCADA Control Connections
    scada.add_connection(Connection(
        source_id="scada_srv_001",
        target_id="rtu_001",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    scada.add_connection(Connection(
        source_id="scada_srv_001",
        target_id="rtu_002",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    scada.add_connection(Connection(
        source_id="scada_srv_001",
        target_id="rtu_003",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    # PacCom links for RTUs (communications backbone dependency)
    # North & East RTUs connect to West Hub for redundancy, South RTU to East Tower
    scada.add_connection(Connection(
        source_id="rtu_001",
        target_id="paccom_002",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional"
    ))
    scada.add_connection(Connection(
        source_id="rtu_002",
        target_id="paccom_002",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional"
    ))
    scada.add_connection(Connection(
        source_id="rtu_003",
        target_id="paccom_003",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional"
    ))

    # RTU to Pumping Stations
    scada.add_connection(Connection(
        source_id="rtu_001",
        target_id="ps_001",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    scada.add_connection(Connection(
        source_id="rtu_002",
        target_id="ps_002",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    # Monitoring connections - Sensors to RTUs
    scada.add_connection(Connection(
        source_id="fm_001",
        target_id="rtu_001",
        connection_type=ConnectionType.MONITORING,
        flow_direction="unidirectional"
    ))

    scada.add_connection(Connection(
        source_id="ls_001",
        target_id="rtu_003",
        connection_type=ConnectionType.MONITORING,
        flow_direction="unidirectional"
    ))

    scada.add_connection(Connection(
        source_id="ls_002",
        target_id="rtu_002",
        connection_type=ConnectionType.MONITORING,
        flow_direction="unidirectional"
    ))

    scada.add_connection(Connection(
        source_id="pg_001",
        target_id="rtu_001",
        connection_type=ConnectionType.MONITORING,
        flow_direction="unidirectional"
    ))

    scada.add_connection(Connection(
        source_id="pg_002",
        target_id="rtu_002",
        connection_type=ConnectionType.MONITORING,
        flow_direction="unidirectional"
    ))

    # Control valve connections
    scada.add_connection(Connection(
        source_id="rtu_001",
        target_id="prv_001",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    scada.add_connection(Connection(
        source_id="rtu_001",
        target_id="cv_001",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    scada.add_connection(Connection(
        source_id="rtu_001",
        target_id="iv_001",
        connection_type=ConnectionType.CONTROL,
        flow_direction="bidirectional"
    ))

    return scada


if __name__ == "__main__":
    # Create the SCADA system
    scada = create_pacific_water_scada()
    
    # Print statistics
    print("Pacific Water SCADA System - Graph Database")
    print("=" * 60)
    stats = scada.get_graph_statistics()
    print(f"Total Components: {stats['total_components']}")
    print(f"Total Connections: {stats['total_connections']}")
    print(f"\nComponent Distribution:")
    for comp_type, count in stats['component_types'].items():
        print(f"  {comp_type}: {count}")
    print(f"\nConnection Distribution:")
    for conn_type, count in stats['connection_types'].items():
        print(f"  {conn_type}: {count}")
    
    # Export to JSON
    with open("pacific_water_scada_data.json", "w") as f:
        f.write(scada.to_json())
    print(f"\n✓ Graph data exported to: pacific_water_scada_data.json")
    
    # Export Neo4j Cypher
    with open("pacific_water_scada_neo4j.cypher", "w") as f:
        f.write(scada.export_to_neo4j_cypher())
    print(f"✓ Neo4j Cypher commands exported to: pacific_water_scada_neo4j.cypher")
    
    # Generate visualization
    try:
        scada.visualize("pacific_water_scada_visualization.png")
        print(f"✓ Graph visualization saved to: pacific_water_scada_visualization.png")
    except ImportError:
        print("⚠ Visualization skipped (requires matplotlib)")
    
    # Example queries
    print("\n" + "=" * 60)
    print("Example Graph Queries:")
    print("=" * 60)
    
    print("\n1. Find all components connected to SCADA Server:")
    neighbors = scada.get_neighbors("scada_srv_001")
    for neighbor_id in neighbors:
        component = scada.get_component(neighbor_id)
        if component:
            print(f"   - {component.name} ({neighbor_id})")
    
    print("\n2. Find paths from Treatment Plant to Customer Zones:")
    paths = scada.find_paths("tp_001", "cz_001")
    for i, path in enumerate(paths, 1):
        components_in_path = [scada.get_component(c).name for c in path]
        print(f"   Path {i}: {' -> '.join(components_in_path)}")
    
    print("\n3. All Pumping Stations:")
    pumps = scada.get_subgraph_by_type(ComponentType.PUMPING_STATION)
    for node in pumps.nodes():
        component = scada.get_component(node)
        print(f"   - {component.name}: {component.capacity} {component.unit}")
