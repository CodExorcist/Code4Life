import sys
import math
from enum import Enum
import collections

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
# To debug: print("Debug messages...", file=sys.stderr, flush=True)

""" 
Game Constant ----------------------------------------------------------------
"""
SAMPLES = "SAMPLES"
DIAGNOSIS = "DIAGNOSIS"
MOLECULES = "MOLECULES"
LABORATORY = "LABORATORY"

class RobotState(Enum):
    START = 0
    SAMPLES = 1
    DIAGNOSIS = 2
    MOLECULE = 3
    LABORATORY = 4

class SubState(Enum):
    NO_SUBSTATE = 0
    UNDIAGNOSED = 1
    TRANSFER = 2

"""
Classes ----------------------------------------------------------------------
"""

class State:

    def __init__(self, c_index=RobotState.START, n_index=RobotState.START, func=lambda: False):
        self.current_state_index = c_index
        self.next_state_index = n_index
        self.action = func
        return    

    def __str__(self):
        return f"Current Index={self.current_state_index}, Next Index={self.next_state_index}"

    def execute(self):
        self.action()


class SampleData:
    
    def __init__(self, _id=-1, carrier=-1, health=0, cost={}):
        self.ID = _id
        self.health = health
        self.cost = cost     
        self.carrier = carrier        

    def __str__(self):
        return f"{self.ID},{self.health},{self.cost},{self.carrier}"

    def __repr__(self):
        return f"SampleData({self.ID},{self.carrier},{self.health},{self.cost})"

    def __eq__(self, other) -> bool:
        return self.ID == other.ID

    def __lt__(self, other):
        return self.health < other.health

    def __gt__(self, other):
        return self.health > other.health

    def is_cloud_data(self)->bool:
        return self.carrier == -1

    def charge_cost(self, cost_id):
        self.cost[cost_id] -= 1
        return


    def total_cost(self)->int:
        return sum(list(self.cost))

    
        
class Robot:
    __next_plausible_sample = None

    def __init__(self, storages={}, sample_datas=[], state=None):
        self.storages = storages
        self.sample_datas = sample_datas
        self.state = state

    # Game Action ---------------------------------------------------------------

    def goto_samples(self)->bool:
        print("GOTO SAMPLES")
        self.goto_next_state()
        return True
    
    def goto_diagnosis(self)->bool:        
        print("GOTO DIAGNOSIS")
        self.goto_next_state()
        return True

    def goto_molecules(self)->bool:
        print("GOTO MOLECULES")
        self.goto_next_state()
        return True

    def goto_laboratory(self)->bool:
        print("GOTO LABORATORY")
        self.goto_next_state()
        return True

    def connect(self, _id):
        print(f"CONNECT {_id}")

    # Status Checking -----------------------------------------------------------

    def is_sample_data_full(self)->bool:
        return len(self.sample_datas) >= 3

    def is_storage_full(self)->bool:
        return sum(self.storages.values()) == 10

    def which_cost_not_fulfill(self, sample)->str:
        for k,v in sample.cost:
            if v > self.storages[k]: return k

        return ""

    def is_sample_fulfill(self, sample):
        for k,v in sample.cost:
            if v > self.storages[k]: return False

        return True

    # Robot Action --------------------------------------------------------------

    # download sample from diagnosis
    def __download_cloud_sample(self, sample_data):
        self.connect(sample_data.ID)
        self.sample_datas += sample_data
        transfer_from_cloud(sample_data)

    # upload sample from diagnosis
    def __upload_sample_to_cloud(self, sample_data):
        self.connect(sample_data.ID)
        self.sample_datas.remove(sample_data)
        transfer_to_cloud(sample_data)

    # hold sample on hand
    def __take_sample(self, sample_data)->bool:
        if self.is_sample_data_full(): 
            return False

        if sample_data.is_cloud_data():
            self.connect(sample_data.ID)
            self.sample_datas.append(sample_data)

        return True 
    
    def __take_molecule(self, _id):
        self.connect(_id)
        self.storages[_id] += 1

    def __produce_medicine(self, sample_id):
        self.connect(sample_id)

    def __remove_molecules_for_sample(self, sample):
        for k,v in sample.cost: self.storages[k] -= v

    def sync_carrying_sample(self, all_samples):
        for self_sample in self.sample_datas: 
            sample = next(filter(lambda a: a == self_sample, all_samples))
            self_sample.carrier = sample.carrier

    def assign_next_plausible_sample(self, sample_data):
        self.__next_plausible_sample = sample_data

    # Robot Main Action --------------------------------------------------------------

    def download_raw_sample_data(self)->bool:
        # Download Rank 3 sample
        if self.is_sample_data_full():
            return False

        self.connect(3)
        return True    

    def take_next_sample(self)->bool:
        return self.__take_sample(self.__next_plausible_sample)

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
    states.append(State(RobotState.START, RobotState.SAMPLES, robot.goto_samples))
    states.append(State(RobotState.SAMPLES, RobotState.SAMPLES, robot.take_next_sample))
    states.append(State(RobotState.SAMPLES, RobotState.DIAGNOSIS, robot.goto_diagnosis))
    states.append(State(RobotState.DIAGNOSIS, RobotState.DIAGNOSIS, robot.take_next_sample))
    states.append(State(RobotState.DIAGNOSIS, RobotState.MOLECULE, robot.goto_molecules))
    states.append(State(RobotState.MOLECULE, RobotState.MOLECULE, robot.take_next_molecule))
    states.append(State(RobotState.MOLECULE, RobotState.LABORATORY, robot.goto_laboratory))
    states.append(State(RobotState.LABORATORY, RobotState.LABORATORY, robot.consume_next_sample))
    states.append(State(RobotState.LABORATORY, RobotState.DIAGNOSIS, robot.goto_diagnosis))
    return

def get_next_state_index(c_index)->RobotState:
    if c_index == RobotState.LABORATORY: return RobotState.DIAGNOSIS
    return RobotState(c_index.value + 1)


def get_next_state(c_index, n_index)->State:
    print(f"c={c_index}, n={n_index}", file=sys.stderr, flush=True)
    state = next(filter(lambda s: s.current_state_index == c_index and 
                                  s.next_state_index == n_index, states))    

    return state

def transfer_to_cloud(sample_data):
    cloud_samples.append(sample_data)

def transfer_from_cloud(sample_data):
    cloud_samples.remove(sample_data)

def find_next_plausible_sample(sample_datas)->SampleData:
    return max([sample for sample in sample_datas if sample.is_cloud_data()])

"""
End Functions ----------------------------------------------------------------------
"""

""" 
Game -----------------------------------------------------------------------------
"""

states = []
cloud_samples = []
storages = { "A":0, "B":0, "C":0, "D":0, "E":0 }

robot = Robot(storages=storages)
initialize_states()
robot.state = states[0]

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
        rank = int(inputs[2])
        expertise_gain = inputs[3] #ignore
        health = int(inputs[4])
        cost_a = int(inputs[5])
        cost_b = int(inputs[6])
        cost_c = int(inputs[7])
        cost_d = int(inputs[8])
        cost_e = int(inputs[9])

        sample = SampleData(sample_id, carried_by, health, 
                            {"A":cost_a, "B":cost_b, "C":cost_c, "D":cost_d, "E":cost_e})
        all_samples.append(sample)

    # print(collections.Counter([s.health for s in all_samples]), file=sys.stderr, flush=True)
    if sample_count > 0: 
        robot.sync_carrying_sample(all_samples)
        n_sample = find_next_plausible_sample(all_samples)
        robot.assign_next_plausible_sample(n_sample)

    while not robot.execute_state(): 
        robot.goto_next_state()
        continue



