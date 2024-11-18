from frappe.app import application
from opentelemetry.instrumentation.wsgi import OpenTelemetryMiddleware

application = OpenTelemetryMiddleware(application)
