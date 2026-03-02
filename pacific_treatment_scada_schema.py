"""
SCADA Graph Database Schema for Pacific Treatment Sewer/Wastewater Network
System for Molokai, HI

Note: all components rely on PacCom's communications backbone for SCADA control
"""

import networkx as nx
import json
from typing import Dict, List
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class ComponentType(Enum):
    """Types of components in the wastewater SCADA system"""
    TREATMENT_PLANT = "treatment_plant"
    LIFT_STATION = "lift_station"
    PUMPING_STATION = "pumping_station"
    SEWER_MAIN = "sewer_main"
    MANHOLE = "manhole"
    SCREENING = "screening"
    CLARIFIER = "clarifier"
    AERATION_TANK = "aeration_tank"
    EFFLUENT_OUTLET = "effluent_outlet"
    ODOR_CONTROL = "odor_control"
    RTU = "rtu"
    SCADA_SERVER = "scada_server"
    FLOW_METER = "flow_meter"
    LEVEL_SENSOR = "level_sensor"
    TURBIDITY_SENSOR = "turbidity_sensor"
    PRESSURE_GAUGE = "pressure_gauge"
    ISOLATION_VALVE = "isolation_valve"
    CHECK_VALVE = "check_valve"
    COMMUNICATION_NODE = "communication_node"


class ConnectionType(Enum):
    """Types of connections between components"""
    HYDRAULIC = "hydraulic"  # Sewage flow
    CONTROL = "control"     # SCADA control signal
    MONITORING = "monitoring"  # Data collection
    COMMUNICATION = "communication"  # Network communication


@dataclass
class Component:
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
    source_id: str
    target_id: str
    connection_type: ConnectionType
    flow_direction: str = "bidirectional"
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
    Generic graph database for SCADA systems
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.components: Dict[str, Component] = {}
        self.connections: List[Connection] = []

    def add_component(self, component: Component) -> None:
        self.components[component.id] = component
        self.graph.add_node(component.id, **component.to_dict())

    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
        self.graph.add_edge(connection.source_id, connection.target_id, **connection.to_dict())

    def get_component(self, component_id: str) -> Component:
        return self.components.get(component_id)

    def get_neighbors(self, component_id: str) -> List[str]:
        return list(self.graph.neighbors(component_id))

    def get_subgraph_by_type(self, component_type: ComponentType) -> nx.DiGraph:
        nodes = [nid for nid, data in self.graph.nodes(data=True) if data.get('component_type') == component_type.value]
        return self.graph.subgraph(nodes)

    def find_paths(self, source_id: str, target_id: str) -> List[List[str]]:
        try:
            return list(nx.all_simple_paths(self.graph, source_id, target_id))
        except nx.NetworkXNoPath:
            return []

    def get_graph_statistics(self) -> Dict:
        return {
            'total_components': self.graph.number_of_nodes(),
            'total_connections': self.graph.number_of_edges(),
            'network_diameter': nx.diameter(self.graph.to_undirected()) if nx.is_connected(self.graph.to_undirected()) else None,
            'average_clustering_coefficient': nx.average_clustering(self.graph.to_undirected()),
            'component_types': self._count_by_type(),
            'connection_types': self._count_connections_by_type()
        }

    def _count_by_type(self) -> Dict[str, int]:
        counts = {}
        for c in self.components.values():
            t = c.component_type.value
            counts[t] = counts.get(t, 0) + 1
        return counts

    def _count_connections_by_type(self) -> Dict[str, int]:
        counts = {}
        for conn in self.connections:
            t = conn.connection_type.value
            counts[t] = counts.get(t, 0) + 1
        return counts

    def to_json(self) -> str:
        data = {
            'metadata': {
                'system': 'Pacific Treatment SCADA',
                'service': 'Sewer & Wastewater',
                'city': 'Molokai',
                'created_date': datetime.now().isoformat(),
                'graph_statistics': self.get_graph_statistics()
            },
            'components': [c.to_dict() for c in self.components.values()],
            'connections': [conn.to_dict() for conn in self.connections]
        }
        return json.dumps(data, indent=2, default=str)

    def export_to_neo4j_cypher(self) -> str:
        commands = [
            "// Pacific Treatment SCADA Database",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// Create components"
        ]
        for comp in self.components.values():
            props = comp.to_dict()
            props_str = ", ".join([f"{k}: {json.dumps(v)}" if not isinstance(v,(int,float)) else f"{k}: {v}" for k,v in props.items()])
            commands.append(f"CREATE (:{comp.component_type.value.upper()} {{{props_str}}});")
        commands.append("\n// Create connections")
        for conn in self.connections:
            commands.append(
                f"MATCH (a {{id: '{conn.source_id}'}}), (b {{id: '{conn.target_id}'}}) CREATE (a)-[:{conn.connection_type.value.upper()} {{flow_direction: '{conn.flow_direction}'}}]->(b);"
            )
        return "\n".join(commands)

    def visualize(self, output_file: str = None):
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(16,12))
            pos = nx.spring_layout(self.graph, k=2, iterations=50)
            color_map = { 'treatment_plant':'#FF6B6B','lift_station':'#4ECDC4','pumping_station':'#45B7D1','sewer_main':'#96CEB4','manhole':'#FFEAA7','rtu':'#DFE6E9','scada_server':'#A29BFE'}
            colors = [color_map.get(self.graph.nodes[n].get('component_type'),'#95E1D3') for n in self.graph.nodes()]
            nx.draw_networkx_nodes(self.graph,pos,node_color=colors,node_size=800,alpha=0.9)
            nx.draw_networkx_edges(self.graph,pos,edge_color='gray',arrows=True,arrowsize=20,alpha=0.6)
            nx.draw_networkx_labels(self.graph,pos,font_size=8)
            plt.title("Pacific Treatment SCADA Sewer Network",fontsize=16,fontweight='bold')
            plt.axis('off')
            if output_file:
                plt.savefig(output_file,dpi=300,bbox_inches='tight')
                print(f"Graph saved to {output_file}")
            else:
                plt.show()
        except ImportError:
            print("Visualization requires matplotlib. Install with: pip install matplotlib")


def create_pacific_treatment_scada() -> SCADAGraphDatabase:
    scada = SCADAGraphDatabase()
    # treatment plant
    scada.add_component(Component(
        id="tp_001",
        name="Molokai Wastewater Treatment Plant",
        component_type=ComponentType.TREATMENT_PLANT,
        location="500 Treatment Rd, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        capacity=3000,
        unit="gpm",
        installed_date="2014-07-01"
    ))
    # scada server
    scada.add_component(Component(
        id="scada_srv_001",
        name="Central SCADA Server",
        component_type=ComponentType.SCADA_SERVER,
        location="500 Treatment Rd, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2017-02-10"
    ))

    # PacCom backbone nodes (multi-hub)
    scada.add_component(Component(
        id="paccom_001",
        name="PacCom Central Gateway",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="100 Power Rd, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        metadata={"provider":"PacCom","type":"fiber/5G","bandwidth_gbps":100}
    ))
    scada.add_component(Component(
        id="paccom_002",
        name="PacCom North Tower",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="North Shore Rd, Molokai, HI",
        latitude=21.2482,
        longitude=-157.0623,
        metadata={"provider":"PacCom","type":"5G","bandwidth_gbps":30}
    ))
    scada.add_component(Component(
        id="paccom_003",
        name="PacCom East Hub",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="East End Rd, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        metadata={"provider":"PacCom","type":"fiber/5G","bandwidth_gbps":20}
    ))

    # interconnect PacCom nodes
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

    # connect SCADA server to central PacCom
    scada.add_connection(Connection(
        source_id="scada_srv_001",
        target_id="paccom_001",
        connection_type=ConnectionType.COMMUNICATION,
        flow_direction="bidirectional"
    ))
    # lift stations / pumps
    scada.add_component(Component(
        id="ls_001",
        name="Lift Station - North Shore",
        component_type=ComponentType.LIFT_STATION,
        location="900 North Shore Rd, Molokai, HI",
        latitude=21.2482,
        longitude=-157.0623,
        capacity=1500,
        unit="gpm",
        installed_date="2016-05-20"
    ))
    scada.add_component(Component(
        id="ls_002",
        name="Lift Station - East End",
        component_type=ComponentType.LIFT_STATION,
        location="1200 East End Rd, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        capacity=1000,
        unit="gpm",
        installed_date="2016-05-20"
    ))
    # sewer mains
    scada.add_component(Component(
        id="sm_001",
        name="Sewer Main - North",
        component_type=ComponentType.SEWER_MAIN,
        location="North Shore corridor",
        latitude=21.2312,
        longitude=-157.0736,
        metadata={"diameter_inches":36,"length_km":5.0}
    ))
    scada.add_component(Component(
        id="sm_002",
        name="Sewer Main - Central",
        component_type=ComponentType.SEWER_MAIN,
        location="Kaunakakai town",
        latitude=21.1923,
        longitude=-157.0621,
        metadata={"diameter_inches":42,"length_km":3.0}
    ))
    scada.add_component(Component(
        id="sm_003",
        name="Sewer Main - East",
        component_type=ComponentType.SEWER_MAIN,
        location="East End corridor",
        latitude=21.1834,
        longitude=-156.8756,
        metadata={"diameter_inches":30,"length_km":4.0}
    ))
    # manholes (represent zones)
    scada.add_component(Component(
        id="mh_001",
        name="Manhole - Maunaloa Residential",
        component_type=ComponentType.MANHOLE,
        location="Maunaloa",
        latitude=21.2156,
        longitude=-157.1298
    ))
    scada.add_component(Component(
        id="mh_002",
        name="Manhole - Kaunakakai Commercial",
        component_type=ComponentType.MANHOLE,
        location="Kaunakakai Downtown",
        latitude=21.1943,
        longitude=-157.0519
    ))
    scada.add_component(Component(
        id="mh_003",
        name="Manhole - Pukoo Industrial",
        component_type=ComponentType.MANHOLE,
        location="Pukoo",
        latitude=21.1745,
        longitude=-156.8234
    ))
    scada.add_component(Component(
        id="mh_004",
        name="Manhole - Mapulehu South",
        component_type=ComponentType.MANHOLE,
        location="Mapulehu",
        latitude=21.1621,
        longitude=-157.0345
    ))
    # sensors
    scada.add_component(Component(
        id="fm_001",
        name="Flow Meter - North Main",
        component_type=ComponentType.FLOW_METER,
        location="North Shore main",
        latitude=21.2312,
        longitude=-157.0736
    ))
    scada.add_component(Component(
        id="ls_003",
        name="Level Sensor - North Lift Station",
        component_type=ComponentType.LEVEL_SENSOR,
        location="North Shore lift",
        latitude=21.2482,
        longitude=-157.0623
    ))
    scada.add_component(Component(
        id="ts_001",
        name="Turbidity Sensor - Treatment Plant Exit",
        component_type=ComponentType.TURBIDITY_SENSOR,
        location="Treatment Plant",
        latitude=21.1952,
        longitude=-157.0547
    ))
    scada.add_component(Component(
        id="pg_001",
        name="Pressure Gauge - East Main",
        component_type=ComponentType.PRESSURE_GAUGE,
        location="East corridor",
        latitude=21.1834,
        longitude=-156.8756
    ))
    # control valves
    scada.add_component(Component(
        id="iv_001",
        name="Isolation Valve - North Main",
        component_type=ComponentType.ISOLATION_VALVE,
        location="North main junction",
        latitude=21.2401,
        longitude=-157.0679
    ))
    scada.add_component(Component(
        id="cv_001",
        name="Check Valve - North Lift",
        component_type=ComponentType.CHECK_VALVE,
        location="North lift station",
        latitude=21.2482,
        longitude=-157.0623
    ))
    # RTUs
    scada.add_component(Component(
        id="rtu_001",
        name="RTU - Treatment Plant",
        component_type=ComponentType.RTU,
        location="Treat Plant",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2017-02-10"
    ))
    scada.add_component(Component(
        id="rtu_002",
        name="RTU - North Lift",
        component_type=ComponentType.RTU,
        location="North Shore",
        latitude=21.2482,
        longitude=-157.0623,
        installed_date="2017-02-10"
    ))
    scada.add_component(Component(
        id="rtu_003",
        name="RTU - East Lift",
        component_type=ComponentType.RTU,
        location="East End",
        latitude=21.1865,
        longitude=-156.8945,
        installed_date="2017-02-10"
    ))
    # control connections
    scada.add_connection(Connection(source_id="scada_srv_001", target_id="rtu_001", connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="scada_srv_001", target_id="rtu_002", connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="scada_srv_001", target_id="rtu_003", connection_type=ConnectionType.CONTROL))

    # RTUs communicate over PacCom backbone (distributed)
    scada.add_connection(Connection(source_id="rtu_001", target_id="paccom_002", connection_type=ConnectionType.COMMUNICATION))
    scada.add_connection(Connection(source_id="rtu_002", target_id="paccom_003", connection_type=ConnectionType.COMMUNICATION))
    scada.add_connection(Connection(source_id="rtu_003", target_id="paccom_002", connection_type=ConnectionType.COMMUNICATION))
    scada.add_connection(Connection(source_id="rtu_002", target_id="ls_001", connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="rtu_003", target_id="ls_002", connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="rtu_001", target_id="iv_001", connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="rtu_002", target_id="cv_001", connection_type=ConnectionType.CONTROL))
    # monitoring
    scada.add_connection(Connection(source_id="fm_001", target_id="rtu_001", connection_type=ConnectionType.MONITORING, flow_direction="unidirectional"))
    scada.add_connection(Connection(source_id="ls_003", target_id="rtu_002", connection_type=ConnectionType.MONITORING, flow_direction="unidirectional"))
    scada.add_connection(Connection(source_id="ts_001", target_id="rtu_001", connection_type=ConnectionType.MONITORING, flow_direction="unidirectional"))
    scada.add_connection(Connection(source_id="pg_001", target_id="rtu_003", connection_type=ConnectionType.MONITORING, flow_direction="unidirectional"))
    # hydraulic flow
    scada.add_connection(Connection(source_id="tp_001", target_id="ls_001", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=1500, diameter_inches=36, length_km=2.0, material="PVC"))
    scada.add_connection(Connection(source_id="tp_001", target_id="ls_002", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=1000, diameter_inches=30, length_km=2.5, material="PVC"))
    scada.add_connection(Connection(source_id="ls_001", target_id="sm_001", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=1500))
    scada.add_connection(Connection(source_id="ls_002", target_id="sm_003", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=1000))
    scada.add_connection(Connection(source_id="sm_001", target_id="mh_001", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=800))
    scada.add_connection(Connection(source_id="sm_002", target_id="mh_002", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=600))
    scada.add_connection(Connection(source_id="sm_003", target_id="mh_003", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=500))
    scada.add_connection(Connection(source_id="sm_001", target_id="mh_004", connection_type=ConnectionType.HYDRAULIC, flow_direction="unidirectional", capacity=700))
    return scada


if __name__ == "__main__":
    scada = create_pacific_treatment_scada()
    print("Pacific Treatment SCADA System - Graph Database")
    print("="*60)
    stats = scada.get_graph_statistics()
    print(f"Total Components: {stats['total_components']}")
    print(f"Total Connections: {stats['total_connections']}")
    print("\nComponent Distribution:")
    for t,c in stats['component_types'].items():
        print(f"  {t}: {c}")
    print("\nConnection Distribution:")
    for t,c in stats['connection_types'].items():
        print(f"  {t}: {c}")
    with open("pacific_treatment_scada_data.json","w") as f:
        f.write(scada.to_json())
    print("\n✓ Graph data exported to: pacific_treatment_scada_data.json")
    with open("pacific_treatment_scada_neo4j.cypher","w") as f:
        f.write(scada.export_to_neo4j_cypher())
    print("✓ Neo4j Cypher commands exported to: pacific_treatment_scada_neo4j.cypher")
    try:
        scada.visualize("pacific_treatment_scada_visualization.png")
        print("✓ Graph visualization saved to: pacific_treatment_scada_visualization.png")
    except ImportError:
        print("⚠ Visualization skipped (requires matplotlib)")
    # generate csv outputs as well
    import csv
    comp_fields=['id','name','component_type','location','latitude','longitude','capacity','unit','operational_status','installed_date']
    with open('pacific_treatment_components.csv','w',newline='') as cf:
        w=csv.DictWriter(cf,fieldnames=comp_fields)
        w.writeheader()
        for comp in scada.components.values():
            r=comp.to_dict()
            w.writerow({k:r.get(k) for k in comp_fields})
    conn_fields=['source_id','target_id','connection_type','flow_direction','capacity','length_km','diameter_inches','material']
    with open('pacific_treatment_connections.csv','w',newline='') as cf2:
        w2=csv.DictWriter(cf2,fieldnames=conn_fields)
        w2.writeheader()
        for conn in scada.connections:
            r=conn.to_dict()
            w2.writerow({k:r.get(k) for k in conn_fields})
    print("\n✓ CSV exports: pacific_treatment_components.csv, pacific_treatment_connections.csv")
