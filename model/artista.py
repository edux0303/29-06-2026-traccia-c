from dataclasses import dataclass, field


@dataclass
class Artista:
    id: int
    nome: str
    brani: set = field(default_factory=set)
    playlist: set = field(default_factory=set)



    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.nome