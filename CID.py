class CID:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f'Value of a cid must be a string, got {type(value)} instead')

        self.value = value if value.startswith('/ipfs/') else f'/ipfs/{value}'

    def __str__(self) -> str:
        return self.value

    def short(self) -> str:
        return self.value[6:]

    def long(self) -> str:
        return self.value