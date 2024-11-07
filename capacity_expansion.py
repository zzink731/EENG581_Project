#  %%
from gamspy import (
    Container,
    Set,
    Parameter,
    Variable,
    Equation,
    Model,
    Sum,
    Sense,
    Problem,
)
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from IPython.display import display

plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300

COST_OF_CARBON = 150  # $/ton of CO2 emissions


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


solar = pd.read_csv("data/solar_profiles.csv")
loads = [sum(load_dict_from_profiles(ts).values()) for ts in range(24)]

data_emissions = {
    "coal_low": 0.8,
    "coal": 1,
    "gas": 0.557,
    "gas_cc": 0.45,
    "nuclear": 0,
    "solar_pv": 0,
    "hydro": 0,
    "battery": 0,
    "fuel_cell": 0,
}

df_emissions = pd.DataFrame(
    list(data_emissions.items()), columns=["Technology", "emissions_rate"]
)

# $/kW
data_capital_cost = {
    "coal_low": 3800,
    "coal": 0.1,  # if this was exactly zero, the model just adds like a gigawatt of coal LOL
    "gas": 700,
    "gas_cc": 1000,
    "nuclear": 1600,
    "solar_pv": 850,
    "hydro": 2500 * 10000,  # hydro is not considered for land use reasons
    "battery": 1400,  # 1400,
    "fuel_cell": 7200,
}

df_cap_cost = pd.DataFrame(
    list(data_capital_cost.items()), columns=["Technology", "cap_cost"]
)

# $/MWh
data_om_cost = {
    "coal_low": 110,
    "coal": 180,
    "gas": 80,
    "gas_cc": 60,
    "nuclear": 150,
    "solar_pv": 40,
    "hydro": 0,
    "battery": 0,
    "fuel_cell": 150,
}

df_om_cost = pd.DataFrame(list(data_om_cost.items()), columns=["Technology", "OM_cost"])


# days is days of O&M/emissions costs considered
def run_model(days):
    m = Container()
    g = Set(m, "generators", records=data_om_cost.keys())
    t = Set(m, "time", records=range(24))

    om_cost = Parameter(m, "om_cost", domain=g, records=df_om_cost)
    cap_cost = Parameter(m, "cap_cost", domain=g, records=df_cap_cost)
    emissions_rate = Parameter(m, "emissions_rate", domain=g, records=df_emissions)
    demand = Parameter(m, "demand", domain=t, records=np.array(loads))
    irradiance = Parameter(m, "irradiance", domain=t, records=solar.Profile)

    # active power from generation type at time t (for 1 hour, so could consider this "energy")
    P = Variable(m, "Power", domain=[g, t], type="positive")
    for time in range(24):
        P.lo["battery", str(time)] = -float("Inf")

    # capacity of generation type installed
    K = Variable(m, "Capacity", domain=g, type="positive")

    # state of charge of the battery from 0 to K["battery"]
    SOC = Variable(m, "SOC", domain=t, type="positive")

    eq_battery_max = Equation(m, "battery_max", domain=t)
    eq_battery_max[t] = SOC[t] <= K["battery"]

    eq_energy_balance = Equation(m, "energy_balance", domain=[t])
    eq_energy_balance[t] = SOC[t.lead(1, "circular")] == SOC[t] - P["battery", t]

    # generation must meet demand
    eq_supply_demand = Equation(m, "supply_demand_eq", domain=[t])
    eq_supply_demand[t] = Sum(g, P[g, t]) == demand[t] - (P["battery", t])

    # generation can't exceed installed capacity
    eq_capacity = Equation(m, "capacity_eq", domain=[g, t])
    eq_capacity[g, t] = P[g, t] <= K[g]

    # solar generation is limited by irradiance amount
    eq_solar_capacity = Equation(m, "solar_eq", domain=[g, t])
    eq_solar_capacity[g, t] = P["solar_pv", t] <= irradiance[t] / 1000 * K["solar_pv"]

    OM_Cost = Variable(m, "OM_cost_variable")
    Cap_Cost = Variable(m, "Cap_cost_variable")
    Emissions_Cost = Variable(m, "Emissions_Cost_variable")

    eq_cost_om = Equation(m, "eq_cost_om")
    eq_cost_cap = Equation(m, "eq_cost_cap")
    eq_cost_emissions = Equation(m, "eq_cost_emissions")

    eq_cost_om[...] = OM_Cost == Sum([g, t], P[g, t] * om_cost[g])
    eq_cost_cap[...] = Cap_Cost == Sum([g], K[g] * cap_cost[g])
    eq_cost_emissions[...] = Emissions_Cost == Sum(
        [g, t], P[g, t] * emissions_rate[g] * COST_OF_CARBON
    )

    TotalCost = Variable(m, "total_cost")
    eq_cost = Equation(m, "total_cost_calc")
    # if you only consider a single day, OM costs and emissions costs are negligible, but the reality
    # is that those generating units will operate more than just this one day
    eq_cost[...] = TotalCost == Cap_Cost + days * (OM_Cost + Emissions_Cost)

    capacity_expansion = Model(
        m,
        "capacity_expansion",
        equations=m.getEquations(),
        problem=Problem.LP,
        sense=Sense.MIN,
        objective=TotalCost,
    )
    capacity_expansion.solve()
    print("STATUS:", capacity_expansion.status)

    generation_chosen = P.records[P.records.level > 1e-6]

    display(P.records[abs(P.records.level) > 1e-6])
    display(generation_chosen)
    display(Emissions_Cost.records)
    display(SOC.records)
    print("cost considering carbon", TotalCost.records.iloc[0].level)
    print(
        "cost without carbon",
        OM_Cost.records.iloc[0].level + Cap_Cost.records.iloc[0].level,
    )

    fig, axs = plt.subplots(2, gridspec_kw={"height_ratios": [3, 1]})
    ax = axs[0]
    ax2 = axs[1]
    ax.grid(color="gray", linestyle="-", linewidth=0.5, alpha=0.2)
    ax2.grid(color="gray", linestyle="-", linewidth=0.5, alpha=0.2)
    ax2.fill_between(
        range(24),
        np.zeros(24),
        SOC.records.level / max(SOC.records.level),
        color="xkcd:pale purple",
    )
    ax2.set_ylabel("Battery SOC")
    ax2.set_ylim(0, 1)
    ax.set_title(f"{days} day(s) of O&M and Emissions costs considered")
    ax.set_xlim(0, 23)
    ax2.set_xlim(0, 23)
    ax2.set_xlabel("hour of day")
    ax.set_ylabel("MW generation")

    colors = {
        "coal": "xkcd:dark",
        "gas_cc": "xkcd:ruby",
        "gas": "xkcd:gross green",
        "solar_pv": "xkcd:saffron",
        "battery": "xkcd:deep lavender",
    }
    for gen_type in generation_chosen.generators.unique():
        ax.plot(
            range(24),
            (P.records[P.records.generators == gen_type]).level,
            label=gen_type,
            color=colors[gen_type],
        )
    ax.legend(loc="upper left")

    plt.savefig(f"generated_images/{days}-capacity-expansion.png")


for i in range(1, 10):
    run_model(i)
