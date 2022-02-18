class RegexDict:
    def __init__(self):
        self._dict = {}
        self.dot = []
        self.is_dot = False

    def set_dot(self):
        self.is_dot = True

    def set_key(self, *args):

        if len(args) == 2 and not self.is_dot:
            if args[0] in self._dict:
                self._dict[args[0]].append(args[1])
            else:
                self._dict[args[0]] = [args[1]]

        elif self.is_dot and len(args) == 1:
            self.dot.append(args[0])

        else:
            raise ValueError("Cannot set dot parameter without calling set_dot")

    def get(self, key=None):
        if self.is_dot:
            return self.dot
        elif key is not None:
            return self._dict[key]


    def __str__(self):
        return f"Dictionary: {self._dict}, dot {self.dot}"


a = RegexDict()
a.set_key(4, 15)
a.set_key(2, 90)
a.set_key(2, 55)
a.set_dot()
a.set_key(23)
a.set_key(55)
print(a.get(333))
print(a)




