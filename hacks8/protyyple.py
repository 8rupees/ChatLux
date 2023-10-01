class token:
    def __init__(self, usrID, amount, has):
        self.usrID = usrID
        self.amount = amount
        self.has = has

    def update(self):
        return [self.usrID, self.amount, self.has]

data = {}

recv = token("8rupees", 1000, "8cb27d335d1da626ceb10a6b51ed8249247c00308ba28694ed4f3a5911a7b3d9")

for i in range(1, 4):
    data.update({str(1): recv.update()})

print(data)
