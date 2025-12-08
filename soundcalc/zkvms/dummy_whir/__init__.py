from pathlib import Path

from soundcalc.zkvms.whir_based_vm import WHIRBasedVM


def load():
    return WHIRBasedVM.load(Path(__file__).parent / "dummy_whir.json")
