from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Confirm
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule
import time

console = Console()

# ── Palette ──────────────────────────────────────────────────────────────────
C_ACCENT  = "bright_green"
C_DIM     = "grey50"
C_WARN    = "yellow"
C_ERR     = "bright_red"
C_INFO    = "cyan"
C_SUCCESS = "bright_green"
C_HEAD    = "bold bright_white"

BANNER = r"""
 ██████╗ ███████╗██╗   ██╗    ██╗    ██╗██╗███████╗ █████╗ ██████╗ ██████╗ 
 ██╔══██╗██╔════╝██║   ██║    ██║    ██║██║╚══███╔╝██╔══██╗██╔══██╗██╔══██╗
 ██║  ██║█████╗  ██║   ██║    ██║ █╗ ██║██║  ███╔╝ ███████║██████╔╝██║  ██║
 ██║  ██║██╔══╝  ╚██╗ ██╔╝    ██║███╗██║██║ ███╔╝  ██╔══██║██╔══██╗██║  ██║
 ██████╔╝███████╗ ╚████╔╝     ╚███╔███╔╝██║███████╗██║  ██║██║  ██║██████╔╝
 ╚═════╝ ╚══════╝  ╚═══╝       ╚══╝╚══╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
"""

def print_banner():
    console.print()
    console.print(BANNER, style=C_ACCENT, highlight=False)
    console.print(
        Align.center(
            Text("⚡  Dev Environment Setup Wizard  ·  Node.js + npm  ·  WSL/Ubuntu  ⚡",
                 style=f"bold {C_INFO}")
        )
    )
    console.print(
        Align.center(Text("─" * 70, style=C_DIM))
    )
    console.print()


def section(title: str):
    console.print()
    console.print(Rule(f"[bold {C_ACCENT}] {title} [/]", style=C_DIM))
    console.print()


def step_panel(number: int, total: int, title: str, description: str):
    header = Text()
    header.append(f"  STEP {number}/{total}  ", style="bold black on bright_green")
    header.append(f"  {title}", style="bold bright_white")
    console.print(header)
    console.print(f"  [dim]{description}[/dim]")
    console.print()


def success(msg: str):
    console.print(f"  [bold {C_SUCCESS}]✔[/]  {msg}")


def warn(msg: str):
    console.print(f"  [{C_WARN}]⚠[/]  [{C_WARN}]{msg}[/]")


def info(msg: str):
    console.print(f"  [{C_INFO}]ℹ[/]  [dim]{msg}[/dim]")


def error(msg: str):
    console.print(f"  [bold {C_ERR}]✘[/]  [{C_ERR}]{msg}[/]")


def confirm(prompt: str, default: bool = True) -> bool:
    return Confirm.ask(f"  [bold {C_INFO}]?[/]  {prompt}", default=default)


def spinner_task(description: str, func, *args, **kwargs):
    """Run func inside a spinner, return its result."""
    with Progress(
        SpinnerColumn(style=C_ACCENT),
        TextColumn(f"[{C_DIM}]{description}[/]"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("", total=None)
        result = func(*args, **kwargs)
    return result


def progress_steps(steps: list):
    """
    Display a multi-step progress bar.
    steps = list of (label, callable)
    Returns list of results.
    """
    results = []
    with Progress(
        SpinnerColumn(style=C_ACCENT),
        BarColumn(bar_width=30, style=C_DIM, complete_style=C_ACCENT),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("[dim]{task.description}[/dim]"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Running…", total=len(steps))
        for label, fn in steps:
            progress.update(task, description=label)
            result = fn()
            results.append(result)
            progress.advance(task)
            time.sleep(0.15)   # small pause so each step is visible
    return results


def summary_table(rows: list[dict]):
    """
    Render a summary table.
    rows = [{"check": str, "status": "ok"|"warn"|"skip"|"fail", "detail": str}]
    """
    table = Table(
        box=box.ROUNDED,
        border_style=C_DIM,
        show_header=True,
        header_style=f"bold {C_HEAD}",
        expand=True,
    )
    table.add_column("Check", style="bold white", min_width=26)
    table.add_column("Status", justify="center", min_width=8)
    table.add_column("Detail", style=C_DIM)

    icons = {
        "ok":   (f"[{C_SUCCESS}]✔ OK[/]",),
        "warn": (f"[{C_WARN}]⚠ WARN[/]",),
        "skip": (f"[{C_DIM}]– SKIP[/]",),
        "fail": (f"[{C_ERR}]✘ FAIL[/]",),
    }

    for row in rows:
        icon_str = icons.get(row["status"], (row["status"],))[0]
        table.add_row(row["check"], icon_str, row.get("detail",""))

    console.print(table)


def final_panel(title: str, lines: list[str], color: str = C_ACCENT):
    body = "\n".join(f"  {l}" for l in lines)
    console.print()
    console.print(
        Panel(
            body,
            title=f"[bold {color}] {title} [/]",
            border_style=color,
            padding=(1, 2),
        )
    )
    console.print()
