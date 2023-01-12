
from dataclasses import dataclass
import string

# Units are cm, kg, s


@dataclass
class GeometryParams:
    radius: float = 0.05335
    nbSections: int = 16
    nbFrames: int = 15
    totalLength: float = 15.

@dataclass
class PhysicsParams:
    youngModulus: float = 80.0e7
    poissonRatio: float = 0.33
    mass: float = 0.0865
    rayleighStiffness: float = 0.1


@dataclass
class FemParams:
    youngModulus: float = 20
    poissonRatio: float = 0.48
    mass: float = 0.3
    rayleigh: float = 0.1
    minVol: string = "16. -8. -5."
    maxVol: string = "40. 8. 5."
    mesh: string = "10 10 10"
    box: string = "15 -10 -10 41 -6 10"


@dataclass
class ContactParams:
    contactDistance: float = 0.01
    alarmDistance: float = 0.1
    dataMu: string = "mu=0.1"
    angleCone: float = "0.01"
    coneFactor: float = "0"


@dataclass
class NeedleParameters:
    # Geometry: GeometryParams = GeometryParams()
    # Physics: PhysicsParams = PhysicsParams()
    # Fem: FemParams = FemParams()
    # contact: ContactParams = ContactParams()
    def display():
        print(f'''
              # Geometry
              {string.ascii_uppercase[:4]}
              {string.ascii_uppercase[4:6]}
              {string.ascii_uppercase[6:8]}
              {string.ascii_uppercase[8:10]}
              '''
              )

@dataclass
class ConstraintsParams:
    constraintDistance: float = 1.3  # distance between two constraint points
    entryForce: float = 0  # The required force to penetrate the volume # about 0.7N in the literature, we have a bit less in our phantom

