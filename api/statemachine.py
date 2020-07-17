from typing import Callable, Iterable, Mapping

#forward declare
class State:
    def __init__(self):
        pass

# Class holding the information for the overall state machine
class StateMachine:
    
    def __init__(self, input_vars: Mapping[str, int], output_vars: Mapping[str, int],
            states: Iterable[State]):
        # Check uniqueness across variable names
        input_vars_set = set(input_vars.key())
        output_vars_set = set(output_vars.key())
        total_set = input_vars_set.union(output_vars_set)
        if len(total_set) != len(input_vars_set) + len(output_vars_set):
            raise KeyError("Variable name shared between input and output variables")
        self._input_vars = input_vars
        self._output_vars = output_vars
        # Check all of the states for uniqueness
        for state in states:
            # TODO: Add a check to ensure there is exactly one starting state
            # TODO: Check uniqueness by name
            pass

        # TODO: Add a starting state and current state (possibly redundant)

    def tick(self):
        # TODO implement once state is properly defined
        # Calls the action function of the state
        # Checks transitions
        # Updates the current state
        pass

    def getOutputVar(self, var_name: str):
        return self._output_vars[var_name]

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

    def __init__(self, name: str, action_func: Callable [[], None]):
        self._name = name
        self._transitions = []
        self._action_func = action_func

    def getName(self) -> str:
        return self._name

    def addTransition(self, transition: Transition):
        self._transitions.append(transition)

    def getTransitions(self) -> Iterable[Transition]:
        return self._transitions

    def action(self):
        self._action_func()
