
class randomgen(object):
    def __init__(self):
        pass

    def execute(self, mean, variance):
        dim = [900,2]
        data = np.random.normal(loc=mean,scale=variance,size=(dim[0],dim[1]))

        return self.data
