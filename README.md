# Ingress Watcher
> Small python deamon script to watch kubernetes and to create DNS A records in Azure

## Installation
Manifests files are included in the form of a Helm chart.

### Azure configuration
You need a DNS Zone in Azure and a service account.

#### Create the service account
Make sure that the Azure CLI is installed and that you are logged in. Then create an RBAC account.

```bash
az ad sp create-for-rbac --name "<desired user name>"

```

The created user incl. password is returned. The newly created service account needs to have the contributor
role to the DNS Zone.

### Kubernetes configuration
You need a valide kubeconfig file. The kubernetes client will be configured in code with the existing current
kubernetes cluster.

### Program configuration
The program is entirely configured with environment variables. Look at the file `appconfig.py` to see all
required environment variables and what they mean.

In order to make it work, all environment variables must be instantiated!