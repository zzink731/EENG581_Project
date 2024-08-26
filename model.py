

from opendssdirect import dss
import pandas as pd

def load_dict_from_profiles(timestep : int):

    loads = {}
    cust_profiles = pd.read_csv("data/customer_profiles.csv")
    load_profiles = pd.read_csv("data/load_profiles.csv")

    for i in cust_profiles.index:
        node = cust_profiles.loc[i]["Node"]
        num_cust = cust_profiles.loc[i]["Num_Customers"]
        profile = cust_profiles.loc[i]["Demand_Profile"]
        
        loads["load"+str(node)] = load_profiles.loc[timestep]["Profile "+str(profile)] * num_cust

    return loads

def set_loads(loads : dict[str,float]):
    for load in loads:
        dss.Commands(f"Edit Load.{load} kw = {loads[load]} Pf = 0.9")

def compute_results():
    voltage_results = dss.Circuit.AllBusVMag()
    return voltage_results





dss.Commands('Redirect "base_circuit.dss"')

for ts in range(0,24):

    
    loads = load_dict_from_profiles(ts)
    set_loads(loads)

    dss.Solution.Solve()

    voltages = compute_results()
    print(voltages)
