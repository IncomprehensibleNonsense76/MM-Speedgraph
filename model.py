from __future__ import annotations
from dataclasses import dataclass, field
from enums import LabeledEnum, TimeSlot


@dataclass
class Check:
    """An acquirable item, song, mask, or event in the game."""

    id: LabeledEnum
    scene: str
    requires: set[str] = field(default_factory=set)
    time: frozenset[TimeSlot] | None = None
    duration: int = 0  # seconds to acquire (cutscenes, etc.)
    warp_to: str | None = None  # position override after acquiring

    @property
    def name(self) -> str:
        return self.id.label if hasattr(self.id, "label") else str(self.id)

    @property
    def parent_scene(self) -> str:
        """Extract scene from room-qualified node like 'Woodfall Temple:Room5'."""
        return self.scene.rsplit(":", 1)[0] if ":" in self.scene else self.scene

    def __repr__(self):
        return f"Check({self.id!r}, {self.scene!r})"
