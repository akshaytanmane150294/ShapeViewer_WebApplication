# myPrismApp/backend/prisms/cad_utils.py

import FreeCAD
import Part
import Mesh

def step_to_stl(step_path, stl_path):
    shape = Part.Shape()
    shape.read(step_path)
    mesh = Mesh.Mesh()
    mesh.addFacets(shape.tessellate(0.5))
    mesh.write(stl_path)
    return stl_path
