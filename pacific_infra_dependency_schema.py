"""
Graph showing interdependencies among Pacific Electric, Pacific Water,
Pacific Treatment, PacCom, and key transportation facilities on Molokai.
"""

import networkx as nx
import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List
from datetime import datetime


class InfraNodeType(Enum):
    UTILITY = "utility"
    COMMUNICATION = "communication"
    TRANSPORT = "transport"
    OTHER = "other"


class InfraEdgeType(Enum):
    DEPENDS_ON = "depends_on"
    CONNECTED_VIA = "connected_via"
    SERVICES = "services"


@dataclass
class InfraNode:
    id: str
    name: str
    node_type: InfraNodeType
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
class InfraEdge:
    source: str
    target: str
    edge_type: InfraEdgeType
    metadata: Dict = None

    def to_dict(self):
        d = asdict(self)
        d['edge_type'] = self.edge_type.value
        if self.metadata is None:
            d['metadata'] = {}
        return d


class InfraDependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, InfraNode] = {}
        self.edges: List[InfraEdge] = []

    def add_node(self,node:InfraNode):
        self.nodes[node.id] = node
        self.graph.add_node(node.id,**node.to_dict())

    def add_edge(self,edge:InfraEdge):
        self.edges.append(edge)
        self.graph.add_edge(edge.source,edge.target,**edge.to_dict())

    def to_json(self):
        data={'metadata':{
                'created':datetime.now().isoformat(),
                'description':'Infrastructure dependency graph'
            },
            'nodes':[n.to_dict() for n in self.nodes.values()],
            'edges':[e.to_dict() for e in self.edges]
        }
        return json.dumps(data,indent=2,default=str)

    def export_csv(self,node_file='infra_nodes.csv',edge_file='infra_edges.csv'):
        import csv
        with open(node_file,'w',newline='') as nf:
            writer=csv.DictWriter(nf,fieldnames=['id','name','node_type','latitude','longitude'])
            writer.writeheader()
            for n in self.nodes.values():
                r=n.to_dict()
                writer.writerow({k:r.get(k) for k in ['id','name','node_type','latitude','longitude']})
        with open(edge_file,'w',newline='') as ef:
            writer=csv.DictWriter(ef,fieldnames=['source','target','edge_type'])
            writer.writeheader()
            for e in self.edges:
                r=e.to_dict()
                writer.writerow({k:r.get(k) for k in ['source','target','edge_type']})

    def visualize(self,output_file=None):
        try:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(12,10))
            pos=nx.spring_layout(self.graph,k=2,iterations=50)
            cmap={'utility':'#FF6B6B','communication':'#4ECDC4','transport':'#FFEAA7','other':'#A29BFE'}
            colors=[cmap.get(self.graph.nodes[n].get('node_type'),'#95E1D3') for n in self.graph.nodes()]
            nx.draw(self.graph,pos,node_color=colors,with_labels=True,node_size=800)
            nx.draw_networkx_edge_labels(self.graph,pos,edge_labels={(u,v):d['edge_type'] for u,v,d in self.graph.edges(data=True)},font_color='gray')
            plt.axis('off')
            if output_file:
                plt.savefig(output_file,dpi=300,bbox_inches='tight')
                print(f"Saved visualization to {output_file}")
            else:
                plt.show()
        except ImportError:
            print("Install matplotlib to visualize")


def build_infra_graph():
    g=InfraDependencyGraph()
    # utilities
    g.add_node(InfraNode(id='water',name='Pacific Water System',node_type=InfraNodeType.UTILITY))
    g.add_node(InfraNode(id='electric',name='Pacific Electric System',node_type=InfraNodeType.UTILITY))
    g.add_node(InfraNode(id='treatment',name='Pacific Treatment System',node_type=InfraNodeType.UTILITY))
    # communications
    g.add_node(InfraNode(id='paccom',name='PacCom Network',node_type=InfraNodeType.COMMUNICATION))
    # transport links
    g.add_node(InfraNode(id='road',name='Road Network',node_type=InfraNodeType.TRANSPORT))
    g.add_node(InfraNode(id='port',name='Molokai Port',node_type=InfraNodeType.TRANSPORT))
    g.add_node(InfraNode(id='airport',name='Molokai Airport',node_type=InfraNodeType.TRANSPORT))

    # dependencies edges
    for util in ['water','electric','treatment']:
        g.add_edge(InfraEdge(source=util,target='paccom',edge_type=InfraEdgeType.DEPENDS_ON))
        g.add_edge(InfraEdge(source=util,target='road',edge_type=InfraEdgeType.DEPENDS_ON))
    # transport serves utilities
    for util in ['water','electric','treatment']:
        g.add_edge(InfraEdge(source='port',target=util,edge_type=InfraEdgeType.SERVICES))
        g.add_edge(InfraEdge(source='airport',target=util,edge_type=InfraEdgeType.SERVICES))
    # paccom connects via road and port
    g.add_edge(InfraEdge(source='paccom',target='road',edge_type=InfraEdgeType.CONNECTED_VIA))
    g.add_edge(InfraEdge(source='paccom',target='port',edge_type=InfraEdgeType.CONNECTED_VIA))
    return g

if __name__=='__main__':
    graph=build_infra_graph()
    print(graph.to_json())
    with open('infra_dependency_data.json','w') as f:
        f.write(graph.to_json())
    graph.export_csv()
    graph.visualize('infra_dependency_visualization.png')
    print("Generated infra dependency data and visualization")
