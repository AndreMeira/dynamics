from typing import Any, Callable, Iterable, List, Mapping, Set, TypeVar
from . import Input, BufferedInput


InputType = TypeVar('InputType', Input, BufferedInput)
class InputSynchronizer:
    input_names: List[str]
    inputs: Set[InputType]
    ready: Set[InputType]
    handler: Callable[[Iterable[Input]], Any]

    def __init__(self, handler: Callable, inputs: Mapping[str, InputType] = {}):
        self.ready = set()
        self.input_names = {k for k in inputs.keys()}
        self.inputs = {i.push(None) for i in inputs.values()}


    def handle_input_change(self, input: InputType) -> None:
        self.ready.add(input)
        if self.ready == self.inputs:
            self.ready.clear()
            self.inputs = {i.actualize() for i in self.inputs}
            args = zip(self.input_names, self.inputs)
            self.handler(**{k: i.value for k, i in args})
            
            
    
       