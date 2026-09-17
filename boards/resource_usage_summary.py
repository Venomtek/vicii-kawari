#!/usr/bin/env python3
"""Create a Markdown resource summary for all rev_4G and rev_4H sweeps."""

import re
import sys
from pathlib import Path


BOARD_NAMES = ("rev_4G", "rev_4H")
RESOURCE_NAMES = (
    "EFX_ADD",
    "EFX_LUT4",
    "EFX_MULT",
    "EFX_FF",
    "EFX_RAM_5K",
    "EFX_DPRAM_5K",
    "EFX_GBUFCE",
)
RESOURCE_LIMITS = {
    "EFX_LUT4": 19_728,
    "EFX_MULT": 36,
    "EFX_FF": 13_920,
    "EFX_GBUFCE": 16,
}
MEMORY_BLOCK_LIMIT = 204
OUTPUT_NAME = "resource_usage_summary.md"


def read_sweep(sweep_dir):
    """Return the variant name and resource values for one sweep directory."""
    variant_file = sweep_dir / "variant.txt"
    log_file = sweep_dir / "seed_0" / "outflow" / "vicii.info.log"

    variant = variant_file.read_text(encoding="utf-8").strip()
    if not variant:
        raise ValueError("variant.txt is empty")

    log = log_file.read_text(encoding="utf-8", errors="replace")
    values = {}
    for resource in RESOURCE_NAMES:
        matches = re.findall(rf"\b{re.escape(resource)}\s*:\s*(\d+)\s*$", log, re.MULTILINE)
        if not matches:
            raise ValueError(f"{resource} is missing from {log_file.relative_to(sweep_dir)}")
        values[resource] = int(matches[-1])

    return variant, values


def markdown_table(rows):
    """Format resource rows as a Markdown document."""
    headers = (
        "Board", "Variant", "EFX_ADD", "EFX_LUT4", "EFX_MULT", "EFX_FF",
        "EFX_RAM_5K", "EFX_DPRAM_5K", "Total 5K Memory", "EFX_GBUFCE",
    )
    lines = [
        "# Resource Usage Summary",
        "",
        "Generated from `seed_0/outflow/vicii.info.log` in each sweep directory.",
        "",
        ("FPGA limits: 19,728 LUT4, 13,920 FF, 204 shared 5 Kbit memory "
         "blocks (1,020 Kbit), 36 multipliers, and 16 global clock nets. "
         "The total memory column combines EFX_RAM_5K and EFX_DPRAM_5K. "
         "EFX_ADD has no separately specified limit."),
        "",
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for board, variant, values in rows:
        variant = variant.replace("|", "\\|")
        resource_cells = []
        for name in RESOURCE_NAMES:
            value = values[name]
            if name in ("EFX_RAM_5K", "EFX_DPRAM_5K"):
                resource_cells.append(str(value))
                if name == "EFX_DPRAM_5K":
                    total_memory = values["EFX_RAM_5K"] + values["EFX_DPRAM_5K"]
                    resource_cells.append(
                        f"{total_memory} [{total_memory / MEMORY_BLOCK_LIMIT:.1%}]"
                    )
            else:
                limit = RESOURCE_LIMITS.get(name)
                percentage = "N/A" if limit is None else f"{value / limit:.1%}"
                resource_cells.append(f"{value} [{percentage}]")
        cells = (board, variant) + tuple(resource_cells)
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main():
    boards_dir = Path(__file__).resolve().parent
    rows = []
    errors = []

    for board_name in BOARD_NAMES:
        board_dir = boards_dir / board_name
        for sweep_dir in sorted(board_dir.glob("run_sweep_*")):
            if not sweep_dir.is_dir():
                continue
            try:
                variant, values = read_sweep(sweep_dir)
                rows.append((board_name, variant, values))
            except (OSError, ValueError) as error:
                errors.append(f"{sweep_dir.relative_to(boards_dir)}: {error}")

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    if not rows:
        print("error: no run_sweep_* directories found", file=sys.stderr)
        return 1

    rows.sort(key=lambda row: (row[0], row[1]))
    output_file = boards_dir / OUTPUT_NAME
    output_file.write_text(markdown_table(rows), encoding="utf-8")
    print(f"Wrote {output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
