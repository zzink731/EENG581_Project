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
    print("TOTAL LOADS", sum(loads.values()))

    return loads


def set_loads(loads: dict[str, float]):
    for load in loads:
        # bottom of page 1 of the project says to use a pf of 0.9
        dss.Commands(f"Edit Load.{load} kw = {loads[load]} Pf = 0.9")


def compute_results():
    voltage_results = dss.Circuit.AllBusVMag()
    return voltage_results


dss.Commands('Redirect "base_circuit.dss"')

voltages = []
currents = []
for ts in range(0, 24):
    loads = load_dict_from_profiles(ts)
    set_loads(loads)

    dss.Solution.Solve()

    results = compute_results()
    # get the average voltage for each bus (we are doing three-phase loads so they are all the same)
    node_voltage_averages = [
        (results[i] + results[i + 1] + results[i + 2]) / 3
        for i in range(0, len(results), 3)
    ]

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
