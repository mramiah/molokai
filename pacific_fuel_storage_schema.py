"""
Graph dataset capturing fuel storage dependencies for standby generators
across Pacific Electric, Pacific Water, and Pacific Treatment systems on Molokai.
"""

import networkx as nx
import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List
from datetime import datetime


class NodeType(Enum):
    PLANT = "plant"
    SUBSTATION = "substation"
    FUEL_STORAGE = "fuel_storage"
    OTHER = "other"


class EdgeType(Enum):
    SUPPLIES = "supplies"  # fuel supply
    DEPENDS_ON = "depends_on"


@dataclass
class Node:
    id: str
    name: str
    node_type: NodeType
    latitude: float = None
    longitude: float = None
    metadata: Dict = None

    def to_dict(self):
        d = asdict(self)
        d['node_type'] = self.node_type.value
        if self.metadata is None:
            d['metadata'] = {}
        return d


@dataclass
class Edge:
    source_id: str
    target_id: str
    edge_type: EdgeType
    metadata: Dict = None

    def to_dict(self):
        d = asdict(self)
        d['edge_type'] = self.edge_type.value
        if self.metadata is None:
            d['metadata'] = {}
        return d


class FuelDependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        self.graph.add_node(node.id, **node.to_dict())

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        self.graph.add_edge(edge.source_id, edge.target_id, **edge.to_dict())

    def to_json(self):
        data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'description': 'Fuel storage dependency graph',
                'node_count': len(self.nodes),
                'edge_count': len(self.edges)
            },
            'nodes': [n.to_dict() for n in self.nodes.values()],
            'edges': [e.to_dict() for e in self.edges]
        }
        return json.dumps(data, indent=2, default=str)

    def export_csv(self, node_file='fuel_nodes.csv', edge_file='fuel_edges.csv'):
        import csv
        node_fields=['id','name','node_type','latitude','longitude']
        with open(node_file,'w',newline='') as nf:
            w=csv.DictWriter(nf,fieldnames=node_fields)
            w.writeheader()
            for n in self.nodes.values():
                r=n.to_dict()
                w.writerow({k:r.get(k) for k in node_fields})
        edge_fields=['source_id','target_id','edge_type']
        with open(edge_file,'w',newline='') as ef:
            w=csv.DictWriter(ef,fieldnames=edge_fields)
            w.writeheader()
            for e in self.edges:
                r=e.to_dict()
                w.writerow({k:r.get(k) for k in edge_fields})

    def visualize(self,output_file=None):
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10,8))
            pos=nx.spring_layout(self.graph,k=1.5,iterations=50)
            color_map={'plant':'#FF6B6B','substation':'#4ECDC4','fuel_storage':'#FFEAA7','other':'#A29BFE'}
            colors=[color_map.get(self.graph.nodes[n].get('node_type'),'#95E1D3') for n in self.graph.nodes()]
            nx.draw(self.graph,pos,node_color=colors,with_labels=True,node_size=800)
            nx.draw_networkx_edge_labels(self.graph,pos,edge_labels={(u,v):d['edge_type'] for u,v,d in self.graph.edges(data=True)},font_color='gray')
            plt.axis('off')
            if output_file:
                plt.savefig(output_file,dpi=300,bbox_inches='tight')
                print(f"Visualization saved to {output_file}")
            else:
                plt.show()
        except ImportError:
            print("Install matplotlib to visualize")


def build_fuel_dependency_graph():
    g=FuelDependencyGraph()
    # plants and substations
    g.add_node(Node(id='water_tp',name='Water Treatment Plant',node_type=NodeType.PLANT,latitude=21.1952,longitude=-157.0547))
    g.add_node(Node(id='electric_sub1',name='Kaunakakai Substation',node_type=NodeType.SUBSTATION,latitude=21.1952,longitude=-157.0547))
    g.add_node(Node(id='electric_sub2',name='East End Substation',node_type=NodeType.SUBSTATION,latitude=21.1865,longitude=-156.8945))
    g.add_node(Node(id='treatment_tp',name='Wastewater Treatment Plant',node_type=NodeType.PLANT,latitude=21.1952,longitude=-157.0547))
    # fuel storage locations
    g.add_node(Node(id='fs_001',name='Fuel Storage Kaunakakai',node_type=NodeType.FUEL_STORAGE,latitude=21.1940,longitude=-157.0520))
    g.add_node(Node(id='fs_002',name='Fuel Storage East End',node_type=NodeType.FUEL_STORAGE,latitude=21.1860,longitude=-156.8950))
    g.add_node(Node(id='fs_003',name='Fuel Storage North Shore',node_type=NodeType.FUEL_STORAGE,latitude=21.2480,longitude=-157.0620))

    # dependencies
    g.add_edge(Edge(source_id='fs_001',target_id='water_tp',edge_type=EdgeType.SUPPLIES))
    g.add_edge(Edge(source_id='fs_001',target_id='electric_sub1',edge_type=EdgeType.SUPPLIES))
    g.add_edge(Edge(source_id='fs_002',target_id='electric_sub2',edge_type=EdgeType.SUPPLIES))
    g.add_edge(Edge(source_id='fs_002',target_id='treatment_tp',edge_type=EdgeType.SUPPLIES))
    g.add_edge(Edge(source_id='fs_003',target_id='electric_sub1',edge_type=EdgeType.SUPPLIES))

    # optional reverse dependency relationship
    for plant in ['water_tp','electric_sub1','electric_sub2','treatment_tp']:
        g.add_edge(Edge(source_id=plant,target_id='fs_001' if plant in ['water_tp','electric_sub1'] else 'fs_002',edge_type=EdgeType.DEPENDS_ON))
    return g


if __name__=='__main__':
    graph=build_fuel_dependency_graph()
    print("Fuel dependency graph")
    print(graph.to_json())
    with open('fuel_dependency_data.json','w') as f:
        f.write(graph.to_json())
    graph.export_csv('fuel_nodes.csv','fuel_edges.csv')
    graph.visualize('fuel_dependency_visualization.png')
    print("Exports complete: fuel_dependency_data.json, fuel_nodes.csv, fuel_edges.csv, fuel_dependency_visualization.png")
