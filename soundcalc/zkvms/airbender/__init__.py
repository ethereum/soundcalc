from pathlib import Path

from soundcalc.zkvms.zkvm import zkVM

def load():
    return zkVM.load_from_toml(Path(__file__).parent / "airbender.toml")
