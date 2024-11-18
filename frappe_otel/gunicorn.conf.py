import logging
from uuid import uuid4

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, Resource

from opentelemetry.exporter.otlp.proto.http._log_exporter import (  # isort:skip  # noqa: E501
    OTLPLogExporter,
)


def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

    resource = Resource.create(
        attributes={
            # each worker needs a unique service.instance.id
            # to distinguish the created metrics in prometheus
            SERVICE_INSTANCE_ID: str(uuid4()),
            "worker": worker.pid,
        }
    )

    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter())
    )  # noqa: E501

    logging_handler = LoggingHandler(
        level=logging.INFO, logger_provider=logger_provider
    )
    logging.getLogger().setLevel(logging.INFO)  # Set root logger to INFO
    logging.getLogger().addHandler(logging_handler)
