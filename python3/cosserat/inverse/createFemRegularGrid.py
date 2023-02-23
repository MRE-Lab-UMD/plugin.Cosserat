# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""Basic scene using Cosserat in SofaPython3.

Based on the work done with SofaPython. See POEMapping.py
"""

__authors__ = "younesssss"
__contact__ = "adagolodjo@protonmail.com, yinoussa.adagolodjo@inria.fr"
__version__ = "1.0.0"
__copyright__ = "(c) 2021,Inria"
__date__ = "March 16 2021"


def createFemCube(parentNode):
    FemNode = parentNode.addChild("FemNode")
    FemNode.addObject('VisualStyle', displayFlags='showBehaviorModels hideCollisionModels hideBoundingCollisionModels '
                                                  'showForceFields hideInteractionForceFields showWireframe')
    gelVolume = FemNode.addChild("gelVolume")
    gelVolume.addObject("RegularGridTopology", name="HexaTop", n="6 6 6", min="40 -16 -10", max="100 20 10")
    gelVolume.addObject("TetrahedronSetTopologyContainer", name="Container", position="@HexaTop.position")
    gelVolume.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    gelVolume.addObject("Hexa2TetraTopologicalMapping", input="@HexaTop", output="@Container", swapping="false")

    GelSurface = FemNode.addChild("GelSurface")
    GelSurface.addObject("TriangleSetTopologyContainer", name="Container", position="@../GelVolume/HexaTop.position")
    # GelSurface.addObject("TriangleSetTopologyModifier", input="@../GelVolume/Container", output="@Container",
    #                      flipNormals="false")

    gelNode = FemNode.addChild("gelNode")
    # gelNode.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels '
    #                                                  'hideMappings hideForceFields showWireframe '
    #                                                  'showInteractionForceFields hideForceFields')
    gelNode.addObject("EulerImplicitSolver", rayleighMass="0.1", rayleighStiffness="0.1")
    gelNode.addObject('SparseLDLSolver', name='preconditioner')
    gelNode.addObject('TetrahedronSetTopologyContainer', src="@../gelVolume/Container", name='container')
    # gelNode.addObject('TetrahedronSetTopologyModifier')
    gelNode.addObject('MechanicalObject', name='tetras', template='Vec3d')
    gelNode.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large',
                      poissonRatio='0.45', youngModulus='100')
    # gelNode.addObject('UniformMass', totalMass='5')
    # gelNode.addObject('BoxROI', name='ROI1', box='40 -17 -10 100 -14 10', drawBoxes='true')
    # gelNode.addObject('RestShapeSpringsForceField', points='@ROI1.indices', stiffness='1e12')

    surfaceNode = gelNode.addChild("surfaceNode")
    surfaceNode.addObject('TriangleSetTopologyContainer', name="surfContainer", src="@../../GelSurface/Container")
    surfaceNode.addObject('MechanicalObject', name='msSurface')
    surfaceNode.addObject('TriangleCollisionModel', name='surface')
    surfaceNode.addObject('LineCollisionModel', name='line')
    surfaceNode.addObject('BarycentricMapping')

    gelNode.addObject('LinearSolverConstraintCorrection')

    return FemNode


def createFemCubeWithParamsJHU(parentNode, geometry):

    FemNode = parentNode.addChild("FemNode")
    # FemNode.addObject('VisualStyle', displayFlags='showBehaviorModels hideCollisionModels
    # hideBoundingCollisionModels ' 'showForceFields hideInteractionForceFields showWireframe')
    gelVolume = FemNode.addChild("gelVolume")
    gelVolume.addObject("RegularGridTopology", name="HexaTop", n=geometry.mesh, min=geometry.minVol,
                        max=geometry.maxVol)
    gelVolume.addObject("TetrahedronSetTopologyContainer", name="TetraContainer", position="@HexaTop.position")
    gelVolume.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    gelVolume.addObject("Hexa2TetraTopologicalMapping", input="@HexaTop", output="@TetraContainer", swapping="false")

    GelSurface = FemNode.addChild("GelSurface")
    GelSurface.addObject("TriangleSetTopologyContainer", name="triangleContainer",
                         position="@../gelVolume/HexaTop.position")
    GelSurface.addObject("TriangleSetTopologyModifier", name="Modifier")
    GelSurface.addObject("Tetra2TriangleTopologicalMapping", input="@../gelVolume/TetraContainer",
                         output="@triangleContainer", flipNormals="false")

    gelNode = FemNode.addChild("gelNode")

    gelNode.addObject("EulerImplicitSolver", rayleighMass=geometry.rayleigh, rayleighStiffness=geometry.rayleigh)
    gelNode.addObject('SparseLDLSolver', name='precond')
    gelNode.addObject('TetrahedronSetTopologyContainer', tetrahedra="@../gelVolume/TetraContainer.tetrahedra", name='container', position="@../gelVolume/HexaTop.position")
    # gelNode.addObject('TetrahedronSetTopologyModifier', name = "Modifier")
    gelNode.addObject('MechanicalObject', name='tetras', template='Vec3d')

    # gelNode.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large',
    #                   poissonRatio=geometry.poissonRatio, youngModulus=geometry.youngModulus)
    gelNode.addObject('BoxROI', name='ROI1', box=geometry.box, drawBoxes='true')
    gelNode.addObject('RestShapeSpringsForceField', points='@ROI1.indices', stiffness='1e12')

    gelNode.addObject("BoxROI", name="Gel1", box="16. -8. -5. 25. 8. 5.", drawBoxes="true" , drawPoints = "0", drawTetrahedra = "0", drawSize = "2")
    gelNode.addObject("BoxROI", name="Gel2", box="25. -8. -5. 40. 8. 5.", drawBoxes="true", drawPoints = "0", drawTetrahedra = "0", drawSize = "2")

    gelNode.addObject("IndexValueMapper", name="Young1", indices="@Gel1.tetrahedronIndices", value="3e4")
    gelNode.addObject("IndexValueMapper", name="Young2", indices="@Gel2.tetrahedronIndices", value="3e4", inputValues="@Young1.outputValues")
    gelNode.addObject("TetrahedronFEMForceField", template = "Vec3d", youngModulus="@Young2.outputValues", poissonRatio="0.4")
    # gelNode.addObject("UniformMass", totalMass = "0.3")

    # gelNode.addObject("BoxROI", name="Surf1", box="13. -8. -5. 30. 8. 5.", drawBoxes="false")
    # gelNode.addObject("BoxROI", name="Surf2", box="25. -8. -5. 45. 8. 5.", drawBoxes="false")

    gelNode.addObject("BoxROI", name="Surf1", box="16. -8. -5. 26. 8. 5.", drawBoxes="false")
    gelNode.addObject("BoxROI", name="Surf2", box="25. -8. -5. 40. 8. 5.", drawBoxes="false")

    surfaceNode = gelNode.addChild("surfaceNode")
    surfaceNode.addObject('TriangleSetTopologyContainer', name="surfContainer",
                          src="@../../GelSurface/triangleContainer")
    surfaceNode.addObject('MechanicalObject', name='msSurface')
    surfaceNode.addObject('TriangleCollisionModel', name='surface')
    surfaceNode.addObject('LineCollisionModel', name='line')
    surfaceNode.addObject('BarycentricMapping')
    visu = surfaceNode.addChild("visu")

    visu.addObject("OglModel", name="Visual", src="@../surfContainer",  color="0.0 0.1 0.9 0.40" )
    visu.addObject("BarycentricMapping", input="@..", output="@Visual")

    # gelNode.addObject('GenericConstraintCorrection', linearSolver='@precond')
    gelNode.addObject('LinearSolverConstraintCorrection')

    # Visualize multiple surfaces
    # surfaceNode = gelNode.addChild("surfaceNode")
    # surfaceNode.addObject('TriangleSetTopologyContainer', name="surfContainer", src="@../../gelNode/container")

    # surface1 = surfaceNode.addChild("Surface1")
    # surface1.addObject("TriangleSetTopologyContainer", name = "Container1", triangles = "@../../Surf1.trianglesInROI")
    # surface1.addObject("TriangleSetTopologyModifier", name = "Modifier")
    # surface1.addObject("MechanicalObject", name = "dofs")
    # surface1.addObject("IdentityMapping", name = "SurfaceMapping")

    # surface2 = surfaceNode.addChild("Surface2")
    # surface2.addObject("TriangleSetTopologyContainer", name = "Container2", triangles = "@../../Surf2.trianglesInROI")
    # surface2.addObject("TriangleSetTopologyModifier", name = "Modifier")
    # surface2.addObject("MechanicalObject", name = "dofs")
    # surface2.addObject("IdentityMapping", name = "SurfaceMapping")

    # surfaceNode.addObject('TriangleCollisionModel', name='surface')
    # surfaceNode.addObject('LineCollisionModel', name='line')

    # visu = surfaceNode.addChild("visu")
    # visualgel1 = visu.addChild("VisualGel1", activated = "1")
    # visualgel1.addObject("TriangleSetTopologyContainer", name="Container", triangles="@../../Surface1/Container1.trianglesInROI")
    # visualgel1.addObject("OglModel", name="Visual1", color="0.0 0.1 0.9 0.40", src = "@../../Surface1/Container1")
    # visualgel1.addObject("BarycentricMapping", input="@..", output="@Visual1")

    # visualgel2 = visu.addChild("VisualGel2", activated = "1")
    # visualgel2.addObject("TriangleSetTopologyContainer", name="Container", triangles="@../../Surface2/Container2.trianglesInROI")
    # visualgel2.addObject("OglModel", name = "Visual2", color="1.0 1.0 1.0 1.0", src = "@../../Surface2/Container2")
    # visualgel2.addObject("BarycentricMapping", input="@..", output="@Visual2")

    # # gelNode.addObject('GenericConstraintCorrection', linearSolver='@precond')
    # gelNode.addObject('LinearSolverConstraintCorrection', linearSolver = "@precond")

    return FemNode

def createFemCubeWithParams(parentNode, geometry):
    
    FemNode = parentNode.addChild("FemNode")
    # FemNode.addObject('VisualStyle', displayFlags='showBehaviorModels hideCollisionModels
    # hideBoundingCollisionModels ' 'showForceFields hideInteractionForceFields showWireframe')
    gelVolume = FemNode.addChild("gelVolume")
    gelVolume.addObject("RegularGridTopology", name="HexaTop", n=geometry.mesh, min=geometry.minVol,
                        max=geometry.maxVol)
    cont = gelVolume.addObject("TetrahedronSetTopologyContainer", name="TetraContainer", position="@HexaTop.position")
    gelVolume.addObject("TetrahedronSetTopologyModifier", name="Modifier")
    gelVolume.addObject("Hexa2TetraTopologicalMapping", input="@HexaTop", output="@TetraContainer", swapping="false")

    GelSurface = FemNode.addChild("GelSurface")
    GelSurface.addObject("TriangleSetTopologyContainer", name="triangleContainer",
                         position="@../gelVolume/HexaTop.position")
    GelSurface.addObject("TriangleSetTopologyModifier", name="Modifier")
    GelSurface.addObject("Tetra2TriangleTopologicalMapping", input="@../gelVolume/TetraContainer",
                         output="@triangleContainer", flipNormals="false")

    gelNode = FemNode.addChild("gelNode")
    # gelNode.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels showCollisionModels '
    #                                                  'hideMappings hideForceFields showWireframe '
    #                                                  'showInteractionForceFields hideForceFields')
    gelNode.addObject("EulerImplicitSolver", rayleighMass=geometry.rayleigh, rayleighStiffness=geometry.rayleigh)
    gelNode.addObject('SparseLDLSolver', name='precond')
    # gelNode.addObject('ShewchukPCGLinearSolver', name='linearSolver', iterations='500', tolerance='1.0e-14',
    #                   preconditioners="precond")
    # gelNode.addObject('SparseLDLSolver', name='precond', template='CompressedRowSparseMatrix3d')
    gelNode.addObject('TetrahedronSetTopologyContainer', src="@../gelVolume/TetraContainer", name='container')
    # gelNode.addObject('TetrahedronSetTopologyModifier')
    gelNode.addObject('MechanicalObject', name='tetras', template='Vec3d')
    gelNode.addObject('TetrahedronFEMForceField', template='Vec3d', name='FEM', method='large',
                      poissonRatio=geometry.poissonRatio, youngModulus=geometry.youngModulus)
    # gelNode.addObject('UniformMass', totalMass='5')
    gelNode.addObject('BoxROI', name='ROI1', box=geometry.box, drawBoxes='true')
    gelNode.addObject('RestShapeSpringsForceField', points='@ROI1.indices', stiffness='1e12')

    surfaceNode = gelNode.addChild("surfaceNode")
    surfaceNode.addObject('TriangleSetTopologyContainer', name="surfContainer",
                          src="@../../GelSurface/triangleContainer")
    surfaceNode.addObject('MechanicalObject', name='msSurface')
    surfaceNode.addObject('TriangleCollisionModel', name='surface')
    surfaceNode.addObject('LineCollisionModel', name='line')
    surfaceNode.addObject('BarycentricMapping')
    visu = surfaceNode.addChild("visu")

    visu.addObject("OglModel", name="Visual", src="@../surfContainer",  color="0.0 0.1 0.9 0.40" )
    visu.addObject("BarycentricMapping", input="@..", output="@Visual")

    # gelNode.addObject('GenericConstraintCorrection', linearSolver='@precond')
    gelNode.addObject('LinearSolverConstraintCorrection')

    return FemNode