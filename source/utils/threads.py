import threading
 
class FuncThread(threading.Thread):
    def __init__(self, target, *args, **kwargs):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args, **self._kwargs)
