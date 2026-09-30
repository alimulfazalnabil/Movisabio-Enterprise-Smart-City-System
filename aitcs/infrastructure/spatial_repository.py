"""In-memory stand-in for intersection coordinates and geofence queries."""

from typing import Dict, List, Tuple

class PostGISSpatialRepository:
    """Expose the future PostGIS contract using built-in demonstration data.

    Despite its name, this class does not open a database connection.
    """

    def __init__(self):
        """Load the demonstration intersections and polygon registry."""

        # Simulated spatial database store for intersections and geofences
        self.intersection_coordinates: Dict[str, Tuple[float, float]] = {
            "INT-001": (23.8103, 90.4125),
            "INT-002": (23.8150, 90.4200),
            "INT-003": (23.8050, 90.4050)
        }
        self.geofences: Dict[str, List[Tuple[float, float]]] = {
            "downtown_zone": [(23.8000, 90.4000), (23.8200, 90.4000), (23.8200, 90.4300), (23.8000, 90.4300)]
        }

    def get_intersection_location(self, intersection_id: str) -> Tuple[float, float]:
        """Return stored coordinates or ``(0.0, 0.0)`` for an unknown ID."""
        return self.intersection_coordinates.get(intersection_id, (0.0, 0.0))

    def check_geofence(self, lat: float, lon: float, zone_name: str) -> bool:
        """Check a point against a named polygon with a ray-casting algorithm.

        Returns ``False`` when the geofence does not exist. Coordinate ordering
        follows the built-in dataset and should be reviewed before replacing it
        with PostGIS geometry types.
        """
        polygon = self.geofences.get(zone_name, [])
        if not polygon:
            return False
        # Ray-casting algorithm for spatial point-in-polygon containment
        inside = False
        n = len(polygon)
        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if lat > min(p1y, p2y):
                if lat <= max(p1y, p2y):
                    if lon <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (lat - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or lon <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
