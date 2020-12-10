import time

'''
Timer class
allow us to time the execution of a function
'''
class Timer():
    def __enter__(self):
        self.t1 = time.perf_counter()
        return self
    def __exit__(self, type, value, traceback):
        self.t2 = time.perf_counter()
        self.t = self.t2 - self.t1
        
    def print(self, template: str='{}', r: int=2) -> int:
        print(template.format(round(self.t,r)))
