class DocumentBasedEntry:
    def __init__(self):
        pass

    def to_json(self):
        pass

class SourceEntry(DocumentBasedEntry):
    def __init__(self, source_name, source_pwd, previous_pwd=None):
        super().__init__()
        self.source_name = source_name
        self.source_pwd = source_pwd
        self.previous_pwd = previous_pwd

    def to_json(self):
        return {
            'source_name' : self.source_name,
            'source_pwd' : self.source_pwd,
            'previous_pwd' : self.previous_pwd if self.source_pwd else None
        }

    def __str__(self) -> str:
        return f'{self.source_name} - {self.source_pwd}'

class PasswordGetEntry(DocumentBasedEntry):
    def __init__(self, username, sources):
        super().__init__()
        self.username = username
        self.sources = sources

    def to_json(self):
        return {
            'username' : self.username,
            'sources': [source.to_json() for source in self.sources]
        }

    def __str__(self) -> str:
        return f'{self.username} - {self.sources}'

class PasswordNewEntry(DocumentBasedEntry):
    def __init__(self, username):
        super().__init__()
        self.username = username
        # Initialize the sources
        self.sources = []

    def to_json(self):
        return {
            'username' : self.username,
            'sources' : [source.to_json() for source in self.sources]
        }

    def __str__(self) -> str:
        return f'{self.username} {[source for source in self.sources]}'

class PasswordValuesDTO:
    def __init__(self, username, key):
        self.username = username
        self.key = key

class PasswordAddValuesDTO(PasswordValuesDTO):
    def __init__(self, username, key, value):
        super().__init__(username, key)
        self.value = value

