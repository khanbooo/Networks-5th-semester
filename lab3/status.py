from dialogueStatuses import DialogueStatuses


class Status:
    def __init__(self):
        self.__status = DialogueStatuses.MAIN_PAGE

    def set_status(self,
                   status: DialogueStatuses = DialogueStatuses.MAIN_PAGE
                   ):
        self.__status = status

    @property
    def get_status(self):
        return self.__status

    @property
    def get_upper_status(self):
        return max(self.__status - 1, DialogueStatuses.MAIN_PAGE)

    @property
    def is_main_page(self):
        return self.__status == DialogueStatuses.MAIN_PAGE

    @property
    def is_choosing_location(self):
        return self.__status == DialogueStatuses.CHOOSING_LOCATION

    @property
    def is_choosing_place(self):
        return self.__status == DialogueStatuses.CHOOSING_PLACE
