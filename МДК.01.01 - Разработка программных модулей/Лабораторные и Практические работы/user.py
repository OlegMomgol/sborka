class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            username=data.get('username')
        )