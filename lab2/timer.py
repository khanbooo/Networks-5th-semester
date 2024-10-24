import threading
import time
from stoppable import StoppableThread


class TimeCounterThread(StoppableThread):
    def __init__(self, interval: float, file_size=None):
        super().__init__()
        self.file_size = file_size

        self.interval = interval
        self._lock = threading.Lock()

        self.first_ns = None
        self.total_bytes_recv = 0

        self.since_last_log = 0

    def run(self):
        while not self._stop_event.wait(self.interval):
            print(123123123)
            self.log()
        self.log(total=True)

    def update(self, ns: int, bytes_recv: int):
        self._lock.acquire()

        self.since_last_log += bytes_recv
        self.total_bytes_recv += bytes_recv
        if self.first_ns is None:
            self.first_ns = ns

        self._lock.release()

    def log(self, total=False):
        self._lock.acquire()
        if self.first_ns is None:
            return
        first_ns, total_bytes_recv, since_last_log = self.first_ns, self.total_bytes_recv, self.since_last_log
        self._lock.release()

        current_ns = time.time_ns()
        average = total_bytes_recv * 1e9 / max(1, (current_ns - first_ns))
        cur = since_last_log / self.interval
        self._lock.acquire()
        self.since_last_log = 0
        self._lock.release()

        msg = f"average speed: {average:.2f} bytes/sec"
        if not total:
            msg = f"current speed: {cur:.2f} bytes/sec | " + msg
            if self.file_size is not None and self.file_size > 0:
                msg = msg + f" | progress: {100 * total_bytes_recv / self.file_size:.2f}%"

        print(msg)


