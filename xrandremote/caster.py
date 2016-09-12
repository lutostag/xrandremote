class Caster(object):
    def __init__(self, screen, remote):
        self.screen = screen
        self.remote = remote
        self.pipe = None

    def stop(self):
        #TODO
        if self.pipe is not None:
            self.pipe

    def start(self):
        #TODO
        pass

    def update_resolution(self, screen):
        self.stop()
        if screen is not None and screen.name == self.screen.name and \
                screen.resolution != self.screen.resolution:
            self.screen.resolution = screen.resolution
            self.start()
