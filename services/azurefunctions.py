from appconfig import AppConfig
from services.loggerfunctions import create_logger


# Instantiate logging
log = create_logger("azure")


def create_dns(subdomain, ip, appConfig: AppConfig):
    log.info("Creating")


def delete_dns(subdomain, ip, appConfig: AppConfig):
    log.info("Deleting")


def resolve_dns_event(event):
    if event == "ADDED" or event == "MODIFIED":
        return create_dns
    if event == "DELETED":
        return delete_dns
    else:
        return None
