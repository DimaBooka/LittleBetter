class RunSpiderError(Exception):
    def __init__(self, arg):
        self.message = arg
        self.show()

    def show(self):
        print("RunSpiderError:" + self.message)
