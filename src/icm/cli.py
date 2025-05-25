from typing import Annotated

import typer
from pathlib import Path
from ruamel.yaml import YAML
from icm.mix_tapes import MixTapeBuilder
import logging.config

cli = typer.Typer()

yaml = YAML()

config = {
    "version": 1,
    "formatters": {"simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": logging.DEBUG,
        }
    },
    "root": {"handlers": ["console"], "level": logging.INFO},
    "disable_existing_loggers": False,
}

logging.config.dictConfig(config)


DATA_FILE = Annotated[Path, typer.Argument(help="Path to yaml data file")]
USERNAME = Annotated[str, typer.Option(help="Spotify Username", envvar="SPOTIFY_USERNAME")]
DRYRUN = Annotated[bool, typer.Option(help="Search for tracks but do not actually make playlist")]
MIN_HIT_RATE = Annotated[float, typer.Option(help="Fraction of hits required to make playlist")]


@cli.command()
def make_playlists(
    data_file: DATA_FILE,
    username: USERNAME,
    min_hit_rate: MIN_HIT_RATE = 0.7,
    dryrun: DRYRUN = False,
):
    tape_list = yaml.load(data_file)
    MixTapeBuilder(username).process_tape_list(tape_list, min_hit_rate, dryrun)

    if not dryrun:
        yaml.dump(tape_list, data_file)


if __name__ == "__main__":
    cli()
