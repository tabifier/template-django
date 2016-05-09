## Create the cluster
Create a project and enable ContainerEngine API for the following:
* Google Container Engine API
* Google Compute Engine and associated APIs

Pick a Zone and a machine type from this list :

```bash
$ gcloud compute zones list
$ gcloud compute machine-types list
```

Create some environment variables
```bash
ZONE=us-east1-c
CLUSTER_ENVIRONMENT=prod
CLUSTER_NAME=roller-$CLUSTER_ENVIRONMENT
CLUSTER_USERNAME=admin
CLUSTER_PASSWORD=
CLUSTER_NUM_NODES=3
CLUSTER_MACHINE_TYPE=n1-standard-1
CLUSTER_MACHINE_DISK_SIZE=100
```

Set the project for gcloud
```bash
PROJECT=roller-io
gcloud config set project $PROJECT
gcloud config set compute/zone $ZONE
```

**NOTE**: Creating a container cluster in the '*default*' network. It's large
enough and can be subnetworked. The auto mode doesn't add firewall rules
or create a large subnetwork. Investigate in the future if necessary.
Ref: https://cloud.google.com/compute/docs/networking#networks
  { $ gcloud compute networks create $CLUSTER_ENVIRONMENT --mode auto }

```bash
gcloud container clusters create $CLUSTER_NAME \
  --zone $ZONE \
  --num-nodes $CLUSTER_NUM_NODES \
  --machine-type $CLUSTER_MACHINE_TYPE\
  --username $CLUSTER_USERNAME \
  --password $CLUSTER_PASSWORD \
  --network default \
  --disk-size $CLUSTER_MACHINE_DISK_SIZE \
  --enable-cloud-monitoring \
  --enable-cloud-logging

# Set the default cluster
gcloud config set container/cluster $CLUSTER_NAME
```

## Passing cluster credentials to kubectl
Let Kubernetes know which cluster to use
```bash
gcloud container clusters get-credentials $CLUSTER_NAME
```

## Create Cloud SQL db

1. Generate a new DB from the console and Authorize the instnaces CREATEDB
   in the previous step to use the db instance.
2. After the database is created setup a root password under access control
   and save the password in roller's 1Password vault

**TODO**: Generate Cloud SQL Generation script to switch to a containerized SQL
**Ref**: https://cloud.google.com/sql/docs/create-instance

**TODO**: Use the dockerized version of the SQL proxy  to connect to the db
**Ref**: https://cloud.google.com/sql/docs/compute-engine-access#gce-connect-proxydocker


**NOTE** To delete an cluster, issue the following command
```bash
gcloud container clusters delete $CLUSTER_NAME --zone $ZONE
```

## Make your cluster accessible
Create a static IP address that will be used by the public load balancer
```bash
gcloud compute forwarding-rules create
```

## Keep track of the secrets

Create/Update the secrets file in the 1Password vault
Push an update to Kubernetes secrets for djangoapp
```bash
djangoapp $  kubectl create -f kubernetes/secrets.yaml
```bash
# Push bitports secrets
bitport $  kubectl create -f kubernetes/secrets.yaml
```
## First Deploy
Run djangoapp's initial deploy to create the Rplication Controller and Service
```bash
djangoapp $  kubectl create -f kubernetes/api-prod.yaml
```

Redeploy using the following command
```bash
djangoapp $  deploy/rolling_update.sh
```

Create the database and the user on the Cloud server
```
kubectl get pods
kubectl exec -ti <POD_NAME> -c django bash
``
Now on the SQL Serve, log on the the SQL server_details

  ```bash
  mysql -uroot -h<CLOUD_SQL_IP_ADDRESS> -p
  # Run the following SQL script to initiate the database
  CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;
  GRANT ALL PRIVILEGES ON *.* TO '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';
  FLUSH PRIVILEGES;
  ```

## Run the migrations
```bash
kubectl exec -ti <POD_NAME> -c django -- bash -c "source load_env_vars.sh && python manage.py migrate"
```
