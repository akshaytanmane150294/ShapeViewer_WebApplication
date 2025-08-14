import math

def compute_surface_area_volume(prism):
    if prism.prism_name == "rectangular":
        l, w, h = prism.length, prism.width, prism.height
        surface_area = 2 * (l*w + w*h + h*l)
        volume = l * w * h

    elif prism.prism_name == "cylinder":
        r, h = prism.radius, prism.height
        surface_area = 2 * 3.14 * r * (r + h)
        volume = 3.14 * r**2 * h
        
    elif prism.prism_name == "cone":
        r, h = prism.radius, prism.height
        l = math.sqrt(r**2 + h**2)
        surface_area = math.pi * r * (r + l)
        volume = (1/3) * math.pi * r**2 * h

    else:
        surface_area = volume = 0

    return {
        "surface_area": surface_area,
        "volume": volume
    }


import sys
sys.path.append('/usr/lib/freecad/lib')
sys.path.append('/usr/lib/freecad/')

import FreeCAD
import Part

def get_cad_model_data(prism):
    prism_type = prism.prism_name.lower()
    
    if prism_type == 'rectangular':
        l, w, h = prism.length, prism.width, prism.height
        shape = Part.makeBox(l, w, h)
    
    elif prism_type == 'cylinder':
        r, h = prism.radius, prism.height
        shape = Part.makeCylinder(r, h)
    
    elif prism_type == 'cone':
        r, h = prism.radius, prism.height
        shape = Part.makeCone(r, 0, h)  # base radius = r, top radius = 0 for cone
    
    else:
        return {'error': f'Unknown prism type: {prism_type}'}
    
    # Export shape to STEP string or bytes (FreeCAD API dependent)
    # For example, save to file or convert to bytes
    # Here just returning a placeholder, replace with actual export code
    
    step_file_path = f"/tmp/{prism.designation}.step"
    shape.exportStep(step_file_path)
    
    return {'step_file_path': step_file_path}

