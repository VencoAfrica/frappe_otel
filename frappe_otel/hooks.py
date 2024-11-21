from . import __version__

app_name = "frappe_otel"
app_title = "Frappe OTel"
app_publisher = "Castlecraft Ecommerce Pvt. Ltd."
app_description = "Frappe Framework wrappers for Opentelemetry"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "support@castlecraft.in"
app_license = "MIT"
app_version = __version__

before_job = ["frappe_otel.background.init_background_tracing"]
