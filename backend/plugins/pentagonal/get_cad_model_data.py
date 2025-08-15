import sys
sys.path.append('/usr/lib/freecad/lib')
sys.path.append('/usr/lib/freecad/')

import FreeCAD, Part, math

def get_cad_model_data(prism):
    """
    Create a regular pentagonal prism in FreeCAD.
    
    Parameters:
    radius : float : distance from center to vertex
    height : float : prism height
    
    Returns:
    Part.Shape : the pentagonal prism
    """
    if prism.prism_name == 'pentagonal':
        r, h = prism.radius, prism.height
        sides = 5 if prism.prism_name == 'pentagonal' else 6
        
        points = []
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            points.append(FreeCAD.Vector(x, y, 0))
        points.append(points[0])  # close the loop

        wire = Part.makePolygon(points)
        face = Part.Face(wire)
        shape = face.extrude(FreeCAD.Vector(0, 0, h))
    
    else:
        return {'error': f'Unknown prism type: {prism.prism_name}'}
    
    # Export shape to STEP string or bytes (FreeCAD API dependent)
    # For example, save to file or convert to bytes
    # Here just returning a placeholder, replace with actual export code
    
    step_file_path = f"/tmp/{prism.designation}.step"
    shape.exportStep(step_file_path)
    
    return {'step_file_path': step_file_path}
