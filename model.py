

from opendssdirect import dss

def load_dict_from_profiles(timestep):
    
    loads = {}
    return loads

def set_loads(loads : dict[str,float]):
    for load in loads:
        dss.Commands(f"Edit Load.{load} kw = {loads[load]} Pf = 0.9")

def compute_results():
    results = dss.Circuit.AllBusVMag()
    return results


dss.Commands('Redirect "base_circuit.dss"')


timesteps = [ts for ts in range(0,24)]

for ts in timesteps:
    loads = load_dict_from_profiles(ts)
    set_loads(loads)
    dss.Solution.Solve()

    print(compute_results)
