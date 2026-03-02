# Pacific Water SCADA System - Molokai, HI Coordinates

## System Overview
All components of the Pacific Water SCADA system are now located on the island of Molokai, Hawaii. The system serves the city of West Pacific with a population of 10,000.

## Geographic Coordinates Reference

### Primary Infrastructure

| Component | Type | Latitude | Longitude | Location | Notes |
|-----------|------|----------|-----------|----------|-------|
| West Pacific Water Treatment Plant | Treatment Plant | 21.1952 | -157.0547 | Kaunakakai | Central treatment facility |
| Primary Pumping Station - North | Pumping Station | 21.2482 | -157.0623 | North Shore Road | 3,000 gpm capacity |
| Secondary Pumping Station - East | Pumping Station | 21.1865 | -156.8945 | East End Road | 2,000 gpm capacity |
| North Storage Reservoir | Reservoir | 21.2561 | -157.0854 | North Shore | 1,000,000 gallons capacity |
| East Storage Reservoir | Reservoir | 21.1802 | -156.8567 | East End | 500,000 gallons capacity |

### Distribution Network

| Component | Type | Latitude | Longitude | Location | Diameter | Length |
|-----------|------|----------|-----------|----------|----------|--------|
| Main Distribution Line - North | Distribution Main | 21.2312 | -157.0736 | North Shore zone | 12" | 4.5 km |
| Main Distribution Line - Central | Distribution Main | 21.1923 | -157.0621 | Kaunakakai | 14" | 2.8 km |
| Main Distribution Line - East | Distribution Main | 21.1834 | -156.8756 | East End zone | 10" | 3.2 km |

### Control & Monitoring Centers

| Component | Type | Latitude | Longitude | Location |
|-----------|------|----------|-----------|----------|
| Central SCADA Server | SCADA Server | 21.1952 | -157.0547 | Kaunakakai |
| RTU - North Station | Remote Terminal Unit | 21.2482 | -157.0623 | North Shore |
| RTU - East Station | Remote Terminal Unit | 21.1865 | -156.8945 | East End |
| RTU - North Reservoir | Remote Terminal Unit | 21.2561 | -157.0854 | North Shore |

### Customer Service Zones

| Component | Type | Latitude | Longitude | Location | Customers | Avg Demand |
|-----------|------|----------|-----------|----------|-----------|-----------|
| Residential Zone - North | Customer Zone | 21.2156 | -157.1298 | Maunaloa | 2,500 | 800 gpm |
| Commercial Zone - Central | Customer Zone | 21.1943 | -157.0519 | Kaunakakai Downtown | 1,500 | 600 gpm |
| Industrial Zone - East | Customer Zone | 21.1745 | -156.8234 | Pukoo | 800 | 500 gpm |
| Residential Zone - South | Customer Zone | 21.1621 | -157.0345 | Mapulehu | 2,200 | 700 gpm |

### Monitoring Sensors

| Component | Type | Latitude | Longitude | Location |
|-----------|------|----------|-----------|----------|
| Flow Meter - Treatment Plant Exit | Flow Meter | 21.1952 | -157.0547 | Kaunakakai |
| Level Sensor - North Reservoir | Level Sensor | 21.2561 | -157.0854 | North Shore |
| Level Sensor - East Reservoir | Level Sensor | 21.1802 | -156.8567 | East End |
| Pressure Gauge - North Line | Pressure Gauge | 21.2312 | -157.0736 | North Shore |
| Pressure Gauge - East Line | Pressure Gauge | 21.1834 | -156.8756 | East End |

### Control Valves

| Component | Type | Latitude | Longitude | Location |
|-----------|------|----------|-----------|----------|
| Pressure Reducing Valve - North | PRV | 21.2234 | -157.0892 | North Shore |
| Check Valve - Pump Station North | Check Valve | 21.2482 | -157.0623 | North Pumping Station |
| Isolation Valve - North Main | Isolation Valve | 21.2401 | -157.0679 | North Shore |

## Molokai Island Geography

### Geographic Bounds
- **North Latitude**: 21.2561° (North Shore Reservoir)
- **South Latitude**: 21.1621° (Mapulehu - South Residential)
- **West Longitude**: -157.1298° (Maunaloa - North Residential)
- **East Longitude**: -156.8234° (Pukoo - Industrial Zone)

### Distance Estimates
- **North-South Span**: ~10 km
- **East-West Span**: ~32 km
- **Total Area**: ~320 km²

### Key Towns & Landmarks on Molokai
- **Kaunakakai** (21.1943°, -157.0519°) - Central business district, treatment plant location
- **Maunaloa** (21.2156°, -157.1298°) - West end, northern residential area
- **Pukoo** (21.1745°, -156.8234°) - East end, industrial zone
- **Mapulehu** (21.1621°, -157.0345°) - South shore, southern residential area

## System Distribution Pattern

The Pacific Water SCADA system is distributed as follows:

```
                    North Shore
                    ┌─────────────────────────┐
                    │     North Residential   │
                    │    (Maunaloa Area)      │
    Lat: 21.2156°   │   2,500 customers       │
    Long: -157.1298 │   800 gpm demand        │
                    └─────────────────────────┘
                              ▲
                              │
                         DM-001 (North)
                         12" diameter
                         4.5 km length
                              │
                              ▼
        ┌─────────────────────────────────┐
        │   North Shore Reservoir         │
        │   1,000,000 gallons             │
        │   Lat: 21.2561°                 │
        │   Long: -157.0854°              │
        └─────────────────────────────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ PS North         │
        │ 3,000 gpm        │
        │ (21.2482, -157.062) │
        └──────────────────┘
                 │
                 ▼
        ┌──────────────────────────────────┐
        │ Treatment Plant (Kaunakakai)     │
        │ 5,000 gpm capacity               │
        │ Lat: 21.1952°, Long: -157.0547°  │
        └──────────────────────────────────┘
                 │
        ┌────────┼────────┐
        ▼        ▼        ▼
    DM-001   DM-003   DM-002
    (North)  (Central) (East)
        │        │        │
    ┌───▼───┐ ┌──▼──┐ ┌───▼────┐
    │North  │ │Comm │ │East    │
    │Res    │ │Zone │ │Ind     │
    │Zone   │ │     │ │Zone    │
    │2500c  │ │1500c│ │800c    │
    │800gpm │ │600gp│ │500gpm  │
    └───────┘ └─────┘ └────────┘
```

## Water Flow Characteristics

### Peak System Demand
- **Total Treatment Capacity**: 5,000 gpm
- **Peak Customer Demand**: 2,600 gpm (52% of capacity)
- **System Reserve**: 2,400 gpm (48% safety margin)

### Flow Distribution
```
Treatment Plant (5000 gpm)
├─ North Pump: 3000 gpm → North Zone (800) + South Zone (700) + Reserve (1500)
├─ East Pump: 2000 gpm → Central Zone (600) + Industrial Zone (500) + Reserve (900)
└─ Storage in Reservoirs for demand balancing
```

## GIS Integration Reference

All components are geo-referenced with latitude/longitude coordinates compatible with:
- **EPSG:4326** (WGS 84 - World Geodetic System)
- Google Maps, OpenStreetMap, ArcGIS
- Standard GPS receivers
- Most GIS software packages

## Files with Coordinate Data

1. **scada_graph_data.json** - Complete system data with lat/long for all components
2. **scada_graph_neo4j.cypher** - Neo4j database with spatial indexing ready
3. **pacific_water_scada_visualization.png** - Network topology diagram
4. **scada_graph_schema.py** - Python implementation with coordinate references

## Mapping Tools

### Quick Map Preview
To view components on a map, use these coordinates with:
- Google Maps: Enter each lat/long pair in search box
- OpenStreetMap: Visit `https://www.openstreetmap.org/?lat=21.XX&lon=-157.XX`
- ArcGIS: Import JSON file with spatial data

### Converting Coordinates
All coordinates are in **Decimal Degrees** (DD) format:
```
Latitude:  21.1952° N (North)
Longitude: -157.0547° W (West)
```

### Distance Calculations
To calculate distance between two components, use the Haversine formula:
```python
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

# Example: Distance from Treatment Plant to North Reservoir
distance = haversine(-157.0547, 21.1952, -157.0854, 21.2561)
print(f"Distance: {distance:.2f} km")
```

## Next Steps

1. **GIS Analysis** - Import data into ArcGIS for spatial analysis
2. **Route Optimization** - Calculate optimal placement for new infrastructure
3. **Service Area Analysis** - Perform coverage analysis for each zone
4. **Network Resilience** - Analyze geographic redundancy
5. **Emergency Planning** - Use coordinates for incident response routing

---

**Created**: March 1, 2026
**System**: Pacific Water Distribution Network
**Island**: Molokai, Hawaii
**Service Population**: 10,000
