import typer
from .summarize import summarizeFileDocs, summarizeHTML

summarizeDocSite = typer.Typer()
summarizeDocSite.command()(summarizeHTML)
summarizeDocFiles = typer.Typer(no_args_is_help=True)
summarizeDocFiles.command()(summarizeFileDocs)

if __name__ == "__main__":
    summarizeDocSite()
    summarizeDocFiles()

