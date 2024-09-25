import sys

from time import sleep
from app import App


def main(*args):
    app = App(args=args)

    try:
        app.start()
        while True:
            sleep(0.5)
    except KeyboardInterrupt:
        print("interrupted")
        app.close()
        sys.exit(0)


if __name__ == '__main__':
    main(sys.argv)
