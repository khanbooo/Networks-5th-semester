import threading


class StoppableThread(threading.Thread):
    def __init__(self, target=None):
        super(StoppableThread, self).__init__(target=target)
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    @property
    def stopped(self) -> threading.Event():
        return self._stop_event.is_set()

    def close(self) -> None:
        self.stop()