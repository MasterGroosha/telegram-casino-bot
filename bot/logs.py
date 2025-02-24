import logging
from json import dumps
from sys import stdout

import structlog
from structlog import WriteLoggerFactory
from structlog.typing import WrappedLogger, EventDict

from bot.config_reader import LogConfig, LogRenderer


class ProjectNameProcessor:
    def __init__(self, project_name: str):
        self.project_name = project_name

    def __call__(
        self, logger: WrappedLogger, name: str, event_dict: EventDict
    ) -> EventDict:
        event_dict["project_name"] = self.project_name
        return event_dict


def get_structlog_config(log_config: LogConfig) -> dict:
    if log_config.show_debug_logs is True:
        min_level = logging.DEBUG
    else:
        min_level = logging.INFO

    if log_config.allow_third_party_logs:
        # Create handler for stdlib logging
        standard_handler = logging.StreamHandler(stream=stdout)
        standard_handler.setFormatter(
            structlog.stdlib.ProcessorFormatter(
                processors=get_processors(log_config)
            )
        )

        # Configure root logger to use this handler
        standard_logger = logging.getLogger()
        standard_logger.addHandler(standard_handler)
        standard_logger.setLevel(logging.DEBUG if log_config.show_debug_logs else logging.INFO)


    return {
        "processors": get_processors(log_config),
        "cache_logger_on_first_use": True,
        "wrapper_class": structlog.make_filtering_bound_logger(min_level),
        "logger_factory": WriteLoggerFactory()
    }


def get_processors(log_config: LogConfig) -> list:
    def custom_json_serializer(data, *args, **kwargs):
        result = dict()

        # Set keys in specific order
        for key in ("level", "event"):
            if key in data:
                result[key] = data.pop(key)

        # Clean up non-native structlog logs:
        if "_from_structlog" in data:
            data.pop("_from_structlog")
            data.pop("_record")

        # Add all other fields
        result.update(**data)
        return dumps(result, default=str)

    processors = list()
    if log_config.show_datetime is True:
        processors.append(structlog.processors.TimeStamper(
            fmt=log_config.datetime_format,
            utc=log_config.time_in_utc
            )
        )

    processors.append(structlog.processors.add_log_level)
    processors.append(ProjectNameProcessor(log_config.project_name))

    if log_config.renderer == LogRenderer.JSON:
        processors.append(structlog.processors.format_exc_info)
        processors.append(structlog.processors.JSONRenderer(serializer=custom_json_serializer))
    else:
        processors.append(structlog.dev.ConsoleRenderer(
            colors=log_config.use_colors_in_console,
            pad_level=False
        ))
    return processors
