import signal

from kubernetes import client, config, watch
from appconfig import AppConfig
from services.azurefunctions import resolve_dns_event
from services.kubernetesfunctions import find_ips, process_ingress, ingress_subdomain, ingress_markprocessed
from services.loggerfunctions import create_logger
import sys

# Instantiate logging
log = create_logger("ingress-watcher")

# Load the kubernetes configuration from the kubeconfig file
config.load_kube_config()

# Instantiate the kubernetes clients
v1 = client.CoreV1Api()
extv1beta1 = client.ExtensionsV1beta1Api()

# Load the app config
appConfig = AppConfig()

# Get the public ips
ips = find_ips(v1)
log.info("Found external ip addresses: %s" % ips)

# Log config
log.info("Watching ingresses with annotation %s" % appConfig.annotation_trigger)

# Instantiate the watcher
w = watch.Watch()

# Configure signal handlers
signal.signal(signal.SIGINT, lambda s, frame: w.stop())
signal.signal(signal.SIGINT, lambda s, frame: log.critical("Received SIGINT"))

# Core watch loop
log.info("Listening on namespace %s" % appConfig.namespace)
for item in w.stream(extv1beta1.list_namespaced_ingress, appConfig.namespace):
    try:
        # Get the ingress, event and name
        ingress = item['object']
        event = item['type']
        name = ingress.metadata.name

        # Check if the ingress contains the correct annotations, if so proceed
        if process_ingress(ingress, appConfig):
            # Get subdomain from the annotation
            subdomain = ingress_subdomain(ingress, appConfig)

            # Resolve the correct action
            action = resolve_dns_event(event)
            if action is not None:
                log.info("Processing %s %s" % (name, event))
                result = action(subdomain, ips, appConfig)

        else:
            log.debug("Skipping %s" % name)
    except:
        log.error("Something went wrong while looping", sys.exc_info())
        w.stop()
        sys.exit(1)

# Exit the program
log.info("The program has stopped")
sys.exit(0)
