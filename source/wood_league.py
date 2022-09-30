import sys
import math

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

""" 
Game Constant ----------------------------------------------------------------
"""
DIAGNOSIS = "DIAGNOSIS"
MOLECULES = "MOLECULES"
LABORATORY = "LABORATORY"

"""
Classes ----------------------------------------------------------------------
"""

class SampleData:
    
    def __init__(self, _id=-1, carrier=-1, health=0, cost=None):
        self.ID = _id
        self.health = health
        self.cost = cost     
        self.carrier = -1        

    def is_cloud_data(self)->bool:
        return self.carrier == -1
        
class Robot:

    def __init__(self, location=None, storages={}, sample_datas=[]):
        self.location = location
        self.storages = storages
        self.sample_datas = sample_datas

    # Game Action ---------------------------------------------------------------
    
    def goto_diagnosis(self):        
        print("GOTO DIAGNOSIS")

    def goto_molecules(self):
        print("GOTO MOLECULES")

    def goto_laboratory(self):
        print("GOTO LABORATORY")

    def connect(self, _id):
        print(f"CONNECT {_id}")

    # Status Checking -----------------------------------------------------------

    def is_storage_full(self):
        return sum(self.storages.values()) == 10

    def is_sample_fulfill(self, sample):
        fulfill = True

        if sample.cost_a > self.storages["A"]: return False
        elif sample.cost_b > self.storages["B"]: return False
        elif sample.cost_c > self.storages["C"]: return False
        elif sample.cost_d > self.storages["D"]: return False
        elif sample.cost_e > self.storages["E"]: return False

        return True

    # Robot Action --------------------------------------------------------------
    
    def take_sample(self, sample_data)->bool:
        if len(self.sample_datas) >= 3: return False

        if sample_data.is_cloud_data():
            self.connect(sample_data.ID)
            self.sample_datas.append(sample_data)

        return True    

    def take_molecule(self, _id):
        self.connect(_id)
        self.storages[_id] += 1

    def produce_medicine(self, sample_id):
        self.connect(sample_id)

    def remove_molecules_for_sample(self, sample):
        self.storages["A"] -= sample.cost[0]
        self.storages["B"] -= sample.cost[1]
        self.storages["C"] -= sample.cost[2]
        self.storages["D"] -= sample.cost[3]
        self.storages["E"] -= sample.cost[4]

    def consume_all_sample(self):
        for sample in self.sample_datas: 
            if self.is_sample_fulfill(sample):
                self.produce_medicine(sample.ID)
                self.sample_datas.remove(sample)    
                self.remove_molecules_for_sample(sample)
            else:
                return

    def goto_lab_and_produce_all(self):
        if self.location != LABORATORY:
            self.goto_laboratory()

        self.consume_all_sample()

"""
End Classes ----------------------------------------------------------------------
"""

""" 
Game -----------------------------------------------------------------------------
"""

robot = Robot()

project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]


# game loop
while True:
    # game stat for this loop
    for i in range(2):
        inputs = input().split()
        target = inputs[0]
        eta = int(inputs[1]) # ignore
        score = int(inputs[2])
        storage_a = int(inputs[3])
        storage_b = int(inputs[4])
        storage_c = int(inputs[5])
        storage_d = int(inputs[6])
        storage_e = int(inputs[7])
        
        # ignore for wood league
        expertise_a = int(inputs[8])
        expertise_b = int(inputs[9])
        expertise_c = int(inputs[10])
        expertise_d = int(inputs[11])
        expertise_e = int(inputs[12])

    # ignore for wood league
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]

    # sample data
    sample_count = int(input())
    for i in range(sample_count):
        inputs = input().split()
        sample_id = int(inputs[0])
        carried_by = int(inputs[1])
        rank = int(inputs[2]) # ignore
        expertise_gain = inputs[3] #ignore
        health = int(inputs[4])
        cost_a = int(inputs[5])
        cost_b = int(inputs[6])
        cost_c = int(inputs[7])
        cost_d = int(inputs[8])
        cost_e = int(inputs[9])

        sample = SampleData(sample_id, carried_by, health, 
                            (cost_a, cost_b, cost_c, cost_d, cost_e))
        
        while robot.location == DIAGNOSIS:
            if robot.take_sample(sample) == False: break




