# ~~Mohagheghi's Minions~~ AC/DC Solutions (All Current/Direct Convenience) Consulting

![minions](./minions.webp)

# Install dependencies
```
pip3 install OpenDSSDirect.py pandas
```

## Set up
To create the base circuit dss file, run 
```python
python3 ./scripts/create_base_circuit.py
```

This populates the lengths between nodes...it should probably add the impedances too.

Questions 
- the Normamps parameter is per phase. I think the line capacities given in the problem actually were meant to be per phase, not three-phase values. Can someone confirm/deny?