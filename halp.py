from gamspy import Container, Set, Variable

# Initialize the model container
m = Container()

# Define the set 't' with specific elements
t = Set(m, name="t", records=["t1", "t2", "t3"])

# Define the variable 'SOC' over the set 't'
SOC = Variable(m, name="SOC", domain=t, type="positive")

# Set the upper bound for 'SOC' to 1
SOC.up = 1

# Fix 'SOC' at element 't2' to a value of 0.5
SOC["t2"].fx = 0.5