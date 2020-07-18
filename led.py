# Sample implementation using the API representing a simple three state FSM
# The options are On, which prints On, Off, which prints off, and error, 
# which prints error.
from api.statemachine import State, Transition, StateMachine

def main():
    # There is only one input var and no output/defined vars
    # Pressed has 0 for not pressed, 1 for pressed, and -1 for
    # pressed and error
    input_vars = {'pressed' : 0}
    output_vars = dict()
    defined_vars = dict()

    # Define the states
    on_state = State("on", lambda x, y, z: print("on"))
    off_state = State("off", lambda x, y, z: print("off"), initial=True)
    error_state = State("error", lambda x, y, z: print("error"))

    #Define the transitions
    on_state.addTransition(Transition(lambda x, y, z: x['pressed'] == 1, off_state))
    on_state.addTransition(Transition(lambda x, y, z: x['pressed'] == -1, error_state))

    off_state.addTransition(Transition(lambda x, y, z: x['pressed'] == 1, on_state))

    error_state.addTransition(Transition(lambda x, y, z: x['pressed'] == 0, off_state))

    # Define the machine
    states = [on_state, off_state, error_state]

    machine = StateMachine(input_vars, output_vars, defined_vars, states)

    # Now lets test the machine.

    # Tick 4 times without pressing
    for i in range(4):
        machine.tick()

    # Press each time for 4 times
    input_vars['pressed'] = 1

    for i in range(4):
        machine.tick()

    # Tick once more with the press
    machine.tick()

    # Verify we stay in on if not pressed
    input_vars['pressed'] = 0
    for i in range(4):
        machine.tick()

    # Transition to error
    input_vars['pressed'] = -1
    for i in range(4):
        machine.tick()

    # Return to off
    input_vars['pressed'] = 0
    for i in range(4):
        machine.tick()

if __name__ == '__main__':
    main()
