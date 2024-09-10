from collections import namedtuple
import csv

Node = namedtuple("Node", ["x", "y"])

node_positions = {}
with open("data/node_positions.csv", mode="r") as file:
    csvFile = csv.reader(file)

    # skip header
    next(csvFile)
    for row in csvFile:
        node_positions[int(row[0])] = Node(float(row[1]), y=float(row[2]))

def distance(nodeA_name, nodeB_name):
    nodeA = node_positions[nodeA_name]
    nodeB = node_positions[nodeB_name]

    # all nodes are adjacent to each other, so they should already match either in x or y coord, if they don't something is wrong
    if (nodeA.x != nodeB.x) & (nodeA.y != nodeB.y):
        raise Exception(f"Something is wrong with node {nodeA_name} and {nodeB_name}")

    return round(((nodeA.x - nodeB.x) ** 2 + (nodeA.y - nodeB.y) ** 2) ** 0.5, 2)


with open("base_circuit.dss", "w") as file:
    file.write(f"""
clear

new circuit.Base34NodeCkt basekv = 24 pu = 1.0 phases = 3 bus1 = 1 MVAsc3=20000 MVASC1=21000

new Load.load1 Bus1 = 1.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0
new Load.load2 Bus1 = 2.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load3 Bus1 = 3.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load4 Bus1 = 4.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load5 Bus1 = 5.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load6 Bus1 = 6.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load7 Bus1 = 7.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load8 Bus1 = 8.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load9 Bus1 = 9.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load10 Bus1 = 10.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load11 Bus1 = 11.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load12 Bus1 = 12.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load13 Bus1 = 13.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load14 Bus1 = 14.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load15 Bus1 = 15.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load16 Bus1 = 16.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load17 Bus1 = 17.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load18 Bus1 = 18.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0  
new Load.load19 Bus1 = 19.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0
new Load.load20 Bus1 = 20.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load21 Bus1 = 21.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load22 Bus1 = 22.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load23 Bus1 = 23.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load24 Bus1 = 24.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load25 Bus1 = 25.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load26 Bus1 = 26.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load27 Bus1 = 27.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load28 Bus1 = 28.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load29 Bus1 = 29.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 
new Load.load30 Bus1 = 30.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0
new Load.load31 Bus1 = 31.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0
new Load.load32 Bus1 = 32.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0
new Load.load33 Bus1 = 33.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0
new Load.load34 Bus1 = 34.1.2.3 Conn = Wye Model = 1 kv = 13.87 kw = 0 kvar = 0 

! TODO input actual given R, and given X
new Line.line1_2 phases = 3 bus1 = 1.1.2.3 bus2 = 2.1.2.3 Length = {distance(1,2)} units = mile
new Line.line2_3 phases = 3 bus1 = 2.1.2.3 bus2 = 3.1.2.3 Length = {distance(2,3)} units = mile
new Line.line3_4 phases = 3 bus1 = 3.1.2.3 bus2 = 4.1.2.3 Length = {distance(3,4)} units = mile
new Line.line4_5 phases = 3 bus1 = 4.1.2.3 bus2 = 5.1.2.3 Length = {distance(4,5)} units = mile
new Line.line4_6 phases = 3 bus1 = 4.1.2.3 bus2 = 6.1.2.3 Length = {distance(4,6)} units = mile
new Line.line6_7 phases = 3 bus1 = 6.1.2.3 bus2 = 7.1.2.3 Length = {distance(6,7)} units = mile
new Line.line7_8 phases = 3 bus1 = 7.1.2.3 bus2 = 8.1.2.3 Length = {distance(7,8)} units = mile
new Line.line8_9 phases = 3 bus1 = 8.1.2.3 bus2 = 9.1.2.3 Length = {distance(8,9)} units = mile
new Line.line9_10 phases = 3 bus1 = 9.1.2.3 bus2 = 10.1.2.3 Length = {distance(9,10)} units = mile
new Line.line10_11 phases = 3 bus1 = 10.1.2.3 bus2 = 11.1.2.3 Length = {distance(10,11)} units = mile
new Line.line11_12 phases = 3 bus1 = 11.1.2.3 bus2 = 12.1.2.3 Length = {distance(11,12)} units = mile
new Line.line9_13 phases = 3 bus1 = 9.1.2.3 bus2 = 13.1.2.3 Length = {distance(9,13)} units = mile
new Line.line13_14 phases = 3 bus1 = 13.1.2.3 bus2 = 14.1.2.3 Length = {distance(13,14)} units = mile
new Line.line13_15 phases = 3 bus1 = 13.1.2.3 bus2 = 15.1.2.3 Length = {distance(13,15)} units = mile
new Line.line15_16 phases = 3 bus1 = 15.1.2.3 bus2 = 16.1.2.3 Length = {distance(15,16)} units = mile
new Line.line16_17 phases = 3 bus1 = 16.1.2.3 bus2 = 17.1.2.3 Length = {distance(16,17)} units = mile
new Line.line17_18 phases = 3 bus1 = 17.1.2.3 bus2 = 18.1.2.3 Length = {distance(17,18)} units = mile
new Line.line17_19 phases = 3 bus1 = 17.1.2.3 bus2 = 19.1.2.3 Length = {distance(17,19)} units = mile
new Line.line19_20 phases = 3 bus1 = 19.1.2.3 bus2 = 20.1.2.3 Length = {distance(19,20)} units = mile
new Line.line20_21 phases = 3 bus1 = 20.1.2.3 bus2 = 21.1.2.3 Length = {distance(20,21)} units = mile
new Line.line21_22 phases = 3 bus1 = 21.1.2.3 bus2 = 22.1.2.3 Length = {distance(21,22)} units = mile
new Line.line20_23 phases = 3 bus1 = 20.1.2.3 bus2 = 23.1.2.3 Length = {distance(20,23)} units = mile
new Line.line23_24 phases = 3 bus1 = 23.1.2.3 bus2 = 24.1.2.3 Length = {distance(23,24)} units = mile
new Line.line23_25 phases = 3 bus1 = 23.1.2.3 bus2 = 25.1.2.3 Length = {distance(23,25)} units = mile
new Line.line25_26 phases = 3 bus1 = 25.1.2.3 bus2 = 26.1.2.3 Length = {distance(25,26)} units = mile
new Line.line26_27 phases = 3 bus1 = 26.1.2.3 bus2 = 27.1.2.3 Length = {distance(26,27)} units = mile
new Line.line27_28 phases = 3 bus1 = 27.1.2.3 bus2 = 28.1.2.3 Length = {distance(27,28)} units = mile
new Line.line28_29 phases = 3 bus1 = 28.1.2.3 bus2 = 29.1.2.3 Length = {distance(28,29)} units = mile
new Line.line25_30 phases = 3 bus1 = 25.1.2.3 bus2 = 30.1.2.3 Length = {distance(25,30)} units = mile
new Line.line30_31 phases = 3 bus1 = 30.1.2.3 bus2 = 31.1.2.3 Length = {distance(30,31)} units = mile
new Line.line31_32 phases = 3 bus1 = 31.1.2.3 bus2 = 32.1.2.3 Length = {distance(31,32)} units = mile
new Line.line31_33 phases = 3 bus1 = 31.1.2.3 bus2 = 33.1.2.3 Length = {distance(31,33)} units = mile
new Line.line33_34 phases = 3 bus1 = 33.1.2.3 bus2 = 34.1.2.3 Length = {distance(33,34)} units = mile

""")
