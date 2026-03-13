class Note:
    def __init__(self, id, title, content, category_id, user_id, created_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.category_id = category_id
        self.user_id = user_id
        self.created_at = created_at

    def __repr__(self):
        return f"Note(id={self.id}, title='{self.title}')"

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            content=data.get('content'),
            category_id=data.get('category_id'),
            user_id=data.get('user_id'),
            created_at=data.get('created_at')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'created_at': self.created_at
        }