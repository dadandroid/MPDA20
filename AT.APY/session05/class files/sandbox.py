import clr
clr.AddReferenceToFile("kangarooSolver.dll")
import KangarooSolver as ks

from System.Collections.Generic import List
import Rhino.Geometry as rg
import scriptcontext as sc

if reset:

    PS = ks.PhysicalSystem()
    PS.ClearParticles()
    GoalList = List[ks.IGoal]()

    counter = 0

forceVec = rg.Vector3d(0,0, -z)

#remove last point from Polyline
for p in polylines:
    p.RemoveAt(p.Count - 1)

n0 = polylines[0].Count

tempCounter = counter % n0

poly = polylines[0][tempCounter]

PS.AddParticle(polylines[0][tempCounter], 0.001 ) #add this point to the particle system

#unary goal
GoalList.Add(ks.Goals.Unary(counter, forceVec ))

if(counter <n0):
    GoalList.Add(ks.Goals.Anchor (counter, PS.GetPosition(counter), 100000))


#create horizontal Springs
if counter != (counter/n0)  * tempCounter and counter != 0:
    GoalList.Add( ks.Goals.Spring(counter -1 , counter, 0 , 20 ))


#create vertical Springs
if counter > n0:
    GoalList.Add( ks.Goals.Spring(counter, counter - n0, 0 , 10 ))


counter +=1

PS.Step(GoalList, False, 0.001)

#expire the component (using the timer)
ghenv.Component.ExpireSolution(True)


A= PS.GetOutput(GoalList)
B= PS.GetPositions()
C = [poly]