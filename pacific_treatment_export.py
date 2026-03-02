#!/usr/bin/env python3
"""
Helper script to export Pacific Treatment SCADA graph and CSVs
"""

import sys
sys.path.insert(0, "/Users/mahe3998/Library/CloudStorage/OneDrive-Esri/1\ HI\ OHS/Workshop/2026/scada")

from pacific_treatment_scada_schema import create_pacific_treatment_scada

# build graph
scada = create_pacific_treatment_scada()

# stats
print("Pacific Treatment SCADA System - Graph Database (Molokai, HI)")
print("="*60)
stats = scada.get_graph_statistics()
print(f"Total Components: {stats['total_components']}")
print(f"Total Connections: {stats['total_connections']}")

# export JSON
with open("pacific_treatment_scada_data.json","w") as f:
    f.write(scada.to_json())
print("\n✓ Graph data exported to: pacific_treatment_scada_data.json")

# export CSVs
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
