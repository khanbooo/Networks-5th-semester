import enum


@enum.unique
class DialogueStatuses(enum.IntEnum):
    MAIN_PAGE = 1
    CHOOSING_LOCATION = 2
    CHOOSING_PLACE = 3
