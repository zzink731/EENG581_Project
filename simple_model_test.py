# %%
from opendssdirect import dss

dss.Commands('Redirect "simple_test.dss"')
dss.Solution.Solve()

lines = dss.Lines.AllNames()

for line in lines:
    # Set the active line
    dss.Lines.Name(line)

    # Retrieve the current values in amperes (returns values per phase)
    currents = dss.CktElement.CurrentsMagAng()  # Magnitude and angle of currents

    currents_magnitude = currents[::2][
        :3
    ]  # Get the magnitudes for the first three phases
    print("current magnitudes", currents_magnitude)

    # Get the normal and emergency ampacity ratings for the line
    norm_amps = dss.Lines.NormAmps()
    emerg_amps = dss.Lines.EmergAmps()