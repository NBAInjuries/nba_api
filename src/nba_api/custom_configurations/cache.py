from typing import Union, Dict, Tuple, List, Callable

TupleValueType = Union[int, str, None]
TupleType = Tuple[str, TupleValueType]
ParametersType = List[TupleType]


class CacheEntity:
    def __init__(self):
        self.id = ''
        self.endpoint = ''
        self.parameters = ''
        self.data = {}


class CacheCallbacks:
    def __init__(
            self,
            # data, endpoint, parameters
            create_entity: Callable[[str, ParametersType, dict], CacheEntity],
            # endpoint, parameters
            does_entity_exist: Callable[[str, ParametersType], Union[CacheEntity, None]],
            # cache entity
            is_entity_valid: Callable[[CacheEntity], bool],
            # cache entity, data, parameters
            update_entity: Callable[[CacheEntity, ParametersType, dict], None]
    ):
        self.create_entity = create_entity
        self.does_entity_exist = does_entity_exist
        self.is_entity_valid = is_entity_valid
        self.update_entity = update_entity
