class EmptyItemListError(Exception):
    pass

class SizeFunctionNotCallableError(Exception):
    pass

class ReductionFunctionNotCallableError(Exception):
    pass

class InvalidItemSize(Exception):
    pass

class Partitions:
    def __init__(self, items: list, with_repetitions: bool, size_function=None, reduction_function=None):
        self.items = items
        self.length = len(items)
        self.with_repetitions = with_repetitions
        self.size = size_function
        self.reduce = reduction_function
        
        self._initialize()

    def partitions(self, obj, start_index=0, printout=True):
        if printout:
            print(f'\nPartitioning {obj} into parts from {self.items}:\n')
        if start_index >= self.length:
            return []

        size = self.size(obj)

        parts = []
        if self.with_repetitions:
            offset = 0
        else:
            offset = 1

        for index, item in enumerate(self.items[start_index:]):
            if self.size(item) > size:
                continue

            head, tail = self.reduce(obj, item)
            if self.size(tail) == 0:
                parts.append([head])
                continue

            sub_parts = self.partitions(tail, start_index + index + offset, printout=False)
            for part in sub_parts:
                parts.append([head, *part])
        if printout:
            print(f"Found {len(parts)} partitions of {obj}!\n")
        return parts

    def _initialize(self):
        if len(self.items) == 0:
            raise EmptyItemListError("Provided item list is empty.")

        if self.size is None:
            self.size = self.__default_size
        if not callable(self.size):
            raise SizeFunctionNotCallableError("The provided size function is not a function.")

        if self.reduce is None:
            self.reduce = self.__default_reduce
        if not callable(self.reduce):
            raise ReductionFunctionNotCallableError("The provided reduction function is not a function.")

        for item in self.items:
            if self.size(item) <= 0:
                raise InvalidItemSize(f"The size of item {item} is {self.size(item)}. Size needs to be greater than 0")

        self._prepare_items()

    def __default_size(self, item):
        return item
    
    def __default_reduce(self, obj, item):
        return item, obj - item
    
    def _prepare_items(self):
        self.items.sort(
            key=lambda item: self.size(item),
            reverse=True
        )
