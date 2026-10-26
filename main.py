
from pathlib import Path

from src.eventbot import EventBot


def main():
    ruta_proyecto = Path(__file__).resolve().parent

    bot = EventBot(ruta_proyecto)
    bot.conversar()


if __name__ == "__main__":
    main()
