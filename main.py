import signal

from kubernetes import client, config, watch
from appconfig import AppConfig
from services.kubernetesfunctions import find_ips, process_ingress
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
for item in w.stream(extv1beta1.list_namespaced_ingress, "debarrage", watch=10):
    try:
        ingress = item['object']
        event = item['type']
        name = ingress.metadata.name
        if process_ingress(ingress, appConfig):
            log.info("Processing %s %s" % (name, event))
        else:
            log.debug("Skipping %s" % name)
        # print(ingress.metadata.annotations)
        # # print("Event: %s %s" % (event['type'], event['object'].metadata.name))
    except:
        log.error("Something went wrong while looping", sys.exc_info())
        w.stop()

log.info("The program has stopped")
