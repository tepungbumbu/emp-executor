from rich.console import Console

def show_cli_dashboard(data):
    console = Console()
    console.rule("[bold green]EMP Executor CLI Dashboard")
    console.print(data)
