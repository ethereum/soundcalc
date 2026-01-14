"""
Main entry point for soundcalc.

Loads zkVMs and produces soundness reports
"""

from __future__ import annotations

from soundcalc.zkvms import risc0, miden, zisk, dummy_whir, pico, openvm, airbender
from soundcalc import report_cli, report_md


def main(print_only: list[str] | None = None) -> None:
    """
    Main entry point for soundcalc.

    Analyze multiple zkVMs across different security regimes,
    generate reports, and save results to disk.
    """
    all_zkvms = [
        zisk.load(),
        miden.load(),
        risc0.load(),
        dummy_whir.load(),
        pico.load(),
        openvm.load(),
        airbender.load(),
    ]

    if print_only:
        filter_names = [p.lower() for p in print_only]
        zkvms = [z for z in all_zkvms if z.get_name().lower() in filter_names]
    else:
        zkvms = all_zkvms

    report_cli.print_summaries(zkvms)
    report_md.generate_and_save_reports(zkvms)


if __name__ == "__main__":
    main()
