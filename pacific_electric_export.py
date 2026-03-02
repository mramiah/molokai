"""
Utility to export Pacific Electric SCADA graph to JSON and CSV.
"""
import json
import csv
from pacific_electric_scada_schema import create_pacific_electric_scada


def main():
    scada = create_pacific_electric_scada()

    # JSON output
    with open('pacific_electric_scada_data.json', 'w') as f:
        f.write(scada.to_json())
    print('JSON export complete: pacific_electric_scada_data.json')

    # CSV output
    comp_fields = ['id', 'name', 'component_type', 'location', 'latitude', 'longitude',
                   'capacity', 'unit', 'operational_status', 'installed_date']
    with open('pacific_electric_components.csv', 'w', newline='') as cf:
        writer = csv.DictWriter(cf, fieldnames=comp_fields)
        writer.writeheader()
        for comp in scada.components.values():
            row = comp.to_dict()
            writer.writerow({k: row.get(k) for k in comp_fields})
    print('CSV export complete: pacific_electric_components.csv')

    conn_fields = ['source_id', 'target_id', 'connection_type', 'flow_direction',
                   'capacity', 'length_km', 'voltage_kv']
    with open('pacific_electric_connections.csv', 'w', newline='') as cf2:
        writer = csv.DictWriter(cf2, fieldnames=conn_fields)
        writer.writeheader()
        for conn in scada.connections:
            row = conn.to_dict()
            writer.writerow({k: row.get(k) for k in conn_fields})
    print('CSV export complete: pacific_electric_connections.csv')


if __name__ == '__main__':
    main()
