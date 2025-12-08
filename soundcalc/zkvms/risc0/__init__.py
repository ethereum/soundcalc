from pathlib import Path

from soundcalc.zkvms.fri_based_vm import FRIBasedVM


def load():
    return FRIBasedVM.load(Path(__file__).parent / "risc0.json")
