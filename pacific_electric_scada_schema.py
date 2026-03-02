"""
SCADA Graph Database Schema for Pacific Electric Distribution Network
System for Molokai, HI

Note: communications are provided by PacCom's island-wide network
"""

import networkx as nx
import json
from typing import Dict, List
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class ComponentType(Enum):
    """Types of components in the electric SCADA system"""
    SUBSTATION = "substation"
    TRANSFORMER = "transformer"
    TRANSMISSION_LINE = "transmission_line"
    DISTRIBUTION_FEEDER = "distribution_feeder"
    DISTRIBUTION_POLE = "distribution_pole"
    BREAKER = "breaker"
    METER = "meter"
    SCADA_SERVER = "scada_server"
    RTU = "rtu"
    VOLTAGE_SENSOR = "voltage_sensor"
    CURRENT_SENSOR = "current_sensor"
    TEMPERATURE_SENSOR = "temperature_sensor"
    COMMUNICATION_NODE = "communication_node"


class ConnectionType(Enum):
    """Types of connections between components"""
    ELECTRICAL = "electrical"  # power flow
    CONTROL = "control"        # SCADA control signal
    MONITORING = "monitoring"  # data collection
    COMMUNICATION = "communication"  # network link


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
    voltage_kv: float = None
    metadata: Dict = None

    def to_dict(self):
        data = asdict(self)
        data['connection_type'] = self.connection_type.value
        if self.metadata is None:
            data['metadata'] = {}
        return data


class SCADAGraphDatabase:
    """Generic graph database for SCADA systems"""

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
        nodes = [nid for nid,data in self.graph.nodes(data=True) if data.get('component_type')==component_type.value]
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

    def _count_by_type(self) -> Dict[str,int]:
        counts={}
        for c in self.components.values():
            t=c.component_type.value
            counts[t]=counts.get(t,0)+1
        return counts

    def _count_connections_by_type(self) -> Dict[str,int]:
        counts={}
        for conn in self.connections:
            t=conn.connection_type.value
            counts[t]=counts.get(t,0)+1
        return counts

    def to_json(self) -> str:
        data={
            'metadata':{
                'system':'Pacific Electric SCADA',
                'service':'Electric Distribution',
                'city':'Molokai',
                'created_date':datetime.now().isoformat(),
                'graph_statistics':self.get_graph_statistics()
            },
            'components':[c.to_dict() for c in self.components.values()],
            'connections':[conn.to_dict() for conn in self.connections]
        }
        return json.dumps(data,indent=2,default=str)

    def export_to_neo4j_cypher(self) -> str:
        cmds=[
            "// Pacific Electric SCADA Database",
            "MATCH (n) DETACH DELETE n;",
            "",
            "// Create components"
        ]
        for comp in self.components.values():
            props=comp.to_dict()
            props_str=", ".join([f"{k}: {json.dumps(v)}" if not isinstance(v,(int,float)) else f"{k}: {v}" for k,v in props.items()])
            cmds.append(f"CREATE (:{comp.component_type.value.upper()} {{{props_str}}});")
        cmds.append("\n// Create connections")
        for conn in self.connections:
            cmds.append(
                f"MATCH (a {{id: '{conn.source_id}'}}),(b {{id:'{conn.target_id}'}}) CREATE (a)-[:{conn.connection_type.value.upper()} {{flow_direction:'{conn.flow_direction}'}}]->(b);"
            )
        return "\n".join(cmds)

    def visualize(self,output_file:str=None):
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(16,12))
            pos=nx.spring_layout(self.graph,k=2,iterations=50)
            color_map={
                'substation':'#FF6B6B','transformer':'#4ECDC4','transmission_line':'#45B7D1',
                'distribution_feeder':'#96CEB4','meter':'#FFEAA7','rtu':'#DFE6E9','scada_server':'#A29BFE'
            }
            colors=[color_map.get(self.graph.nodes[n].get('component_type'),'#95E1D3') for n in self.graph.nodes()]
            nx.draw_networkx_nodes(self.graph,pos,node_color=colors,node_size=800,alpha=0.9)
            nx.draw_networkx_edges(self.graph,pos,edge_color='gray',arrows=True,arrowsize=20,alpha=0.6)
            nx.draw_networkx_labels(self.graph,pos,font_size=8)
            plt.title("Pacific Electric SCADA Network",fontsize=16,fontweight='bold')
            plt.axis('off')
            if output_file:
                plt.savefig(output_file,dpi=300,bbox_inches='tight')
                print(f"Graph saved to {output_file}")
            else:
                plt.show()
        except ImportError:
            print("Visualization requires matplotlib. Install with: pip install matplotlib")


def create_pacific_electric_scada() -> SCADAGraphDatabase:
    scada=SCADAGraphDatabase()
    # substations
    scada.add_component(Component(
        id="sub_001",
        name="Kaunakakai Substation",
        component_type=ComponentType.SUBSTATION,
        location="100 Power Rd, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        capacity=5000,
        unit="kW",
        installed_date="2013-04-01"
    ))
    scada.add_component(Component(
        id="sub_002",
        name="East End Substation",
        component_type=ComponentType.SUBSTATION,
        location="1400 East End Rd, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        capacity=3000,
        unit="kW",
        installed_date="2013-04-01"
    ))
    # feeders
    scada.add_component(Component(
        id="fd_001",
        name="Feeder - North Shore",
        component_type=ComponentType.DISTRIBUTION_FEEDER,
        location="North Shore corridor",
        latitude=21.2312,
        longitude=-157.0736,
        metadata={"voltage_kv":12, "length_km":5}
    ))
    scada.add_component(Component(
        id="fd_002",
        name="Feeder - Central",
        component_type=ComponentType.DISTRIBUTION_FEEDER,
        location="Kaunakakai town",
        latitude=21.1923,
        longitude=-157.0621,
        metadata={"voltage_kv":12, "length_km":3}
    ))
    scada.add_component(Component(
        id="fd_003",
        name="Feeder - East End",
        component_type=ComponentType.DISTRIBUTION_FEEDER,
        location="East End corridor",
        latitude=21.1834,
        longitude=-156.8756,
        metadata={"voltage_kv":12, "length_km":4}
    ))
    # transformers
    scada.add_component(Component(
        id="tr_001",
        name="Transformer - Maunaloa",
        component_type=ComponentType.TRANSFORMER,
        location="Maunaloa",
        latitude=21.2156,
        longitude=-157.1298,
        capacity=1000,
        unit="kVA"
    ))
    scada.add_component(Component(
        id="tr_002",
        name="Transformer - Pukoo",
        component_type=ComponentType.TRANSFORMER,
        location="Pukoo",
        latitude=21.1745,
        longitude=-156.8234,
        capacity=800,
        unit="kVA"
    ))
    # breakers
    scada.add_component(Component(
        id="br_001",
        name="Breaker - Kaunakakai Substation",
        component_type=ComponentType.BREAKER,
        location="Kaunakakai Substation",
        latitude=21.1952,
        longitude=-157.0547
    ))
    scada.add_component(Component(
        id="br_002",
        name="Breaker - East Substation",
        component_type=ComponentType.BREAKER,
        location="East End Substation",
        latitude=21.1865,
        longitude=-156.8945
    ))
    # meters
    scada.add_component(Component(
        id="mt_001",
        name="Meter - Maunaloa Residential",
        component_type=ComponentType.METER,
        location="Maunaloa",
        latitude=21.2156,
        longitude=-157.1298
    ))
    scada.add_component(Component(
        id="mt_002",
        name="Meter - Kaunakakai Commercial",
        component_type=ComponentType.METER,
        location="Kaunakakai Downtown",
        latitude=21.1943,
        longitude=-157.0519
    ))
    # sensors
    scada.add_component(Component(
        id="vs_001",
        name="Voltage Sensor - North Feeder",
        component_type=ComponentType.VOLTAGE_SENSOR,
        location="North Feeder",
        latitude=21.2312,
        longitude=-157.0736
    ))
    scada.add_component(Component(
        id="cs_001",
        name="Current Sensor - East Feeder",
        component_type=ComponentType.CURRENT_SENSOR,
        location="East Feeder",
        latitude=21.1834,
        longitude=-156.8756
    ))
    scada.add_component(Component(
        id="ts_001",
        name="Temperature Sensor - Transformer Pukoo",
        component_type=ComponentType.TEMPERATURE_SENSOR,
        location="Pukoo Transformer",
        latitude=21.1745,
        longitude=-156.8234
    ))
    # SCADA devices
    scada.add_component(Component(
        id="scada_srv_001",
        name="Central SCADA Server",
        component_type=ComponentType.SCADA_SERVER,
        location="100 Power Rd, Kaunakakai, Molokai, HI",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2017-01-15"
    ))

    # PacCom backbone nodes (central + regional)
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
        name="PacCom North Relay",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="North Shore Rd, Molokai, HI",
        latitude=21.2482,
        longitude=-157.0623,
        metadata={"provider":"PacCom","type":"5G","bandwidth_gbps":30}
    ))
    scada.add_component(Component(
        id="paccom_003",
        name="PacCom East Relay",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="East End Rd, Molokai, HI",
        latitude=21.1865,
        longitude=-156.8945,
        metadata={"provider":"PacCom","type":"5G","bandwidth_gbps":30}
    ))

    # interconnect PacCom nodes
    scada.add_connection(Connection(source_id="paccom_001",target_id="paccom_002",connection_type=ConnectionType.COMMUNICATION,flow_direction="bidirectional",metadata={"link":"fiber_trunk"}))
    scada.add_connection(Connection(source_id="paccom_001",target_id="paccom_003",connection_type=ConnectionType.COMMUNICATION,flow_direction="bidirectional",metadata={"link":"fiber_trunk"}))

    # connect SCADA server to central and RTUs to regional nodes
    scada.add_connection(Connection(source_id="scada_srv_001",target_id="paccom_001",connection_type=ConnectionType.COMMUNICATION))
    scada.add_connection(Connection(source_id="rtu_001",target_id="paccom_002",connection_type=ConnectionType.COMMUNICATION))
    scada.add_connection(Connection(source_id="rtu_002",target_id="paccom_003",connection_type=ConnectionType.COMMUNICATION))
    scada.add_component(Component(
        id="rtu_001",
        name="RTU - Kaunakakai Substation",
        component_type=ComponentType.RTU,
        location="Kaunakakai Substation",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2017-01-15"
    ))
    scada.add_component(Component(
        id="rtu_002",
        name="RTU - East Substation",
        component_type=ComponentType.RTU,
        location="East End Substation",
        latitude=21.1865,
        longitude=-156.8945,
        installed_date="2017-01-15"
    ))
    # control connections
    scada.add_connection(Connection(source_id="scada_srv_001",target_id="rtu_001",connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="scada_srv_001",target_id="rtu_002",connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="rtu_001",target_id="br_001",connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="rtu_002",target_id="br_002",connection_type=ConnectionType.CONTROL))
    # monitoring
    scada.add_connection(Connection(source_id="vs_001",target_id="rtu_001",connection_type=ConnectionType.MONITORING,flow_direction="unidirectional"))
    scada.add_connection(Connection(source_id="cs_001",target_id="rtu_002",connection_type=ConnectionType.MONITORING,flow_direction="unidirectional"))
    scada.add_connection(Connection(source_id="ts_001",target_id="rtu_002",connection_type=ConnectionType.MONITORING,flow_direction="unidirectional"))
    # electrical flow
    scada.add_connection(Connection(source_id="sub_001",target_id="fd_001",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=2500,voltage_kv=12,length_km=5))
    scada.add_connection(Connection(source_id="sub_001",target_id="fd_002",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=2000,voltage_kv=12,length_km=3))
    scada.add_connection(Connection(source_id="sub_002",target_id="fd_003",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=1500,voltage_kv=12,length_km=4))
    scada.add_connection(Connection(source_id="fd_001",target_id="tr_001",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=1000))
    scada.add_connection(Connection(source_id="fd_003",target_id="tr_002",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=800))
    scada.add_connection(Connection(source_id="fd_001",target_id="mt_001",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=500))
    scada.add_connection(Connection(source_id="fd_002",target_id="mt_002",connection_type=ConnectionType.ELECTRICAL,flow_direction="bidirectional",capacity=400))
    return scada


if __name__ == "__main__":
    scada=create_pacific_electric_scada()
    print("Pacific Electric SCADA System - Graph Database")
    print("="*60)
    stats=scada.get_graph_statistics()
    print(f"Total Components: {stats['total_components']}")
    print(f"Total Connections: {stats['total_connections']}")
    print("\nComponent Distribution:")
    for t,c in stats['component_types'].items():
        print(f"  {t}: {c}")
    print("\nConnection Distribution:")
    for t,c in stats['connection_types'].items():
        print(f"  {t}: {c}")
    with open("pacific_electric_scada_data.json","w") as f:
        f.write(scada.to_json())
    print("\n✓ Graph data exported to: pacific_electric_scada_data.json")
    with open("pacific_electric_scada_neo4j.cypher","w") as f:
        f.write(scada.export_to_neo4j_cypher())
    print("✓ Neo4j Cypher commands exported to: pacific_electric_scada_neo4j.cypher")
    try:
        scada.visualize("pacific_electric_scada_visualization.png")
        print("✓ Graph visualization saved to: pacific_electric_scada_visualization.png")
    except ImportError:
        print("⚠ Visualization skipped (requires matplotlib)")
    # csv exports
    import csv
    comp_fields=['id','name','component_type','location','latitude','longitude','capacity','unit','operational_status','installed_date']
    with open('pacific_electric_components.csv','w',newline='') as cf:
        w=csv.DictWriter(cf,fieldnames=comp_fields)
        w.writeheader()
        for comp in scada.components.values():
            r=comp.to_dict()
            w.writerow({k:r.get(k) for k in comp_fields})
    conn_fields=['source_id','target_id','connection_type','flow_direction','capacity','length_km','voltage_kv']
    with open('pacific_electric_connections.csv','w',newline='') as cf2:
        w2=csv.DictWriter(cf2,fieldnames=conn_fields)
        w2.writeheader()
        for conn in scada.connections:
            r=conn.to_dict()
            w2.writerow({k:r.get(k) for k in conn_fields})
    print("\n✓ CSV exports: pacific_electric_components.csv, pacific_electric_connections.csv")