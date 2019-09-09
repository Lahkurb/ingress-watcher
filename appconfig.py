import os


class AppConfig:

    annotation_trigger = os.getenv(
        "ANNOTATION_TRIGGER", "org.debarrage.dns")
    annotation_confirmed = os.getenv(
        "ANNOTATION_CONFIRMED", "org.debarrage.dns.confirmed")

