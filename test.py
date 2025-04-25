class Baz:
    def __init__(self, x: int) -> None:
        self.x = x

    def __eq__(self, other):
        if not isinstance(other, Baz):
            return False
        return self.x == other.x

    def __hash__(self):
        return hash(self.x)


st = set()
st.add(Baz(1))

print(Baz(1) in st)
