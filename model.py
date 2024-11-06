# %%
from opendssdirect import dss
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

BASE_KV = 24  # kv (RMS, line to line)
PHASE_KV = BASE_KV / (3**0.5)


def load_dict_from_profiles(timestep: int):
    loads = {}
    cust_profiles = pd.read_csv("data/customer_profiles.csv")
    load_profiles = pd.read_csv("data/load_profiles.csv")

    for i in cust_profiles.index:
        node = cust_profiles.loc[i]["Node"]
        num_cust = cust_profiles.loc[i]["Num_Customers"]
        profile = cust_profiles.loc[i]["Demand_Profile"]

        loads["load" + str(node)] = (
            load_profiles.loc[timestep]["Profile " + str(profile)] * num_cust
        )

    return loads


def set_loads(loads: dict[str, float]):
    for load in loads:
        # bottom of page 1 of the project says to use a pf of 0.9
        dss.Commands(f"Edit Load.{load} kw = {loads[load]} Pf = 0.9")

def set_generation(ts: int):
    gen_13 = [0, 0, 0, 0, 300, 0, 0, 0, 0, 0, 0, 800,800, 0, 0, 0, -200, -300, -300, -2900, -2900, -2900, -1800, -800]
    gen_29 = [500, 500, 500, 500, 500, 500, 500, 500, 0, 0, 0, 0, 0, 0, 0, 0, -200, -500, -1500, -1500, -1600, -1600, -1600, -1500]

    #print(sum(gen_13))
    #print(sum(gen_29))
    solar_profile = pd.read_csv("data/solar_profiles.csv")
    solar_irrad_dict = {}
    for i in solar_profile.index:
        solar_irrad_dict[i] = solar_profile.loc[i]["Profile"]
    



    print("Solar power:",solar_irrad_dict[ts]*5)
    dss.Commands(f'edit Load.solar13 Bus1 = 13.1.2.3 Conn = Wye Model = 1 kv = 24 kw = -{solar_irrad_dict[ts]*5} kvar = 0')
    dss.Commands(f'edit Load.gen13 Bus1 = 13.1.2.3 Conn = Wye Model = 1 kv = 24 kw = {gen_13[ts]} kvar = 0')
    dss.Commands(f'edit Load.gen29 Bus1 = 29.1.2.3 Conn = Wye Model = 1 kv = 24 kw = {gen_29[ts]} kvar = 0')


    dss.Commands('edit Load.load22 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load30 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load31 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load32 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load33 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load34 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')

    dss.Commands('edit Load.load15 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load16 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load17 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('edit Load.load18 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')

def compute_results():
    voltage_results = dss.Circuit.AllBusVMag()
    return voltage_results

def solution_case():

    #Reconductoring
    #dss.Commands('Edit Line.line1_2 Normamps=130 Emergamps=150')
    #dss.Commands('Edit Line.line2_3 Normamps=130 Emergamps=150')
    #dss.Commands('Edit Line.line3_4 Normamps=130 Emergamps=150')
    dss.Commands('Edit Line.line23_25 Normamps=40 Emergamps=50')

    #Batteries, Wind
    dss.Commands('new Load.solar13 Bus1 = 13.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('new Load.gen13 Bus1 = 13.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    dss.Commands('new Load.gen29 Bus1 = 29.1.2.3 Conn = Wye Model = 1 kv = 24 kw = 0 kvar = 0')
    
    #Voltage Regulation
    dss.Commands('edit Line.line15_16 bus1 = rg.1.2.3')
    dss.Commands("""
    New Transformer.Reg1 phases=1 bank=reg1 XHL=0.01 kVAs=[800 800]
    ~ Buses=[15.1 rg.1] kVs=[13.87  13.87] %LoadLoss=0.01
    new regcontrol.Reg1  transformer=Reg1 winding=2  vreg=140  band=1  ptratio=100

    New Transformer.Reg2 phases=1 bank=reg1 XHL=0.01 kVAs=[800 800]
    ~ Buses=[15.2 rg.2] kVs=[13.87  13.87] %LoadLoss=0.01
    new regcontrol.Reg2  transformer=Reg2 winding=2  vreg=140  band=1  ptratio=100

    New Transformer.Reg3 phases=1 bank=reg1 XHL=0.01 kVAs=[800 800]
    ~ Buses=[15.3 rg.3] kVs=[13.87 13.87] %LoadLoss=0.01
    new regcontrol.Reg3  transformer=Reg3 winding=2  vreg=140  band=1  ptratio=100
    """)



dss.Commands('Redirect "base_circuit.dss"')
dss.Solution.MaxControlIterations(20)

 
solution_case() #Edits OpenDSS model to include proposed improvements

dss.Solution.Solve()

voltages = []
currents = []
for ts in range(0, 24):
    loads = load_dict_from_profiles(ts)
    set_loads(loads)
    set_generation(ts)
    dss.Solution.Solve()

    results = compute_results()
    # get the average voltage for each bus (we are doing three-phase loads so they are all the same)
    node_voltage_averages = [
        (results[i] + results[i + 1] + results[i + 2]) / 3
        for i in range(0, len(results), 3)
    ]

    power = 0
    for load in dss.Loads.AllNames():
        dss.Loads.Name(load)
        power += dss.Loads.kW()
    print(ts,"net power:",power)

    voltages.append(node_voltage_averages)

    lines = dss.Lines.AllNames()

    # currents at this timestep
    currents_ts = dict()
    for line in lines:
        # Set the active line
        dss.Lines.Name(line)

        # Retrieve the current values in amperes (returns values per phase)
        currents = dss.CktElement.CurrentsMagAng()  # Magnitude and angle of currents

        # Extract magnitude values for each phase (assuming a three-phase line)
        currents_magnitude = currents[::2][
            :3
        ]  # Get the magnitudes for the first three phases

        # Get the normal and emergency ampacity ratings for the line
        norm_amps = dss.Lines.NormAmps()
        emerg_amps = dss.Lines.EmergAmps()

        # Check for overload condition
        for phase, current in enumerate(currents_magnitude, start=1):
            if current > emerg_amps:
                print(
                    f"({ts}) Line {line} is overloaded on Phase {phase}. Current: {current} A, EmergAmps: {emerg_amps} A"
                )


# Transform the list
voltage_timeseries = [list(item) for item in zip(*voltages)]


cmap = cm.get_cmap("rainbow", 34)
for i, bus_voltages in enumerate(voltage_timeseries):
    plt.plot(
        [v / (PHASE_KV * 1000) for v in bus_voltages], label=f"bus {i}", color=cmap(i)
    )
    plt.xlabel("time [hours]")
    plt.ylabel("voltage [pu]")
    plt.text(
        0,
        0.6,
        "Nodes increase in redness as they increase in number (number 34 is totally red)",
    )
# %%
