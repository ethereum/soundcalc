from soundcalc.zkvms.fri_based_vm import FRIBasedVM
from pathlib import Path

def load():
    return FRIBasedVM.load_from_toml(Path(__file__).parent / "miden.toml")
