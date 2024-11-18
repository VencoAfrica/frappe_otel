import os

import click
import frappe
from rq import Connection, Worker

from frappe.utils.background_jobs import (  # isort:skip
    get_queue_list,
    get_redis_conn,
    get_worker_name,
)


@click.command("worker-with-apm")
@click.option(
    "--queue",
    type=str,
    help=(
        "Queue to consume from. Multiple queues can be "
        "specified using comma-separated string. "
        "If not specified all queues are consumed."
    ),
)
@click.option("--quiet", is_flag=True, default=False, help="Hide Log Outputs")
def start_worker(queue, quiet=False):

    _start_sentry()
    with frappe.init_site():
        # empty init is required to get
        # redis_queue from common_site_config.json
        redis_connection = get_redis_conn()

    with Connection(redis_connection):
        queues = get_queue_list(queue)
        logging_level = "INFO"
        if quiet:
            logging_level = "WARNING"
        Worker(queues, name=get_worker_name(queue)).work(
            logging_level=logging_level
        )  # noqa: E501


def _start_sentry():
    sentry_dsn = os.getenv("FRAPPE_SENTRY_DSN")
    if not sentry_dsn:
        return

    import sentry_sdk
    from sentry_sdk.integrations.argv import ArgvIntegration
    from sentry_sdk.integrations.atexit import AtexitIntegration
    from sentry_sdk.integrations.dedupe import DedupeIntegration
    from sentry_sdk.integrations.excepthook import ExcepthookIntegration
    from sentry_sdk.integrations.modules import ModulesIntegration

    from frappe_otel.sentry import FrappeIntegration, before_send

    integrations = [
        AtexitIntegration(),
        ExcepthookIntegration(),
        DedupeIntegration(),
        ModulesIntegration(),
        ArgvIntegration(),
    ]

    experiments = {}
    kwargs = {}

    if os.getenv("ENABLE_SENTRY_DB_MONITORING"):
        integrations.append(FrappeIntegration())
        experiments["record_sql_params"] = True

    tracing_sample_rate = os.getenv("SENTRY_TRACING_SAMPLE_RATE")
    if tracing_sample_rate:
        kwargs["traces_sample_rate"] = float(tracing_sample_rate)

    sentry_sdk.init(
        dsn=sentry_dsn,
        before_send=before_send,
        attach_stacktrace=True,
        release=frappe.__version__,
        auto_enabling_integrations=False,
        default_integrations=False,
        integrations=integrations,
        _experiments=experiments,
        **kwargs,
    )
