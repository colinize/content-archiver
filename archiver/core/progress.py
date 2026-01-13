"""Progress tracking and interactive prompts using Rich."""

from typing import Optional, Callable, Any
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    TaskID,
)
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()


class DownloadProgress:
    """Manages download progress display."""

    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
        )
        self._task_id: Optional[TaskID] = None

    def __enter__(self):
        self.progress.__enter__()
        return self

    def __exit__(self, *args):
        self.progress.__exit__(*args)

    def start_task(self, description: str, total: Optional[int] = None) -> TaskID:
        """Start a new download task."""
        self._task_id = self.progress.add_task(description, total=total or 0)
        return self._task_id

    def update(self, completed: int, total: Optional[int] = None) -> None:
        """Update progress."""
        if self._task_id is not None:
            if total:
                self.progress.update(self._task_id, completed=completed, total=total)
            else:
                self.progress.update(self._task_id, completed=completed)

    def finish(self) -> None:
        """Mark current task as finished."""
        if self._task_id is not None:
            self.progress.update(self._task_id, completed=self.progress.tasks[self._task_id].total)


def show_found_items(
    content_type: str,
    source_name: str,
    items: list[dict],
    item_label: str = "items"
) -> None:
    """Display a summary of found items."""
    panel_content = f"[bold]{content_type.upper()}[/bold]: {source_name}\n\n"
    panel_content += f"Found [bold green]{len(items)}[/bold green] {item_label}"

    # Show first few items as preview
    if items:
        panel_content += "\n\n[dim]Preview:[/dim]"
        for item in items[:5]:
            title = item.get("title", item.get("name", "Unknown"))
            panel_content += f"\n  • {title[:60]}{'...' if len(title) > 60 else ''}"
        if len(items) > 5:
            panel_content += f"\n  [dim]... and {len(items) - 5} more[/dim]"

    rprint(Panel(panel_content, title="[bold]Content Found[/bold]", border_style="green"))


def confirm_download(
    count: int,
    item_label: str = "items",
    allow_select: bool = True
) -> str:
    """Prompt user to confirm download. Returns 'all', 'none', or 'select'."""
    if allow_select:
        choice = Prompt.ask(
            f"\nDownload all {count} {item_label}?",
            choices=["y", "n", "select"],
            default="y"
        )
        if choice == "y":
            return "all"
        elif choice == "n":
            return "none"
        else:
            return "select"
    else:
        if Confirm.ask(f"\nDownload all {count} {item_label}?", default=True):
            return "all"
        return "none"


def select_items(items: list[dict], title_key: str = "title") -> list[int]:
    """Let user select specific items. Returns list of indices."""
    console.print("\n[bold]Select items to download:[/bold]")
    for i, item in enumerate(items):
        title = item.get(title_key, f"Item {i+1}")
        console.print(f"  [{i+1}] {title[:70]}{'...' if len(title) > 70 else ''}")

    selection = Prompt.ask(
        "\nEnter numbers (comma-separated) or 'all'",
        default="all"
    )

    if selection.lower() == "all":
        return list(range(len(items)))

    try:
        indices = [int(x.strip()) - 1 for x in selection.split(",")]
        return [i for i in indices if 0 <= i < len(items)]
    except ValueError:
        console.print("[red]Invalid selection, downloading all[/red]")
        return list(range(len(items)))


def show_status(stats: dict, downloads: list) -> None:
    """Display archive status and history."""
    # Stats summary
    console.print("\n[bold]Archive Status[/bold]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Status")
    table.add_column("Count", justify="right")

    for status, count in stats.get("by_status", {}).items():
        color = {
            "complete": "green",
            "pending": "yellow",
            "downloading": "blue",
            "error": "red"
        }.get(status, "white")
        table.add_row(status.title(), f"[{color}]{count}[/{color}]")

    console.print(table)

    # Recent downloads
    if downloads:
        console.print("\n[bold]Recent Downloads[/bold]\n")
        dl_table = Table(show_header=True, header_style="bold")
        dl_table.add_column("Source")
        dl_table.add_column("Title")
        dl_table.add_column("Type")
        dl_table.add_column("Status")

        for dl in downloads[:10]:
            status_color = {
                "complete": "green",
                "pending": "yellow",
                "downloading": "blue",
                "error": "red"
            }.get(dl.status, "white")

            dl_table.add_row(
                dl.source_name[:20] if dl.source_name else "",
                dl.title[:30] + "..." if dl.title and len(dl.title) > 30 else (dl.title or ""),
                dl.content_type,
                f"[{status_color}]{dl.status}[/{status_color}]"
            )

        console.print(dl_table)


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[blue]ℹ[/blue] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[yellow]⚠[/yellow] {message}")
