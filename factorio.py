from typing import List

from draftsman.blueprintable import Blueprint
from draftsman.entity import ConstantCombinator


def generate_flasher_blueprint(machine_code: List[int], label: str | None = None) -> str:
    blueprint = Blueprint()
    blueprint.label = label

    for i, code in enumerate(machine_code):
        combinator = ConstantCombinator(tile_position=(0, i))
        section = combinator.add_section()
        section.set_signal(0, name="signal-dot", type="virtual", count=code)
        blueprint.entities.append(combinator)

    return blueprint.to_string()
