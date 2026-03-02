# Pacific Fuel Dependency Graph

This dataset models the relationships between fuel storage locations and
critical facilities that depend on standby diesel generators for backup
power in Pacific Electric, Pacific Water, and Pacific Treatment systems on
Molokai, HI.

## Components
- **Plants/Substations**: water treatment plant, wastewater treatment plant,
  electric substations.
- **Fuel Storage Sites**: three depots located around Molokai (Kaunakakai,
  East End, North Shore).

## Dependencies
- Storage sites supply fuel to one or more plants/substations.
- Reverse `depends_on` edges indicate which plants rely on which storage.

## Files
- `pacific_fuel_storage_schema.py` - Python graph generation code
- `pacific_fuel_export.py` - Helper for generating JSON/CSV/PNG exports
- `fuel_dependency_data.json` - Exported graph structure
- `fuel_nodes.csv`, `fuel_edges.csv` - Tabular exports
- `fuel_dependency_visualization.png` - Graph visualization

## Usage
```bash
python3 pacific_fuel_storage_schema.py
# or use helper
python3 pacific_fuel_export.py
```

Visualization requires `matplotlib`.

## Notes
This graph helps illustrate how multiple utility systems share common fuel
resources, highlighting potential single points of failure at storage sites.