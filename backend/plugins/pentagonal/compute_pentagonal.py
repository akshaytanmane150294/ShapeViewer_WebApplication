import math

def compute_surface_area_volume(prism):
    """
    Calculate surface area and volume of a regular pentagonal prism
    given the radius (center to vertex) of the base and prism height.
    
    Parameters:
    r : float : radius of the pentagon (center to vertex)
    h : float : height of the prism
    
    Returns:
    tuple : (surface_area, volume)
    """
    # Calculate side length from radius
    r, h = prism.radius, prism.height
    
    s = 2 * r * math.sin(math.pi / 5)
    
    # Base area
    base_area = (5/4) * s**2 * (1 / math.tan(math.pi / 5))
    
    # Lateral area
    lateral_area = 5 * s * h
    
    # Total surface area
    surface_area = 2 * base_area + lateral_area
    
    # Volume
    volume = base_area * h
    
    return {
        "surface_area": surface_area,
        "volume": volume
    }