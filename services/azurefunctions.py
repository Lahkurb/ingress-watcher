import sys

from appconfig import AppConfig
from services.loggerfunctions import create_logger
from azure.mgmt.dns import DnsManagementClient
from azure.common.credentials import UserPassCredentials
from azure.common.credentials import ServicePrincipalCredentials

# Instantiate logging
log = create_logger("azure")

# Some common params
record_type = "A"


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


def create_dns(subdomain, ips, appConfig: AppConfig):
    """
    Create a DNS record.

    :param subdomain: string value of the subdomain
    :param ips: array of ip addresses
    :param appConfig: configuration
    :return: true when succeeded
    """
    try:
        log.info("Creating A-record %s in %s" % (subdomain, appConfig.az_dns))
        client = az_client(appConfig)

        client.record_sets.create_or_update(
            appConfig.az_resourcegroup,
            appConfig.az_dns,
            subdomain,
            record_type,
            {
                "arecords": list(map(lambda ip: {"ipv4_address": ip}, ips)),
                "ttl": 360,
            }
        )

        # Log and return
        log.info("Created A-record %s in %s" % (subdomain, appConfig.az_dns))
        return True

    except:
        log.info("Cannot create A-record", sys.exc_info()[0])
        return False


def delete_dns(subdomain, ips, appConfig: AppConfig):
    """
    Delete a DNS record

    :param subdomain: string value of the subdomain
    :param ips: array of ip addresses
    :param appConfig: configuration
    :return: true when succeeded
    """

    try:
        client = az_client(appConfig)
        client.record_sets.delete(
            appConfig.az_resourcegroup,
            appConfig.az_dns,
            subdomain,
            record_type
        )

        # Lig and return
        log.info("Deleted A-record %s in %s" % (subdomain, appConfig.az_dns))
        return True

    except:
        log.info("Cannot create A-record", sys.exc_info()[0])
        return False


def resolve_dns_event(event):
    log.debug("Resolving event %s" % event)
    if event == "ADDED" or event == "MODIFIED":
        return create_dns
    if event == "DELETED":
        return delete_dns
    else:
        return None
