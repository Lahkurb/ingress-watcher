from appconfig import AppConfig
from services.loggerfunctions import create_logger
from azure.mgmt.dns import DnsManagementClient
from azure.common.credentials import UserPassCredentials
from azure.common.credentials import ServicePrincipalCredentials

# Instantiate logging
log = create_logger("azure")

def az_credentials(appConfig: AppConfig):
    return ServicePrincipalCredentials(
        client_id=appConfig.az_user,
        secret=appConfig.az_pwd,
        tenant=appConfig.az_tenant
    )

def az_client(appConfig: AppConfig):
    return DnsManagementClient(
        az_credentials(appConfig),
        appConfig.az_subscription
    )

def create_dns(subdomain, ip, appConfig: AppConfig):
    client = az_client(appConfig)
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
