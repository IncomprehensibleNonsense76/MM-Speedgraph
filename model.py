from dataclasses import dataclass, field
from enums import LabeledEnum


@dataclass
class Check:
    """An acquirable item, song, mask, or event in the game."""
    id: LabeledEnum
    scene: str
    requires: set[str] = field(default_factory=set)

    @property
    def name(self) -> str:
        return self.id.label

    def __repr__(self):
        return f"Check({self.id!r}, {self.scene!r})"
