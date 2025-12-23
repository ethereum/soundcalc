from soundcalc.zkvms.zkvm import zkVM
from pathlib import Path

def load():
    return zkVM.load_from_toml(Path(__file__).parent / "openvm.toml")
