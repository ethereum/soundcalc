"""
Main entry point for soundcalc.

Loads zkVMs and produces soundness reports
"""

from __future__ import annotations

from soundcalc.zkvms import risc0, miden, zisk, dummy_whir, pico, openvm, airbender, sp1
from soundcalc import report_cli, report_md

# All zkVM loaders
_LOADERS = [
    ("ZisK", zisk.load),
    ("Miden", miden.load),
    ("RISC0", risc0.load),
    ("DummyWHIR", dummy_whir.load),
    ("Pico", pico.load),
    ("OpenVM", openvm.load),
    ("Airbender", airbender.load),
    ("SP1", sp1.load),
]


def _load_zkvms():
    """
    Load all zkVMs, gracefully skipping those with incomplete configuration.
    """
    zkvms = []
    skipped = []

    for name, loader in _LOADERS:
        try:
            zkvms.append(loader())
        except KeyError as e:
            skipped.append((name, e.args[0]))

    if skipped:
        print("Note: Some zkVMs were skipped (incomplete configuration):")
        for name, key in skipped:
            print(f"  - {name}: missing '{key}'")
        print()

    return zkvms


def main(print_only: list[str] | None = None) -> None:
    """
    Main entry point for soundcalc.

    Analyze multiple zkVMs across different security regimes,
    generate reports, and save results to disk.
    """
    all_zkvms = _load_zkvms()

    if print_only:
        filter_names = [p.lower() for p in print_only]
        zkvms = [z for z in all_zkvms if z.get_name().lower() in filter_names]
    else:
        zkvms = all_zkvms

    report_cli.print_summaries(zkvms)
    report_md.generate_and_save_reports(zkvms)


if __name__ == "__main__":
    main()
