"""
Helper script for exporting the fuel dependency graph
"""
from pacific_fuel_storage_schema import build_fuel_dependency_graph


def main():
    g = build_fuel_dependency_graph()
    with open('fuel_dependency_data.json','w') as f:
        f.write(g.to_json())
    print('JSON export written: fuel_dependency_data.json')
    g.export_csv('fuel_nodes.csv','fuel_edges.csv')
    print('CSV exports written: fuel_nodes.csv, fuel_edges.csv')
    try:
        g.visualize('fuel_dependency_visualization.png')
        print('Visualization saved: fuel_dependency_visualization.png')
    except Exception:
        pass

if __name__=='__main__':
    main()
