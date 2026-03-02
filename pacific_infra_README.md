# Infrastructure Dependency Graph

This dataset highlights how key utility systems on Molokai (Pacific Electric,
Pacific Water, Pacific Treatment) rely on communication and transportation
infrastructure provided by PacCom, the road network, the island port, and the
airport.

## Node Types
- **Utility**: overall system nodes representing each service provider
- **Communication**: PacCom network backbone
- **Transport**: Road network, Molokai Port, Molokai Airport

## Edge Types
- `depends_on`: indicates a system requires another infrastructure to operate
- `services`: transport facilities servicing utilities (e.g., port supplies
  equipment)
- `connected_via`: connectivity relationships (PacCom uses road and port routes)

## Files
- `pacific_infra_dependency_schema.py` – Python code for graph construction
- `pacific_infra_export.py` – helper for JSON/CSV/PNG exports
- `infra_dependency_data.json` – exported graph data
- `infra_nodes.csv`, `infra_edges.csv` – tabular exports
- `infra_dependency_visualization.png` – network diagram

## Generate Data
```bash
python3 pacific_infra_dependency_schema.py
# or
python3 pacific_infra_export.py
```

Visualization requires `matplotlib`.

## Purpose
Provides a high‑level view of cross‑sector dependencies, useful for
coordination, risk assessment, and planning. For instance, the graph shows
that all three utility systems depend on both the PacCom network and the road
system, and that PacCom itself is connected via road and port infrastructure.