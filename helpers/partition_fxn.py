from .errors import (
    EmptyItemListError,
    InvalidArgumentError,
    InvalidItemSize,
    ReductionFunctionNotCallableError,
    SizeFunctionNotCallableError
)


class Partitions:
    """
    This is class for generating more general partitions given a list of items.
    It can produce partitions with or without repetition.

    It works as follows. A list of items is provided at construction. Then these items
    are used to partition a given object. The class picks the largest item in the list
    and "subtracts" it from the object. Then it recursively partitions the remaining
    object until either nothing is left or no partition can be applied. It returns
    all the valid partitions.

    The class is meant to work in a more general way, where custom rules can be applied.
    The size function controls how the items behave in the partition. For that we also
    need a reduction function to help us define what "subtract" means.

    For example, if we are partitioning integers, we can use the defaults. However,
    if we are partitioning a string, the reduction function can be one that removes
    a number of starting characters (based on the list of items). The size function will be
    the length function.

    This is incomplete and buggy still. It's also slow for reasonable inputs.
    """
    def __init__(self, items: list, with_repetitions: bool, size_function=None, reduction_function=None):
        self.__validateFunctions(size_function, reduction_function)

        self.size = self.__defaultSizeFunction
        if size_function:
            self.size = size_function

        self.reduce = self.__defaultReductionFunction
        if reduction_function:
            self.reduce = reduction_function

        self.__validateItems(items)
        self.items = items
        self.items.sort(
            key=lambda item: self.size(item),
            reverse=True
        )
        self.length = len(self.items)

        self.with_repetitions = with_repetitions

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

    def __validateFunctions(self, size_function, reduction_function):
        if size_function is not None:
            if not callable(size_function):
                raise SizeFunctionNotCallableError()
            if reduction_function is None:
                raise InvalidArgumentError('Reduction function provided but no Size function provided.')

        if reduction_function is not None:
            if not callable(reduction_function):
                raise ReductionFunctionNotCallableError()
            if size_function is None:
                raise InvalidArgumentError('Size function provided but no Reduction function provided.')

    def __validateItems(self, items):
        if len(items) == 0:
            raise EmptyItemListError("Provided item list is empty.")

        for item in items:
            if self.size(item) <= 0:
                raise InvalidItemSize(f"The size of item {item} is {self.size(item)}. The provided size must be positive.")

    def __defaultSizeFunction(self, item):
        return item
    
    def __defaultReductionFunction(self, obj, item):
        return item, obj - item
