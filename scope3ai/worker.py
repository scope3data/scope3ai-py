import logging
import queue
import threading
from time import sleep
from typing import Callable, Optional

from time import monotonic

logger = logging.getLogger("scope3ai.worker")


class BackgroundWorker:
    STOP_WORKER = object()

    def __init__(self, size: int) -> None:
        self._queue = queue.Queue(maxsize=size)
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    @property
    def is_alive(self) -> bool:
        return self._thread and self._thread.is_alive()

    def _ensure_thread(self) -> None:
        if not self.is_alive:
            self.start()

    def submit(self, callback: Callable[[], None]) -> bool:
        self._ensure_thread()
        try:
            self._queue.put_nowait(callback)
            return True
        except queue.Full:
            return False

    def start(self) -> None:
        with self._lock:
            if self.is_alive:
                return
            logger.debug("Starting background worker")
            self._thread = threading.Thread(
                target=self._run,
                name="scope3ai.BackgroundWorker",
                daemon=True,
            )
            try:
                self._thread.start()
            except RuntimeError:
                self._thread = None

    def kill(self) -> None:
        logger.debug("Got kill signal")
        with self._lock:
            if not self._thread:
                return
            try:
                self._queue.put_nowait(self.STOP_WORKER)
            except queue.Full:
                logger.debug("Failed to kill worker")
            except queue.ShutDown:
                logger.debug("Worker already shutdown")
            self._thread = None

    def flush(self, timeout: float = 5) -> None:
        logger.debug("Got flush signal")
        with self._lock:
            if not self.is_alive:
                return
            self._wait_flush(timeout)
        logger.debug("Worker flushed")

    def _wait_flush(self, timeout: float) -> None:
        initial_timeout = min(0.1, timeout)
        if not self._timed_queue_join(initial_timeout):
            pending = self._queue.qsize() + 1
            logger.debug(f"{pending} event(s) pending on flush")

            if not self._timed_queue_join(timeout - initial_timeout):
                pending = self._queue.qsize() + 1
                logger.error(f"flush timed out, dropped {pending} events")

    def _timed_queue_join(self, timeout: float) -> bool:
        deadline = monotonic() + timeout
        queue = self._queue

        queue.all_tasks_done.acquire()

        try:
            while queue.unfinished_tasks:
                delay = deadline - monotonic()
                if delay <= 0:
                    return False
                queue.all_tasks_done.wait(timeout=delay)

            return True
        finally:
            queue.all_tasks_done.release()

    def _run(self) -> None:
        while True:
            callback = self._queue.get()
            try:
                if callback is self.STOP_WORKER:
                    break
                try:
                    callback()
                except Exception:
                    logger.error("Failed processing job", exc_info=True)
            finally:
                self._queue.task_done()
            sleep(0)
