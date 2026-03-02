"""
Helper for exporting infrastructure dependency graph
"""
from pacific_infra_dependency_schema import build_infra_graph


def main():
    g = build_infra_graph()
    with open('infra_dependency_data.json','w') as f:
        f.write(g.to_json())
    print('JSON export written: infra_dependency_data.json')
    g.export_csv()
    print('CSV exports written: infra_nodes.csv, infra_edges.csv')
    try:
        g.visualize('infra_dependency_visualization.png')
        print('Visualization saved: infra_dependency_visualization.png')
    except Exception:
        pass

if __name__=='__main__':
    main()
