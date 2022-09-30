import sys
import math
from enum import Enum

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

""" 
Game Constant ----------------------------------------------------------------
"""
DIAGNOSIS = "DIAGNOSIS"
MOLECULES = "MOLECULES"
LABORATORY = "LABORATORY"

class RobotState(Enum):
    START = 0
    DIAGNOSIS = 1
    MOLECULE = 2
    LABORATORY = 3

"""
Classes ----------------------------------------------------------------------
"""

class State:

    def __init__(self, c_index=RobotState.START, n_index=RobotState.START, func=lambda: False):
        self.current_state_index = c_index
        self.next_state_index = n_index
        self.action = func
        return    

    def execute(self):
        self.action()


class SampleData:
    
    def __init__(self, _id=-1, carrier=-1, health=0, cost=None):
        self.ID = _id
        self.health = health
        self.cost = cost     
        self.carrier = -1        

    def is_cloud_data(self)->bool:
        return self.carrier == -1
        
class Robot:

    def __init__(self, location=None, storages={}, sample_datas=[], state=None):
        self.location = location
        self.storages = storages
        self.sample_datas = sample_datas
        self.state = state

    # Game Action ---------------------------------------------------------------
    
    def goto_diagnosis(self)->bool:        
        print("GOTO DIAGNOSIS")
        return False

    def goto_molecules(self)->bool:
        print("GOTO MOLECULES")
        return False

    def goto_laboratory(self)->bool:
        print("GOTO LABORATORY")
        return False

    def connect(self, _id):
        print(f"CONNECT {_id}")

    # Status Checking -----------------------------------------------------------

    def is_sample_data_full(self)->bool:
        return len(self.sample_datas) >= 3

    def is_storage_full(self)->bool:
        return sum(self.storages.values()) == 10

    def which_cost_not_fulfill(self, sample)->str:
        if sample.cost_a > self.storages["A"]: return "A"
        elif sample.cost_b > self.storages["B"]: return "B"
        elif sample.cost_c > self.storages["C"]: return "C"
        elif sample.cost_d > self.storages["D"]: return "D"
        elif sample.cost_ed > self.storages["E"]: return "E"
        else: return ""


    def is_sample_fulfill(self, sample):

        if sample.cost_a > self.storages["A"]: return False
        elif sample.cost_b > self.storages["B"]: return False
        elif sample.cost_c > self.storages["C"]: return False
        elif sample.cost_d > self.storages["D"]: return False
        elif sample.cost_e > self.storages["E"]: return False

        return True

    # Robot Action --------------------------------------------------------------
    
    def __take_molecule(self, _id):
        self.connect(_id)
        self.storages[_id] += 1

    def __produce_medicine(self, sample_id):
        self.connect(sample_id)

    def __remove_molecules_for_sample(self, sample):
        self.storages["A"] -= sample.cost[0]
        self.storages["B"] -= sample.cost[1]
        self.storages["C"] -= sample.cost[2]
        self.storages["D"] -= sample.cost[3]
        self.storages["E"] -= sample.cost[4]

    # Robot Main Action --------------------------------------------------------------

    def take_sample(self, sample_data)->bool:
        if self.is_sample_data_full(): 
            return False

        if sample_data.is_cloud_data():
            self.connect(sample_data.ID)
            self.sample_datas.append(sample_data)        

        return True    

    def consume_next_sample(self)->bool:
        for sample in self.sample_datas: 
            if self.is_sample_fulfill(sample):
                self.__produce_medicine(sample.ID)
                self.sample_datas.remove(sample)    
                self.__remove_molecules_for_sample(sample)
                return True

        return False

    def take_next_molecule(self)->bool:    
        if self.is_storage_full():
            return False

        for sample in self.sample_datas:
            if not self.is_sample_fulfill(sample):
                cost = self.which_cost_not_fulfill(sample)
                self.__take_molecule(cost)
                return True
            else: 
                continue

        return False

    # Robot State --------------------------------------------------------------

    def update_state(self, next_state_index):
        c_index = self.state.next_state_index
        self.state = get_next_state(c_index, next_state_index)
        return

    def goto_next_state(self):
        self.update_state(get_next_state_index(self.state.current_state_index))
        return

    def execute_state(self)->bool:
        return self.state.action()

"""
End Classes ----------------------------------------------------------------------
"""

"""
Functions ----------------------------------------------------------------------
"""

def initialize_states():
    states.append(State(RobotState.START, RobotState.DIAGNOSIS, robot.goto_diagnosis))
    states.append(State(RobotState.DIAGNOSIS, RobotState.DIAGNOSIS, robot.take_next_molecule))
    states.append(State(RobotState.DIAGNOSIS, RobotState.MOLECULE, robot.goto_molecules))
    states.append(State(RobotState.MOLECULE, RobotState.MOLECULE, robot.take_next_molecule))
    states.append(State(RobotState.MOLECULE, RobotState.LABORATORY, robot.goto_laboratory))
    states.append(State(RobotState.LABORATORY, RobotState.LABORATORY, robot.consume_next_sample))
    states.append(State(RobotState.LABORATORY, RobotState.LABORATORY), robot.goto_diagnosis)
    return

def get_next_state_index(c_index)->RobotState:
    if c_index == RobotState.LABORATORY: return RobotState.DIAGNOSIS
    
    return c_index + 1


def get_next_state(c_index, n_index)->State:
    state = next(filter(lambda s: s.current_state_index == c_index and 
                                  s.next_state_index == n_index, states))    
    return state


"""
End Functions ----------------------------------------------------------------------
"""

""" 
Game -----------------------------------------------------------------------------
"""

states = []
robot = Robot()

project_count = int(input())
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]


# game loop
while True:
    all_samples = []

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
        all_samples.append(sample)
    
    while not robot.execute_state(): 
        robot.goto_next_state()
        continue


