from time import sleep

class Automations:

    def __init__(self, arduino, camera):
        self.arduino = arduino
        self.camera = camera

    def RTI(self):
        print("RTI scan")
    
    def focus_stack(self):
        print("focus stacking scan")

    def stereo_photography(self):
        print("stereo photography scan")


