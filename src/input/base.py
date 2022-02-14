from math import inf
from collections import deque
import re
from typing import Callable, Deque, Generic, Iterable, Optional, Type, TypeVar, List, Mapping, Set, Any, Union

from pyrsistent import T


class Input(Generic[T]):
    value: Optional[T]
    listeners: List[Callable[['Input']]]

    def __init__(self):
        self.value = None
        self.listeners = []

    def push(self, value: T):
        self.value = value
        [h(self) for h in self.listeners]
        return self


    def listen(self, handler: Callable[['Input']]):
        self.listeners.append(handler)
    
    def actualize(self):
        return self

    def copy(self):
        copy = self.__class__()
        # /!\ @todo value could be a mutable
        copy.value = self.value
        copy.listeners = list(self.listeners)


    @property
    def value(self) -> T:
        return self.value

    @classmethod
    def define(cls, **options) -> Type['Input'[T]]:
        return cls



class BufferedInput(Generic[T]):
    queue: Deque[Union[T, None]]
    listeners: List[Callable[['Input']]]

    def __init__(self, max_size: int = None):
        self.queue = deque(maxlen=max_size)
        self.listeners = []
    
    def push(self, value: T = None) -> 'BufferedInput':
        self.queue.appendleft(value)
        return self

    def pop(self) -> T:
        return self.queue.pop()
    
    def actualize(self):
        if len(self.queue) > 1:
            self.queue.pop()
        return self
    
    def listen(self, handler: Callable[['Input']]):
        self.listeners.append(handler)
    
    def copy(self):
        copy = self.__class__()
        copy.queue = self.queue.copy()
        copy.listeners = list(self.listeners)
        return copy

    @property
    def value(self) -> T:
        length: int = len(self.queue)
        return self.queue[length - 1]
 
    @classmethod
    def define(cls, **options) -> Type['BufferedInput'[T]]:
        return cls