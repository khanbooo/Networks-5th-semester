class Packet:
    def __init__(self, program_uuid=None, status=True):
        self.uuid = program_uuid
        self.status = status

    # @property
    # def bytes(self) -> bytes:
    #     return bytes(self)
