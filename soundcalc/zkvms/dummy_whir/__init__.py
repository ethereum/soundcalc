from soundcalc.zkvms.whir_based_vm import WHIRBasedVM
from pathlib import Path

def load():
    return WHIRBasedVM.load_from_toml(Path(__file__).parent / "dummy_whir.toml")
