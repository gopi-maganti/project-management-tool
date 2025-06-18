import logging
import structlog
import sys
import traceback

from structlog.processors import CallsiteParameter
from structlog.stdlib import BoundLogger


# Configure structured logging with structlog
def configure_structlog_logger():
    """
    Configure the structlog logger with processors and pretty JSON output.
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.CallsiteParameterAdder({
                CallsiteParameter.FILENAME,
                CallsiteParameter.FUNC_NAME,
                CallsiteParameter.LINENO,
                CallsiteParameter.MODULE,
                CallsiteParameter.PATHNAME,
            }),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
        wrapper_class=BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(module_name: str = __name__) -> BoundLogger:
    """
    Get a structured logger.
    """
    return structlog.get_logger(module=module_name)


def log_exception(message: str, exception: Exception, **kwargs):
    """
    Log exceptions in a structured way.
    """
    logger = get_logger(kwargs.pop("module_name", __name__))
    logger.error(
        message,
        error=str(exception),
        traceback=traceback.format_exc(),
        **kwargs
    )
