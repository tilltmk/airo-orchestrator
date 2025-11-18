#!/usr/bin/env python3
"""
AIRO v2.0 - Automated Idea Realization with Ollama
Modernisierte Version mit Multi-Agent-Architektur und Best Practices 2025
"""

import sys
import argparse
from typing import Optional
from orchestrator import AIROOrchestrator
from config import system

# Rich imports für bessere CLI (optional, fallback zu Standard-Ausgabe)
try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Tipp: Installieren Sie 'rich' für eine bessere CLI-Erfahrung: pip install rich")


class AIROApp:
    """Hauptanwendung für AIRO v2"""

    def __init__(self):
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None

    def print(self, *args, **kwargs):
        """Wrapper für print mit Rich-Support"""
        if self.console:
            self.console.print(*args, **kwargs)
        else:
            print(*args, **kwargs)

    def prompt(self, message: str, default: str = "") -> str:
        """Wrapper für Prompt mit Rich-Support"""
        if RICH_AVAILABLE:
            return Prompt.ask(message, default=default)
        else:
            response = input(f"{message} [{default}]: " if default else f"{message}: ")
            return response if response else default

    def confirm(self, message: str, default: bool = True) -> bool:
        """Wrapper für Confirm mit Rich-Support"""
        if RICH_AVAILABLE:
            return Confirm.ask(message, default=default)
        else:
            default_str = "Y/n" if default else "y/N"
            response = input(f"{message} [{default_str}]: ").lower()
            if not response:
                return default
            return response in ['y', 'yes', 'ja']

    def show_banner(self):
        """Zeige AIRO Banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     █████╗ ██╗██████╗  ██████╗     ██╗   ██╗██████╗     ║
║    ██╔══██╗██║██╔══██╗██╔═══██╗    ██║   ██║╚════██╗    ║
║    ███████║██║██████╔╝██║   ██║    ██║   ██║ █████╔╝    ║
║    ██╔══██║██║██╔══██╗██║   ██║    ╚██╗ ██╔╝██╔═══╝     ║
║    ██║  ██║██║██║  ██║╚██████╔╝     ╚████╔╝ ███████╗    ║
║    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝       ╚═══╝  ╚══════╝    ║
║                                                           ║
║    Automated Idea Realization with Ollama                ║
║    Version 2.0 - Multi-Agent Architecture (2025)         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""

        if RICH_AVAILABLE:
            self.console.print(banner, style="bold cyan")
        else:
            print(banner)

    def interactive_mode(self):
        """Interaktiver Modus für Projekt-Erstellung"""
        self.show_banner()

        self.print("\n[bold green]Willkommen zu AIRO v2![/bold green]")
        self.print("Erstellen Sie Software-Projekte mit KI-unterstützter Multi-Agent-Entwicklung.\n")

        # Projekt-Name
        project_name = self.prompt(
            "[cyan]Projekt-Name[/cyan]",
            "mein_projekt"
        )

        # Projekt-Beschreibung
        self.print("\n[cyan]Beschreiben Sie Ihr Projekt:[/cyan]")
        self.print("[dim](Was soll die Software tun? Welche Features brauchen Sie?)[/dim]")
        description = self.prompt("[cyan]Beschreibung[/cyan]")

        # Programmiersprache
        self.print("\n[cyan]Wählen Sie die Haupt-Programmiersprache:[/cyan]")
        languages = ["python", "javascript", "typescript", "rust", "go", "java"]

        if RICH_AVAILABLE:
            table = Table(show_header=False, box=None)
            for i, lang in enumerate(languages, 1):
                table.add_row(f"{i}.", lang)
            self.console.print(table)

            lang_choice = self.prompt("[cyan]Sprache[/cyan]", "1")
            try:
                lang_idx = int(lang_choice) - 1
                if 0 <= lang_idx < len(languages):
                    language = languages[lang_idx]
                else:
                    language = "python"
            except:
                language = "python"
        else:
            for i, lang in enumerate(languages, 1):
                print(f"{i}. {lang}")
            lang_choice = input("Wählen Sie (1-6) [1]: ") or "1"
            try:
                language = languages[int(lang_choice) - 1]
            except:
                language = "python"

        # Optionen
        self.print("\n[cyan]Optionen:[/cyan]")
        include_tests = self.confirm("Tests generieren?", True)
        include_review = self.confirm("Code-Review durchführen?", True)
        verbose = self.confirm("Ausführliche Ausgabe?", False)

        # Zusammenfassung
        self.print("\n[bold yellow]Zusammenfassung:[/bold yellow]")
        if RICH_AVAILABLE:
            summary = Table(show_header=False, box=None)
            summary.add_row("Projekt:", project_name)
            summary.add_row("Sprache:", language)
            summary.add_row("Tests:", "Ja" if include_tests else "Nein")
            summary.add_row("Review:", "Ja" if include_review else "Nein")
            self.console.print(summary)
        else:
            print(f"Projekt: {project_name}")
            print(f"Sprache: {language}")
            print(f"Tests: {'Ja' if include_tests else 'Nein'}")
            print(f"Review: {'Ja' if include_review else 'Nein'}")

        if not self.confirm("\n[bold]Projekt erstellen?[/bold]", True):
            self.print("[yellow]Abgebrochen.[/yellow]")
            return

        # Erstelle Projekt
        self.print("\n[bold green]Starte Projekt-Erstellung...[/bold green]\n")

        orchestrator = AIROOrchestrator(project_name, verbose=verbose)
        success = orchestrator.create_project(
            description=description,
            primary_language=language,
            include_tests=include_tests,
            include_review=include_review
        )

        if success:
            # Zeige Ergebnis
            summary = orchestrator.get_project_summary()

            self.print("\n[bold green]✨ Projekt erfolgreich erstellt! ✨[/bold green]\n")

            if RICH_AVAILABLE:
                result_table = Table(title="Projekt-Details")
                result_table.add_column("Eigenschaft", style="cyan")
                result_table.add_column("Wert", style="green")

                result_table.add_row("Name", summary.get('name', 'N/A'))
                result_table.add_row("Architektur", summary.get('architecture_type', 'N/A'))
                result_table.add_row("Komponenten", str(summary.get('num_components', 0)))
                result_table.add_row("Ausgabe-Verzeichnis", summary.get('output_dir', 'N/A'))

                self.console.print(result_table)

                # Komponenten-Details
                if summary.get('components'):
                    self.print("\n[bold]Generierte Komponenten:[/bold]")
                    comp_table = Table()
                    comp_table.add_column("Name", style="cyan")
                    comp_table.add_column("Datei", style="yellow")
                    comp_table.add_column("Qualität", style="green")

                    for comp in summary['components']:
                        quality = comp.get('quality', 0)
                        quality_str = f"{quality:.2f}" if quality else "N/A"
                        comp_table.add_row(
                            comp.get('name', 'N/A'),
                            comp.get('file', 'N/A'),
                            quality_str
                        )

                    self.console.print(comp_table)
            else:
                print(f"\nName: {summary.get('name')}")
                print(f"Architektur: {summary.get('architecture_type')}")
                print(f"Komponenten: {summary.get('num_components')}")
                print(f"Ausgabe: {summary.get('output_dir')}")

            self.print(f"\n[bold cyan]Nächste Schritte:[/bold cyan]")
            self.print(f"1. cd {summary.get('output_dir')}")
            self.print(f"2. Überprüfen Sie die generierten Dateien")
            if language == "python":
                self.print(f"3. pip install -r requirements.txt")
                self.print(f"4. Führen Sie die Tests aus (falls generiert)")
            elif language in ["javascript", "typescript"]:
                self.print(f"3. npm install")
                self.print(f"4. npm test")

        else:
            self.print("\n[bold red]Fehler bei der Projekt-Erstellung.[/bold red]")
            self.print("[yellow]Überprüfen Sie die Konfiguration und Ollama-Verbindung.[/yellow]")

    def run_cli(self, args):
        """Führe CLI-Modus aus"""
        if args.interactive or not args.description:
            self.interactive_mode()
        else:
            # Direkter Modus
            self.show_banner()
            orchestrator = AIROOrchestrator(args.project, verbose=args.verbose)

            success = orchestrator.create_project(
                description=args.description,
                primary_language=args.language,
                include_tests=not args.no_tests,
                include_review=not args.no_review
            )

            if success:
                summary = orchestrator.get_project_summary()
                self.print(f"\n[green]✓[/green] Projekt erstellt: {summary.get('output_dir')}")
                sys.exit(0)
            else:
                self.print("\n[red]✗[/red] Fehler bei der Projekt-Erstellung")
                sys.exit(1)


def main():
    """Haupteinstiegspunkt"""
    parser = argparse.ArgumentParser(
        description="AIRO v2 - Automated Idea Realization with Ollama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Interaktiver Modus
  python airo_v2.py

  # Direkter Modus
  python airo_v2.py -p "todo_app" -d "Eine Todo-App mit REST API" -l python

  # Mit Optionen
  python airo_v2.py -p "blog" -d "Ein Blog-System" --no-tests -v
        """
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interaktiver Modus (Standard wenn keine Beschreibung)'
    )

    parser.add_argument(
        '-p', '--project',
        default='mein_projekt',
        help='Projekt-Name (Standard: mein_projekt)'
    )

    parser.add_argument(
        '-d', '--description',
        help='Projekt-Beschreibung'
    )

    parser.add_argument(
        '-l', '--language',
        default='python',
        choices=['python', 'javascript', 'typescript', 'rust', 'go', 'java'],
        help='Programmiersprache (Standard: python)'
    )

    parser.add_argument(
        '--no-tests',
        action='store_true',
        help='Keine Tests generieren'
    )

    parser.add_argument(
        '--no-review',
        action='store_true',
        help='Kein Code-Review durchführen'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Ausführliche Ausgabe'
    )

    args = parser.parse_args()

    app = AIROApp()
    app.run_cli(args)


if __name__ == '__main__':
    main()
