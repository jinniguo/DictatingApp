"""iOS entrypoint."""

from shared.mobile_app import DictationApp


if __name__ == "__main__":
    DictationApp(platform_name="iPhone").run()
