from opentelemetry.instrumentation.instrumentor import BaseInstrumentor


def init_background_tracing(*args, **kwargs):
    BaseInstrumentor().instrument()
