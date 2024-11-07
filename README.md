# ~~Mohagheghi's Minions~~ AC/DC Solutions (All Current/Direct Convenience) Consulting

![minions](./minions.webp)

# Install dependencies
```
pip3 install OpenDSSDirect.py pandas altdss dss-python[plot]
```

## Set up
To create the base circuit dss file, run 
```python
python3 ./scripts/create_base_circuit.py
```

This populates the lengths between nodes.

## Questions
- Should we consider an outage at 1.25x the line capacity or just anything above the line capacity?