# fsm-generator
A code base for automatically generating state machines aimed at usability and eventually integrating formal verification.

## Design Considerations and Ideas
We probably need to start with basic design plans. It seems like there are a few main issues we may want to start with (or decide to ignore til later). So far I think we need to consider:

  1. Frontend Representation
  2. Module Division/Points of Separation
  3. Conventions and Semantics Used
  4. Backend languages
  5. Development Plan

### Frontend Representation

While this probably classifies as just another module, I think this is by far the most important feature to consider. 
If you want anyone to try and use this there needs to be a clear and preferrably effortless path through which one translates the FSM drawing into a code layout.
This naturally suggests using a visual representation of the chart, which I think is probably the correct thought process. However, my experience using Yakindu is that have a GUI
interface for manually constructing code is very clunky. Instead I would suggest a more programmer friendly interface where one can both generate a visual output of their FSM and construct
code in a traditional manner. One idea I have is that all the actual code generate could be done in an example programming langauge, like a python file, and then use language annotations
to construct a visual representation of the FSM. Alternatively, rather than placing all the FSM construction contents in the scripting language file, the process could be semi-interactive.
One could generate all of the state transition functions, variables, and state initialization information in the scripting language file, and then use an interactive gui to combine the
information.

### Module Divisions

As we design our layout I think its important to understand what our modules might be (and potentially why). Here are some example modules I was thinking we could eventually have:
  * Frontend Visual (representing the graph)
  * Frontend Code Parsing (if we want to parse any scripting file contents)
  * FSM translation (converting the frontend representation to a native FSM)
  * Backend Code Generation IR (Module for an IR for eventually converting the FSM to some target code generation)
  * Backend Code Generation Output (Module for converting the IR to C, Java, C++, etc. Probably best to start with one langauge but the IR gives flexibility).
  * Optimizations (Any possible aims at generating more efficient code or FSMs).
  * Formal Verification (Any code that aims to prove code details from the FSM structure).

I think clearly we don't want to start implementing all of these modules and thes module definitions may not make sense. For example, it may make the most sense to just define an IR that natively
describes an FSM so you don't need to translate the frontend into an FSM in another langauge. In addition, some modules, like optimizations and formal verification probably don't make any sense
to even consider until far later in the process.

### Conventions and Semantics Used

I really don't think this important right now and that we should just start with the simplest FSMs first. However we may need to decide things like default transitions from the start.

### Backend Languages

I don't have any preference yet but we should probably decide what language(s) we want to use to get started. It might make more sense what to use where once its clear how we want to design this.

### Development Plan

I think the best plan is to start with a simplest FSM. First design the code for "creating" an FSM, possibly without a code visualization technique. Then we should undergo a translation, convert
it to a simple IR, and finally produce a C backend (as that is probably the easiest to do). 
