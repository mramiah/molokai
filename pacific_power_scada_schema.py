"""
SCADA Graph Database Schema for Pacific Power Generation Network
Supporting Pacific Electric distribution on Molokai, HI

Note: controllers and servers communicate over PacCom's backbone
"""

import networkx as nx
import json
from typing import Dict, List
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime


class ComponentType(Enum):
    """Types of components in the power generation SCADA system"""
    POWER_PLANT = "power_plant"
    WIND_FARM = "wind_farm"
    WIND_TURBINE = "wind_turbine"
    SOLAR_ARRAY = "solar_array"
    HYDRO_PLANT = "hydro_plant"
    OCEAN_PLANT = "ocean_plant"
    SUBSTATION = "substation"
    TRANSMISSION_LINE = "transmission_line"
    SCADA_SERVER = "scada_server"
    RTU = "rtu"
    POWER_SENSOR = "power_sensor"
    TEMPERATURE_SENSOR = "temperature_sensor"
    COMMUNICATION_NODE = "communication_node"


class ConnectionType(Enum):
    """Types of connections between components"""
    ELECTRICAL = "electrical"
    CONTROL = "control"
    MONITORING = "monitoring"
    COMMUNICATION = "communication"


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
                'system':'Pacific Power SCADA',
                'service':'Electric Generation',
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
            "// Pacific Power SCADA Database",
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
                'power_plant':'#FF6B6B','wind_farm':'#4ECDC4','solar_array':'#FFEAA7',
                'hydro_plant':'#45B7D1','ocean_plant':'#96CEB4','substation':'#A29BFE'
            }
            colors=[color_map.get(self.graph.nodes[n].get('component_type'),'#95E1D3') for n in self.graph.nodes()]
            nx.draw_networkx_nodes(self.graph,pos,node_color=colors,node_size=800,alpha=0.9)
            nx.draw_networkx_edges(self.graph,pos,edge_color='gray',arrows=True,arrowsize=20,alpha=0.6)
            nx.draw_networkx_labels(self.graph,pos,font_size=8)
            plt.title("Pacific Power Generation SCADA Network",fontsize=16,fontweight='bold')
            plt.axis('off')
            if output_file:
                plt.savefig(output_file,dpi=300,bbox_inches='tight')
                print(f"Graph saved to {output_file}")
            else:
                plt.show()
        except ImportError:
            print("Visualization requires matplotlib. Install with: pip install matplotlib")


def create_pacific_power_scada() -> SCADAGraphDatabase:
    scada=SCADAGraphDatabase()
    # generation plants
    scada.add_component(Component(
        id="pp_001",
        name="Kaunakakai Wind Farm",
        component_type=ComponentType.WIND_FARM,
        location="West Molokai ridge",
        latitude=21.2050,
        longitude=-157.0700,
        capacity=2000,
        unit="kW",
        installed_date="2015-06-01",
        metadata={"turbines":20}
    ))
    scada.add_component(Component(
        id="pp_002",
        name="Maunaloa Solar Array",
        component_type=ComponentType.SOLAR_ARRAY,
        location="Maunaloa plains",
        latitude=21.2156,
        longitude=-157.1298,
        capacity=1500,
        unit="kW",
        installed_date="2016-09-15",
        metadata={"panels":5000}
    ))
    scada.add_component(Component(
        id="pp_003",
        name="East End Hydro Plant",
        component_type=ComponentType.HYDRO_PLANT,
        location="East Molokai stream",
        latitude=21.1820,
        longitude=-156.8800,
        capacity=800,
        unit="kW",
        installed_date="2014-11-20"
    ))
    scada.add_component(Component(
        id="pp_004",
        name="Ocean Current Generator",
        component_type=ComponentType.OCEAN_PLANT,
        location="Kaunakakai bay",
        latitude=21.1950,
        longitude=-157.0550,
        capacity=500,
        unit="kW",
        installed_date="2018-03-05"
    ))
    # sensors
    scada.add_component(Component(
        id="ps_001",
        name="Power Sensor - Wind Farm",
        component_type=ComponentType.POWER_SENSOR,
        location="West Molokai ridge",
        latitude=21.2050,
        longitude=-157.0700
    ))
    scada.add_component(Component(
        id="ps_002",
        name="Power Sensor - Solar Array",
        component_type=ComponentType.POWER_SENSOR,
        location="Maunaloa plains",
        latitude=21.2156,
        longitude=-157.1298
    ))
    # substations / transmission
    scada.add_component(Component(
        id="sub_001",
        name="Generation Substation",
        component_type=ComponentType.SUBSTATION,
        location="100 Power Rd, Kaunakakai",
        latitude=21.1952,
        longitude=-157.0547,
        capacity=5000,
        unit="kW"
    ))
    scada.add_component(Component(
        id="line_001",
        name="Transmission Line - West Corridor",
        component_type=ComponentType.TRANSMISSION_LINE,
        location="West route",
        latitude=21.2050,
        longitude=-157.0700,
        metadata={"length_km":7, "voltage_kv":69}
    ))
    # SCADA devices
    scada.add_component(Component(
        id="scada_srv_001",
        name="Power SCADA Server",
        component_type=ComponentType.SCADA_SERVER,
        location="100 Power Rd, Kaunakakai",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2015-01-10"
    ))

    # PacCom backbone with central and auxiliary nodes
    scada.add_component(Component(
        id="paccom_001",
        name="PacCom Central Gateway",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="100 Power Rd, Kaunakakai",
        latitude=21.1952,
        longitude=-157.0547,
        metadata={"provider":"PacCom","type":"fiber/5G","bandwidth_gbps":100}
    ))
    scada.add_component(Component(
        id="paccom_002",
        name="PacCom West Relay",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="Maunaloa Ridge",
        latitude=21.2156,
        longitude=-157.1298,
        metadata={"provider":"PacCom","type":"5G","bandwidth_gbps":25}
    ))
    scada.add_component(Component(
        id="paccom_003",
        name="PacCom East Relay",
        component_type=ComponentType.COMMUNICATION_NODE,
        location="East End Rd",
        latitude=21.1865,
        longitude=-156.8945,
        metadata={"provider":"PacCom","type":"5G","bandwidth_gbps":25}
    ))
    scada.add_connection(Connection(source_id="paccom_001",target_id="paccom_002",connection_type=ConnectionType.COMMUNICATION,flow_direction="bidirectional",metadata={"link":"fiber_trunk"}))
    scada.add_connection(Connection(source_id="paccom_001",target_id="paccom_003",connection_type=ConnectionType.COMMUNICATION,flow_direction="bidirectional",metadata={"link":"fiber_trunk"}))
    scada.add_connection(Connection(source_id="scada_srv_001",target_id="paccom_001",connection_type=ConnectionType.COMMUNICATION))
    scada.add_connection(Connection(source_id="rtu_001",target_id="paccom_002",connection_type=ConnectionType.COMMUNICATION))
    scada.add_component(Component(
        id="rtu_001",
        name="RTU - Generation Substation",
        component_type=ComponentType.RTU,
        location="Generation Substation",
        latitude=21.1952,
        longitude=-157.0547,
        installed_date="2015-01-10"
    ))
    # control & monitoring connections
    scada.add_connection(Connection(source_id="scada_srv_001",target_id="rtu_001",connection_type=ConnectionType.CONTROL))
    scada.add_connection(Connection(source_id="rtu_001",target_id="ps_001",connection_type=ConnectionType.MONITORING,flow_direction="unidirectional"))
    scada.add_connection(Connection(source_id="rtu_001",target_id="ps_002",connection_type=ConnectionType.MONITORING,flow_direction="unidirectional"))
    # electrical flow from plants to substation
    scada.add_connection(Connection(source_id="pp_001",target_id="line_001",connection_type=ConnectionType.ELECTRICAL,capacity=2000,voltage_kv=69))
    scada.add_connection(Connection(source_id="pp_002",target_id="line_001",connection_type=ConnectionType.ELECTRICAL,capacity=1500,voltage_kv=69))
    scada.add_connection(Connection(source_id="pp_003",target_id="sub_001",connection_type=ConnectionType.ELECTRICAL,capacity=800,voltage_kv=12))
    scada.add_connection(Connection(source_id="pp_004",target_id="sub_001",connection_type=ConnectionType.ELECTRICAL,capacity=500,voltage_kv=12))
    scada.add_connection(Connection(source_id="line_001",target_id="sub_001",connection_type=ConnectionType.ELECTRICAL,capacity=3500,voltage_kv=69))
    return scada


if __name__ == "__main__":
    scada=create_pacific_power_scada()
    print("Pacific Power SCADA System - Graph Database")
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
    with open("pacific_power_scada_data.json","w") as f:
        f.write(scada.to_json())
    print("\n✓ Graph data exported to: pacific_power_scada_data.json")
    with open("pacific_power_scada_neo4j.cypher","w") as f:
        f.write(scada.export_to_neo4j_cypher())
    print("✓ Neo4j Cypher commands exported to: pacific_power_scada_neo4j.cypher")
    try:
        scada.visualize("pacific_power_scada_visualization.png")
        print("✓ Graph visualization saved to: pacific_power_scada_visualization.png")
    except ImportError:
        print("⚠ Visualization skipped (requires matplotlib)")
    import csv
    comp_fields=['id','name','component_type','location','latitude','longitude','capacity','unit','operational_status','installed_date']
    with open('pacific_power_components.csv','w',newline='') as cf:
        w=csv.DictWriter(cf,fieldnames=comp_fields)
        w.writeheader()
        for comp in scada.components.values():
            r=comp.to_dict()
            w.writerow({k:r.get(k) for k in comp_fields})
    conn_fields=['source_id','target_id','connection_type','flow_direction','capacity','length_km','voltage_kv']
    with open('pacific_power_connections.csv','w',newline='') as cf2:
        w2=csv.DictWriter(cf2,fieldnames=conn_fields)
        w2.writeheader()
        for conn in scada.connections:
            r=conn.to_dict()
            w2.writerow({k:r.get(k) for k in conn_fields})
    print("\n✓ CSV exports: pacific_power_components.csv, pacific_power_connections.csv")