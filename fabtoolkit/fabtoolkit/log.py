import logging

class ConsoleLogFormatter(logging.Formatter):
    """Custom log formatter for console output with color coding based on log level."""
    # ANSI color codes
    COLORS = {
        logging.DEBUG: "\x1b[30m",      # black
        logging.INFO: "\x1b[1;30m",     # bold black
        logging.WARNING: "\x1b[33;20m", # yellow
        logging.ERROR: "\x1b[31;20m",   # red
        logging.CRITICAL: "\x1b[31;1m", # bold red
    }
    RESET = "\x1b[0m"
    MESSAGE_FORMAT = " %(asctime)s - %(message)s"
    DATE_FORMAT = "%H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record with color coding based on the log level.

        Args:
            record (logging.LogRecord): The log record to format.
        
        Returns:
            str: The formatted log message.
        """
        color = self.COLORS.get(record.levelno, self.RESET)
        log_fmt = f"{color}[{record.levelname}]{self.MESSAGE_FORMAT}{self.RESET}"
        formatter = logging.Formatter(log_fmt, datefmt=self.DATE_FORMAT)
        return formatter.format(record)