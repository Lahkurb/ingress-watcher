from kubernetes.client import CoreV1Api
from services.loggerfunctions import create_logger

from appconfig import AppConfig

# Instantiate logging
log = create_logger("kubernetes")

system_namespace = "kube-system"


def find_ips(v1: CoreV1Api):
    ips = []
    # try:
    services = v1.list_namespaced_service(system_namespace).items
    for s in services:
        try:
            if s.status.load_balancer.ingress:
                for i in s.status.load_balancer.ingress:
                    ips.append(i.ip)
        except:
            log.info("Cannot process service %s" % s.metadata.self_link)
    # except:
    #     print("Cannot get all services in %s" % system_namespace)

    if len(ips) > 0:
        return ips
    else:
        return ["127.0.0.1"]


def process_ingress(ingress, appConfig: AppConfig):
    if ingress.metadata.annotations is not None:
        if appConfig.annotation_trigger in ingress.metadata.annotations:
            return True
    return False


def ingress_subdomain(ingress, appConfig: AppConfig):
    if process_ingress(ingress, appConfig):
        return ingress.metadata.annotations[appConfig.annotation_trigger]
