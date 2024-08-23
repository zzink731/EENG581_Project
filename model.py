

from opendssdirect import dss




dss.Command('Redirect "base_circuit.dss"')
dss.Solution.Solve()


print(dss.Circuit.AllBusNames())
print(dss.Loads.AllNames())
print(dss.Lines.AllNames())