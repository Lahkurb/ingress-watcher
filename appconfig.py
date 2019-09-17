import os


class AppConfig:

    annotation_trigger = os.getenv(
        "ANNOTATION_TRIGGER", "org.debarrage.dns")
    annotation_confirmed = os.getenv(
        "ANNOTATION_CONFIRMED", "org.debarrage.dns.confirmed")
    namespace = os.getenv("NAMESPACE", "default")

    az_tenant = os.getenv("AZ_TENANT", "")
    az_subscription = os.getenv("AZ_SUBSCRIPTION", "")
    az_user = os.getenv("AZ_USER", "")
    az_pwd = os.getenv("AZ_PWD", "")

