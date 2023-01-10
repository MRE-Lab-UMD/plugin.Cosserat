# Required import for python
import Sofa
import sys

sys.path.append('../')

# Choose in your script to activate or not the GUI
USE_GUI = True


def main():
    import SofaRuntime
    import Sofa.Gui
    SofaRuntime.importPlugin("SofaOpenglVisual")
    SofaRuntime.importPlugin("SofaImplicitOdeSolver")

    root = Sofa.Core.Node("root")
    createScene(root)
    Sofa.Simulation.init(root)

    if not USE_GUI:
        for iteration in range(10):
            Sofa.Simulation.animate(root, root.dt.value)
    else:
        Sofa.Gui.GUIManager.Init("myscene", "qglviewer")
        Sofa.Gui.GUIManager.createGUI(root, __file__)
        Sofa.Gui.GUIManager.SetDimension(1080, 1080)
        Sofa.Gui.GUIManager.MainLoop(root)
        Sofa.Gui.GUIManager.closeGUI()


def createScene(root):
    root.gravity=[0, 0, 0]
    root.dt=0.01

    root.addObject('DefaultAnimationLoop')

    root.addObject('VisualStyle', displayFlags="showVisualModels showCollisionModels showInteractionForceFields showBehaviorModels")

    # List of required plugins 
    root.addObject('RequiredPlugin', pluginName = "Sofa.Component.AnimationLoop")
    root.addObject('RequiredPlugin', pluginName = "Sofa.Component.Constraint.Lagrangian.Correction")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Constraint.Lagrangian.Solver")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Constraint.Projective")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Engine.Select")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Engine.Transform")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.LinearSolver.Direct")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.LinearSolver.Iterative")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Mapping.Linear")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Mass")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.MechanicalLoad")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.ODESolver.Backward")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.SolidMechanics.FEM.Elastic")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.StateContainer")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Topology.Container.Dynamic")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Topology.Container.Grid")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Topology.Mapping")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.Visual")
    root.addObject("RequiredPlugin", pluginName = "Sofa.GL.Component.Rendering3D")
    root.addObject("RequiredPlugin", pluginName = "Sofa.Component.SolidMechanics.Spring")

    # Constraints solver
    root.addObject('GenericConstraintSolver', maxIterations = "500", tolerance = "0.0002", computeConstraintForces = "true")

    # Topology information
    topo = root.addChild('Topology')
    topo.addObject('RegularGridTopology' , name = 'HexaTop', n = "9 9 18", min = "-0.05 -0.05 0.210", max = "0.05 0.05 0.295")
    topo.addObject('TetrahedronSetTopologyContainer', name = "Container", position = "@HexaTop.position")
    topo.addObject('TetrahedronSetTopologyModifier' , name = "Modifier")
    topo.addObject('Hexa2TetraTopologicalMapping', input = "@HexaTop", output="@Container", swapping="false")

    # FEM informationm
    fem = root.addChild('FEM')
    fem.addObject('EulerImplicitSolver', rayleighMass = "0.1", rayleighStiffness="0.1", vdamping="0.5")
    fem.addObject('ShewchukPCGLinearSolver', preconditioner="@precond", update_step="15")
    fem.addObject('SparseLDLSolver', name="precond", template="CompressedRowSparseMatrixMat3x3d")
    fem.addObject('TetrahedronSetTopologyContainer', name="Container", position="@../Topology/HexaTop.position", tetrahedra="@../Topology/Container.tetrahedra")
    fem.addObject('TetrahedronSetTopologyModifier', name = "Modifier")
    
    fem.addObject('MechanicalObject', name="mstate", template="Vec3d", showIndices="0")
    # fem.addObject('BoxConstraint', name = "support", box ="-0.06 -0.06 0.29 0.06 0.06 0.295", drawBoxes="true" )
    
    fem.addObject('BoxROI', name='BoxConstraint', box='-0.07 -0.07 0.28 0.07 0.07 0.3', drawBoxes='true')
    fem.addObject('RestShapeSpringsForceField', points='@BoxConstraint.indices', stiffness='1e12')

    fem.addObject("BoxROI", name="Gel1", box="-0.05 -0.05 0.210 0.05 0.05 0.225", drawBoxes="false")
    fem.addObject("BoxROI", name="Gel2", box="-0.05 -0.05 0.2245 0.05 0.05 0.245", drawBoxes="false")
    fem.addObject("BoxROI", name="Gel3", box="-0.05 -0.05 0.245 0.05 0.05 0.260", drawBoxes="false")
    fem.addObject("BoxROI", name="Gel4", box="-0.05 -0.05 0.260 0.05 0.05 0.295", drawBoxes="false")

    fem.addObject("IndexValueMapper", name="Young1", indices="@Gel1.tetrahedronIndices", value="3e4")
    fem.addObject("IndexValueMapper", name="Young2", indices="@Gel2.tetrahedronIndices", value="3e4", inputValues="@Young1.outputValues")
    fem.addObject("IndexValueMapper", name="Young3", indices="@Gel3.tetrahedronIndices", value="3e4", inputValues="@Young2.outputValues")
    fem.addObject("IndexValueMapper", name="Young4", indices="@Gel4.tetrahedronIndices", value="3e4", inputValues="@Young3.outputValues")
    fem.addObject("TetrahedronFEMForceField", youngModulus="@Young4.outputValues", poissonRatio="0.4")

    # Apply forces here
    fem.addObject("ConstantForceField", force="0 0 0")
    fem.addObject("UniformMass", totalMass = "0.3")

    fem.addObject("BoxROI", name="Surf1", box="-0.05 -0.05 0.2095 0.05 0.05 0.2105", drawBoxes="false")
    fem.addObject("BoxROI", name="Surf2", box="-0.05 -0.05 0.2245 0.05 0.05 0.2255", drawBoxes="false")
    fem.addObject("BoxROI", name="Surf3", box="-0.05 -0.05 0.2445 0.05 0.05 0.2455", drawBoxes="false")
    fem.addObject("BoxROI", name="Surf4", box="-0.05 -0.05 0.2595 0.05 0.05 0.2605", drawBoxes="false")

    # Surfaces information
    surfaces = fem.addChild("Surfaces")

    surface1 = surfaces.addChild("Surface1")
    surface1.addObject("TriangleSetTopologyContainer", name = "Container", triangles = "@../../Surf1.trianglesInROI")
    surface1.addObject("TriangleSetTopologyModifier", name = "Modifier")
    surface1.addObject("MechanicalObject", name = "dofs")
    surface1.addObject("IdentityMapping", name = "SurfaceMapping")

    surface2 = surfaces.addChild("Surface2")
    surface2.addObject("TriangleSetTopologyContainer", name = "Container", triangles = "@../../Surf2.trianglesInROI")
    surface2.addObject("TriangleSetTopologyModifier", name = "Modifier")
    surface2.addObject("MechanicalObject", name = "dofs")
    surface2.addObject("IdentityMapping", name = "SurfaceMapping")

    surface3 = surfaces.addChild("Surface3")
    surface3.addObject("TriangleSetTopologyContainer", name = "Container", triangles = "@../../Surf3.trianglesInROI")
    surface3.addObject("TriangleSetTopologyModifier", name = "Modifier")
    surface3.addObject("MechanicalObject", name = "dofs")
    surface3.addObject("IdentityMapping", name = "SurfaceMapping")

    surface4 = surfaces.addChild("Surface4")
    surface4.addObject("TriangleSetTopologyContainer", name = "Container", triangles = "@../../Surf4.trianglesInROI")
    surface4.addObject("TriangleSetTopologyModifier", name = "Modifier")
    surface4.addObject("MechanicalObject", name = "dofs")
    surface4.addObject("IdentityMapping", name = "SurfaceMapping")

    # Visualization and all the mapping
    visual = fem.addChild("Visual")

    visualgel1 = visual.addChild("VisualGel1", activated = "1")
    visualgel1.addObject("TriangleSetTopologyContainer", name="Container", triangles="@../../Gel1.trianglesInROI")
    visualgel1.addObject("OglModel", color="0 0.7 1 0.2", name="visualModel")
    visualgel1.addObject("BarycentricMapping", name="VisualMapping")

    visualgel2 = visual.addChild("VisualGel2", activated = "1")
    visualgel2.addObject("TriangleSetTopologyContainer", name="Container", triangles="@../../Gel2.trianglesInROI")
    visualgel2.addObject("OglModel", color="0.8 0.3 1 0.2", name="visualModel")
    visualgel2.addObject("BarycentricMapping", name="VisualMapping")

    visualgel3 = visual.addChild("VisualGel3", activated = "1")
    visualgel3.addObject("TriangleSetTopologyContainer", name="Container", triangles="@../../Gel3.trianglesInROI")
    visualgel3.addObject("OglModel", color="0.2 0.6 0.5 0.2", name="visualModel")
    visualgel3.addObject("BarycentricMapping", name="VisualMapping")

    visualgel4 = visual.addChild("VisualGel4", activated = "1")
    visualgel4.addObject("TriangleSetTopologyContainer", name="Container", triangles="@../../Gel4.trianglesInROI")
    visualgel4.addObject("OglModel", color="1 1 0.2 0.2", name="visualModel")
    visualgel4.addObject("BarycentricMapping", name="VisualMapping")

    fem.addObject("LinearSolverConstraintCorrection", linearSolver = "@precond")

    return root


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    main()