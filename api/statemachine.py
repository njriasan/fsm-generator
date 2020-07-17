from typing import Callable, Iterable, Mapping

#forward declare of State to trick the typing module
class State:
    def __init__(self):
        pass

# Class holding the information for the overall state machine
class StateMachine:
    
    def __init__(self, input_vars: Mapping[str, int], output_vars: Mapping[str, int],
            states: List[State]):
        # No need to store the list of states but we will just in case
        # compiling becomes easier/for debugging
        self._states = states

        # Check uniqueness across variable names
        input_vars_set = set(input_vars.key())
        output_vars_set = set(output_vars.key())
        total_set = input_vars_set.union(output_vars_set)
        if len(total_set) != len(input_vars_set) + len(output_vars_set):
            raise RuntimeError("Error: Variable name shared between input and output variables.")
        self._input_vars = input_vars
        self._output_vars = output_vars
        # Check all of the states for uniqueness
        names_set = set()
        initial_counter = 0
        for state in states:
            names_set.append(state.getName())
            is_initial = state.isInitial()
            if is_initial:
                initial_counter += 1
                # Add a current and starting state. The starting state might
                # be redundnant
                self._start_state = state
                self._curr_state = state
        # Check that there are no duplicate names
        if len(names_set) != len(states):
            raise RuntimeError("Error: Not all states provided have a unique name.")
        # Check that there is exactly 1 start state
        if initial_counter > 1:
            raise RuntimeError("Error: Multiple start states provided.")
        elif initial_counter == 0:
            raise RuntimeError("Error: No start state provided.")

    def tick(self):
        # TODO: Figure out how to include the input/output
        # vars as available in each function        
        state = getCurrState()

        # Calls the action function of the state
        state.action()

        # Checks transitions
        for transition in state.getTransitions():
            if transition.checkCondition():
                # Updates the current state
                self._curr_state = self.getNextState()
                break

    def getOutputVar(self, var_name: str):
        return self._output_vars[var_name]

    def getStartState(self) -> State:
        return self._start_state

    def getCurrState(self) -> State:
        return self._curr_state

    def getStates(self) -> List[State]:
        return self._states

# Class holding the information for a particular transition
class Transition:
    
    def __init__(self, cond_func: Callable [[], bool], next_state: State):
        self._cond_func = cond_func
        self._next_state = next_state

    def checkCondition(self) -> bool:
        return self._cond_func()

    def getNextState(self) -> State:
        return self._next_state

# Class holding the information about a particular state
class State:

    def __init__(self, name: str, action_func: Callable [[], None], initial=False: bool):
        self._name = name
        self._transitions = []
        self._action_func = action_func
        self._initial = initial

    def getName(self) -> str:
        return self._name

    def addTransition(self, transition: Transition):
        self._transitions.append(transition)

    def getTransitions(self) -> List[Transition]:
        return self._transitions

    def action(self):
        self._action_func()

    def isInitial(self) -> bool:
        return self._initial
