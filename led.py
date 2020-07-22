# Sample implementation using the API representing a simple three state FSM
# The options are On, which prints On, Off, which prints off, and error, 
# which prints error.
from api.statemachine import State, Transition, StateMachine

def main():
    # Dictionary mapping function names to entire functions
    # as strings. This section should be replaced by a parser
    # that generates this mapping for user defined functions
    function_dict = dict()
    # Maps function name to entire function as a string
    function_dict["on_action"] = \
    """
    def on_action():
        print("on")
    """
    function_dict["off_action"] = \
    """
    def off_action():
        print("off")
    """
    function_dict["error_action"] = \
    """
    def error_action():
        print("error")
    """
    function_dict["is_pressed"] = \
    """
    def is_pressed():
        return pressed == 1
    """
    function_dict["is_pressed_error"] = \
    """
    def is_pressed_error():
        return pressed == -1
    """

    # There is only one input var and no output/defined vars
    # Pressed has 0 for not pressed, 1 for pressed, and -1 for
    # pressed and error
    input_vars = {'pressed' : 0}
    output_vars = dict()
    defined_vars = dict()

    # Define the states
    on_state = State("on", "on_action")
    off_state = State("off", "off_action", initial=True)
    error_state = State("error", "error_action")

    #Define the transitions
    on_state.addTransition(Transition("is_pressed", off_state))
    on_state.addTransition(Transition("is_pressed_error", error_state))

    off_state.addTransition(Transition("is_pressed", on_state))

    error_state.addTransition(Transition("is_pressed", off_state))

    # Define the machine
    states = [on_state, off_state, error_state]

    machine = StateMachine(input_vars, output_vars, defined_vars, states, function_dict, "example.py")


if __name__ == '__main__':
    main()
