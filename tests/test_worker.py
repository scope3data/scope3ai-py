def test_background_worker():
    from scope3ai.worker import BackgroundWorker
    from threading import Event

    worker = BackgroundWorker(10)
    event = Event()

    def task():
        event.set()

    assert worker.submit(task) is True
    assert event.wait(timeout=2) is True


def test_background_worker_multiple():
    from scope3ai.worker import BackgroundWorker
    from threading import Event

    worker = BackgroundWorker(10)
    event1 = Event()
    event2 = Event()

    def task1():
        event1.set()

    def task2():
        event2.set()

    worker.submit(task1)
    worker.submit(task2)
    assert event1.wait(timeout=2) is True
    assert event2.wait(timeout=2) is True


def test_background_worker_with_task_exception():
    from scope3ai.worker import BackgroundWorker
    from threading import Event

    worker = BackgroundWorker(10)
    event = Event()

    def task():
        raise Exception("Task exception")

    def task2():
        event.set()

    assert worker.submit(task) is True
    assert worker.submit(task2) is True
    assert event.wait(timeout=2) is True


def test_background_worker_limit():
    from scope3ai.worker import BackgroundWorker

    worker = BackgroundWorker(1)
    worker.pause()

    def task():
        pass

    assert worker.submit(task) is True
    assert worker.submit(task) is False


def test_background_worker_kill():
    from scope3ai.worker import BackgroundWorker
    import threading

    worker = BackgroundWorker(10)
    thread1 = thread2 = None
    event1 = threading.Event()
    event2 = threading.Event()

    def task1():
        nonlocal thread1
        thread1 = threading.get_ident()
        event1.set()

    def task2():
        nonlocal thread2
        thread2 = threading.get_ident()
        event2.set()

    assert worker.submit(task1) is True
    worker.kill()
    assert worker.submit(task2) is True
    assert event1.wait(timeout=2) is True
    assert event2.wait(timeout=2) is True
    assert thread1 != thread2


def test_background_worker_kill_twice():
    from scope3ai.worker import BackgroundWorker

    worker = BackgroundWorker(10)

    def task():
        pass

    assert worker.submit(task) is True
    worker.kill()
    worker.kill()


def test_background_worker_flush():
    from scope3ai.worker import BackgroundWorker
    from threading import Event
    import time

    worker = BackgroundWorker(10)
    event = Event()

    def task():
        time.sleep(1)
        event.set()

    assert worker.submit(task) is True
    worker.flush()

    # normally because flush is already waiting, event should be set
    assert event.is_set() is True


def test_background_worker_pause_resume():
    from scope3ai.worker import BackgroundWorker
    from threading import Event

    worker = BackgroundWorker(10)
    event_run = Event()
    event = Event()

    def task_wait_run():
        event_run.set()

    def task():
        event.set()

    worker.submit(task_wait_run)
    assert event_run.wait(timeout=2) is True
    worker.pause()
    worker.submit(task)
    assert event.wait(timeout=1) is False
    assert event.is_set() is False
    worker.resume()
    assert event.wait(timeout=2) is True
