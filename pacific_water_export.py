#!/usr/bin/env python3
"""
Simplified SCADA graph database exporter - generates data without matplotlib dependency
"""

import sys
sys.path.insert(0, "/Users/mahe3998/Library/CloudStorage/OneDrive-Esri/1\ HI\ OHS/Workshop/2026/scada")

from pacific_water_scada_schema import create_pacific_water_scada

# Create the SCADA system
scada = create_pacific_water_scada()

# Print statistics
print("Pacific Water SCADA System - Graph Database (Molokai, HI)")
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

# Export to CSV for components and connections
import csv

comp_fields = [
    'id','name','component_type','location','latitude','longitude',
    'capacity','unit','operational_status','installed_date'
]
with open('pacific_water_components.csv', 'w', newline='') as cf:
    writer = csv.DictWriter(cf, fieldnames=comp_fields)
    writer.writeheader()
    for comp in scada.components.values():
        row = comp.to_dict()
        # flatten metadata if needed
        writer.writerow({k: row.get(k) for k in comp_fields})

conn_fields = [
    'source_id','target_id','connection_type','flow_direction',
    'capacity','length_km','diameter_inches','material'
]
with open('pacific_water_connections.csv', 'w', newline='') as cf2:
    writer = csv.DictWriter(cf2, fieldnames=conn_fields)
    writer.writeheader()
    for conn in scada.connections:
        row = conn.to_dict()
        writer.writerow({k: row.get(k) for k in conn_fields})

print("\n✓ CSV exports: pacific_water_components.csv, pacific_water_connections.csv")

# Check sample components with Molokai coordinates
print("\n" + "=" * 60)
print("Sample Components with Molokai Coordinates:")
print("=" * 60)
for comp_id in ["tp_001", "ps_001", "res_001", "cz_001", "cz_002"]:
    comp = scada.get_component(comp_id)
    if comp:
        print(f"\n{comp.name}")
        print(f"  Location: {comp.location}")
        print(f"  Lat/Long: {comp.latitude}, {comp.longitude}")

print("\n✓ All locations updated to Molokai, HI")
