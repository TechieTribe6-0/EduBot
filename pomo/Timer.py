class Timer:
    def __init__(self):
        self.running = False
        self.ticks = 0
        self.max_tiks = 5 #will change to 25*60
    
    def start(self):
        self.runnning = True
        self.ticks = 0

    def stop(self):
        self.running = False

    def get_status(self):
        return self.running

    def get_ticks(self):
        return self.ticks
