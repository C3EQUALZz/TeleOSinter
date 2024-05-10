import click
import art


@click.command()
def main() -> None:
    project_name = art.text2art("TeleOSinter")
    click.echo(project_name)
    click.echo("")


if __name__ == "__main__":
    main()
