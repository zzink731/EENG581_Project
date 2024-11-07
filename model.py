# %%
from dss import plot
from opendssdirect import dss
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

BASE_KV = 24  # kv (RMS, line to line)
PHASE_KV = BASE_KV / (3**0.5)

plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
# plot.enable(show=False)

CREATE_ANIMATION = False


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


def solution_case():
    dss.Commands("Edit Line.line1_2 Normamps=130 Emergamps=150")
    dss.Commands("Edit Line.line2_3 Normamps=130 Emergamps=150")
    dss.Commands("Edit Line.line23_25 Normamps=40 Emergamps=50")
    dss.Commands(
        "new Load.gen13 Bus1 = 13.1.2.3 Conn = Wye Model = 1 kv = 24 kw = -450 kvar = 0"
    )
    dss.Commands(
        "new Load.gen29 Bus1 = 29.1.2.3 Conn = Wye Model = 1 kv = 24 kw = -1300 kvar = 0"
    )

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


def plot_grid(ts):
    if ts == 20:
        dss.Text.Command("Buscoords data/node_positions.csv")
        # dss.Text.Command("plot circuit currents")
        dss.Text.Command = "Plot Circuit Linewidth=2 colorphases=yes"
        if CREATE_ANIMATION:
            plt.title(ts)
            plt.savefig(f"generated_images/current{ts}.png")

    # dss.Text.Command("plot scatter")


dss.Commands('Redirect "base_circuit.dss"')
dss.Solution.MaxControlIterations(20)


# solution_case()  # Edits OpenDSS model to include proposed improvements

dss.Solution.Solve()

voltages = []
currents = []
over_currents = []
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

    # plot_grid(ts)

    # currents at this timestep
    currents_ts = dict()
    this_ts_over_currents = []
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
            print(phase)
            if phase == 1 and current > emerg_amps:
                this_ts_over_currents.append(line)
                print(
                    f"({ts}) Line {line} is overloaded on Phase {phase}. Current: {current} A, EmergAmps: {emerg_amps} A"
                )
    over_currents.append(this_ts_over_currents)

df_over_currents = pd.DataFrame(
    {"hour": range(1, 25), "over_currents": [", ".join(lines) for lines in over_currents]}
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
        0,
        "Nodes increase in redness as they increase in number (number 34 is totally red)",
    )
# plt.legend()
# %%
# Must have ffmepg installed to run this part, can take a few minutes
# brew install ffmpeg
# Also need to add imageio and imageio-ffmpeg
# pip3 install imageio imageio-ffmpeg
import imageio

# filenames = glob.glob("./generated_images/current*.png")
images = []
for ts in range(0, 24):
    images.append(imageio.imread(f"./generated_images/current{ts}.png"))
imageio.mimsave("./generated_images/current_base.mp4", images)
