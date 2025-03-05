from typing import Annotated

import typer
from pathlib import Path
from ruamel.yaml import YAML
from icm.mix_tapes import MixTapeBuilder
import logging.config

cli = typer.Typer()

yaml = YAML()

config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': logging.DEBUG
        }
    },
    'root': {
        'handlers': ['console'],
        'level': logging.INFO
    },
    'disable_existing_loggers': False
}

logging.config.dictConfig(config)


DATA_FILE = Annotated[Path, typer.Argument(help="Path to yaml data file")]
USERNAME = Annotated[str, typer.Option(envvar="SPOTIFY_USERNAME")]

@cli.command()
def make_playlists(data_file: DATA_FILE, username: USERNAME):
    tape_list = yaml.load(data_file)
    MixTapeBuilder(username).process_tape_list(tape_list)
    yaml.dump(tape_list, data_file)

if __name__ == "__main__":
    cli()
