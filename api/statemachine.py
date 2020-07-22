from typing import Callable, List, Mapping

def print_indent(f_stream, indent:int):
    space_str = " " * indent
    print("{}".format(space_str), file=f_stream, end='')

#forward declare of State to trick the typing module
class State:
    def __init__(self):
        pass

# Class holding the information for the overall state machine
class StateMachine:
    
    def __init__(self, input_vars: Mapping[str, int], output_vars: Mapping[str, int], 
            defined_vars: Mapping[str, int], states: List[State], function_dict: Mapping[str, str], filename: str):
       
        # Store a dictionary of functions
        self._function_dict = function_dict

        # Store the list of state
        self._states = states

        # Check uniqueness across variable names
        input_vars_set = set(input_vars.keys())
        output_vars_set = set(output_vars.keys())
        defined_vars_set = set(defined_vars.keys())
        total_set = input_vars_set.union(output_vars_set).union(defined_vars_set)
        if len(total_set) != len(input_vars_set) + len(output_vars_set) + len(defined_vars):
            raise RuntimeError("Error: Variable name shared between input, output, and defined variables.")
        self._input_vars = input_vars
        self._output_vars = output_vars
        self._defined_vars = defined_vars
        # Check all of the states for uniqueness
        names_set = set()
        initial_counter = 0
        for i, state in enumerate(states):
            state.setEnum(i)
            names_set.add(state.getName())
            is_initial = state.isInitial()
            if is_initial:
                initial_counter += 1
                # Add the start state
                self._start_state = state
        # Check that there are no duplicate names
        if len(names_set) != len(states):
            raise RuntimeError("Error: Not all states provided have a unique name.")
        # Check that there is exactly 1 start state
        if initial_counter > 1:
            raise RuntimeError("Error: Multiple start states provided.")
        elif initial_counter == 0:
            raise RuntimeError("Error: No start state provided.")

        with open(filename, "w") as f:
            self.generateCode(f, 0)

    def generateCode(self, f_stream, indent: int):
        # Start with the assumption you create input, output, and defined vars
        total_vars = [self._input_vars, self._output_vars, self._defined_vars]

        # First, generate input, output, and defined vars as global variables
        for var_dict in total_vars:
            for key, value in var_dict.items():
                print_indent(f_stream, indent)
                print("{} = {}".format(key, value), file=f_stream)

        # Second, define our run_statemachine function + create a state variable.
        print_indent(f_stream, indent)
        # REPLACE HARDCODED NAME HERE
        print("def run_statemachine():", file=f_stream)
        indent += 4

        # Initialize the state variable to the intiial state
        print_indent(f_stream, indent)
        # REPLACE HARDCODED NAME HERE
        print("curr_state = {}".format(self._start_state.getEnum()), file=f_stream)

        # Iterate through each state and call generateCode
        for i, state in enumerate(self._states):
            if i == 0:
                cond_str = "if"
            else:
                cond_str = "elif"
            print_indent(f_stream, indent)
            # REPLACE HARDCODED NAME HERE
            print("{} curr_state == {}:".format(cond_str, state.getEnum()), file=f_stream)
            state.generateCode(f_stream, indent + 4)
        indent -= 4
        print_indent(f_stream, indent)
        print("", file=f_stream)
        # Include each user defined function
        for function_str in self._function_dict.values():
            lines = function_str.strip().split("/n")
            for line in lines:
                print_indent(f_stream, indent)
                print(line, file=f_stream)
            print_indent(f_stream, indent)
            print("", file=f_stream)
                 

    def getOutputVar(self, var_name: str):
        return self._output_vars[var_name]

    def getStartState(self) -> State:
        return self._start_state

    def getStates(self) -> List[State]:
        return self._states

# Class holding the information for a particular transition
class Transition:
    
    def __init__(self, cond_func: str, next_state: State):
        self._cond_func = cond_func
        self._next_state = next_state

    def getCondition(self):
        return self._cond_func

    def getNextState(self) -> State:
        return self._next_state


# Class holding the information about a particular state
class State:

    def __init__(self, name: str, action_func: str, initial: bool = False):
        self._name = name
        self._transitions = []
        self._action_func = action_func
        self._initial = initial

    def setEnum(self, index: int):
        self._index = index

    def getEnum(self) -> int:
        return self._index

    def getName(self) -> str:
        return self._name

    def addTransition(self, transition: Transition):
        self._transitions.append(transition)

    def getTransitions(self) -> List[Transition]:
        return self._transitions

    def isInitial(self) -> bool:
        return self._initial

    def generateCode(self, f_stream, indent: int):
        # 1. Generate a call to the action function
        print_indent(f_stream, indent)
        print("{}()".format(self._action_func), file=f_stream)
        # 2. For each transition, call generateCode
        for i, transition in enumerate(self._transitions):
            if i == 0:
                cond_str = "if"
            else:
                cond_str = "elif"
            print_indent(f_stream, indent)
            # ADD CALL to cond function
            print("{} {}():".format(cond_str, transition.getCondition()), file=f_stream)
            print_indent(f_stream, indent + 4)
            print("curr_state = {}".format(transition.getNextState().getEnum()), file=f_stream)
