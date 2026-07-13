from .appenders.console_appender import ConsoleAppender
from .appenders.file_appender import FileAppender
from .enums.log_level import LogLevel
from .formatter.plain_text_formatter import PlainTextFormatter
from .log_handler_configuration import LogHandlerConfiguration
from .logger import Logger


def main() -> None:
    logger = Logger.get_instance()

    LogHandlerConfiguration.add_appender_for_level(
        LogLevel.INFO,
        ConsoleAppender(PlainTextFormatter()),
    )

    LogHandlerConfiguration.add_appender_for_level(
        LogLevel.ERROR,
        ConsoleAppender(PlainTextFormatter()),
    )

    LogHandlerConfiguration.add_appender_for_level(
        LogLevel.ERROR,
        FileAppender(PlainTextFormatter(), "logs.txt"),
    )

    # Usage
    logger.info("This is some key information")  # CONSOLE
    logger.error("Oh no! there's an error")  # CONSOLE + FILE


if __name__ == "__main__":
    main()
