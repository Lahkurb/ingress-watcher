import os


class AppConfig:

    # Ingress manifest annotation to trigger this script
    annotation_trigger = os.getenv("ANNOTATION_TRIGGER", "org.debarrage.dns")

    # Namespace to watch, default value is default
    namespace = os.getenv("NAMESPACE", "default")

    # Azure Tenant ID
    az_tenant = os.getenv("AZ_TENANT", "")

    # Azure Subscription ID
    az_subscription = os.getenv("AZ_SUBSCRIPTION", "")

    # Azure Service account user for automation
    az_user = os.getenv("AZ_USER", "")

    # Azure Service account psswoard
    az_pwd = os.getenv("AZ_PWD", "")

    # Azure Resource group where the DNS resource is installed
    az_resourcegroup = os.getenv("AZ_RESGROUP", "")

    # Azure DNS resource
    az_dns = os.getenv("AZ_DNS", "")

