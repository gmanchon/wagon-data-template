
# usage

## Run project tests

``` bash
make pytest file=tests/conf
make pytest file=tests/code
make pytest file=tests/registry
```

## Run project trainer

``` bash
python -m project.app                   # run trainer
make run                                # run trainer
make run reg=True                       # run trainer with registry
```

## Run project prediction API locally

``` bash
make run_api
```

## Train on AI Platform

``` bash
. ./make_gcp_env.sh                     # create env variables once configured
make show_aipf_env                      # show ai platform env vars conf
make show_prod_env                      # show gcr and gke env vars conf
make show_gcp_conf                      # show gcp conf
```

## Create a prediction API container image and use it locally

build local image

``` bash
docker build --tag=test .
```

run local image

``` bash
docker run -e PORT=8000 -p 8000:8000 test
```

connect to http://localhost:8000/

``` bash
docker ps
```

``` bash
docker stop <container id>
docker kill <container id>
```

## Create a prediction API container image and deploy on Google Container Registry

enable [Google Container Registry API](https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com&redirect=https://cloud.google.com/container-registry/docs/quickstart
) for your project

login to gcp

``` bash
gcloud auth login
```

configure docker for gcp

``` bash
gcloud auth configure-docker
```

list your config

``` bash
gcloud config list
```

configure your project

``` bash
export PROJECT_ID=replace-with-gcloud-project-id
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
```

define a docker image name for your project

``` bash
export DOCKER_IMAGE_NAME=define-some-container-image-name
echo $DOCKER_IMAGE_NAME
```

build image

``` bash
docker build -t eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME .
```

make sure the image runs

``` bash
docker run -p 8000:8000 eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```

push image to Google Container Registry

``` bash
docker push eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```

## Deploy prediction API container image on Google Cloud Run

deploy on cloud run

``` bash
gcloud run deploy --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME --platform managed --region europe-west1
```

you should see the output

``` txt
Service name (wagon-data-tpl-image):
Allow unauthenticated invocations to [wagon-data-tpl-image] (y/N)?  y

Deploying container to Cloud Run service [wagon-data-tpl-image] in project [le-wagon-data] region [europe-west1]
✓ Deploying new service... Done.
  ✓ Creating Revision... Revision deployment finished. Waiting for health check to begin.
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.
Service [wagon-data-tpl-image] revision [wagon-data-tpl-image-00001-kup] has been deployed and is serving 100 percent of traffic.
Service URL: https://wagon-data-tpl-image-xi54eseqrq-ew.a.run.app
```

you are now able to browse to the deployed url and make a prediction using the API notebook for GCR

### Writing to GCS from GCR

Dockerfile

``` bash
COPY /path/to/your/credentials.json /credentials.json
```

``` bash
gcloud run deploy \
    --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME \
    --platform managed \
    --region europe-west1 \
    --GOOGLE_APPLICATION_CREDENTIALS="/credentials.json"
```

## Deploy prediction API container image on Google Kubernetes Engine

define a cluster name

``` bash
export CLUSTER_NAME=define-some-cluster-name
echo $CLUSTER_NAME
```

select a region from the [region list](https://cloud.google.com/compute/docs/regions-zones)

``` bash
gcloud container clusters create $CLUSTER_NAME --num-nodes 2 --region europe-west1
```

you should see the output

``` txt
Creating cluster wagon-data-tpl-cluster in europe-west1... Cluster is being health-checked (master is healthy)...done.
Created [https://container.googleapis.com/v1/projects/le-wagon-data/zones/europe-west1/clusters/wagon-data-tpl-cluster].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west1/wagon-data-tpl-cluster?project=le-wagon-data
kubeconfig entry generated for wagon-data-tpl-cluster.
NAME                    LOCATION      MASTER_VERSION   MASTER_IP     MACHINE_TYPE   NODE_VERSION     NUM_NODES  STATUS
wagon-data-tpl-cluster  europe-west1  1.16.13-gke.401  35.195.38.77  n1-standard-1  1.16.13-gke.401  6          RUNNING
```

you can [access the cluster](https://console.cloud.google.com/kubernetes/list?project=le-wagon-data)
and [inspect the content of the cluster](https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west1-c/wag-data-tpl-cluster?project=le-wagon-data)

the started instances are visible in [compute engine](https://console.cloud.google.com/compute/instances)

you can [delete the cluster](https://console.cloud.google.com/kubernetes/list) at anytime to stop it from running

optionally customize the parameters of the machine in a gke.yaml file

(replace ml-kube-deployment)

``` bash
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: ml-kube-deployment
  name: ml-kube-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ml-kube-deployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: ml-kube-deployment
    spec:
      containers:
      - image: gcr.io/$GCP_PROJECT_ID/ml-kube-deployment
        name: ml-kube-deployment
        resources:
          requests:
            memory: "4G"
status: {}
```

and apply the configuration

``` bash
echo gke.yaml | kubectl apply -f -
```

create deployment name

``` bash
export DEPLOYMENT_NAME=define-some-deployment-name
echo $DEPLOYMENT_NAME
```

copy full image name from

https://console.cloud.google.com/gcr/images/le-wagon-data/EU/wagon-data-tpl-image?project=le-wagon-data&gcrImageListsize=30

deploy docker image to the cluster

``` bash
kubectl create deployment $DEPLOYMENT_NAME --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME
```

``` bash
kubectl expose deployment $DEPLOYMENT_NAME --type=LoadBalancer --port 80 --target-port 5000
```

retrieve external ip address

```bash
kubectl get service --watch
```

``` txt
NAME                 TYPE           CLUSTER-IP       EXTERNAL-IP     PORT(S)        AGE
kubernetes           ClusterIP      10.111.240.1     <none>          443/TCP        19m
ml-kube-deployment   LoadBalancer   10.111.246.169   35.240.48.112   80:32076/TCP   48s
```

### Troubleshoot

``` bash
gcloud container clusters list
kubectl get pods
kubectl describe pod ml-kube-deployment-67556cccc5-6ldwx
```

look at messages in the events

## Delete Google Kubernetes Engine cluster once usage is done

delete the application on the cluster

```bash
kubectl delete deployment $DEPLOYMENT_NAME
```

delete the cluster

```bash
gcloud container clusters delete $CLUSTER_NAME --region europe-west1
```

# Create a budget alert

Go to Billing / Budgets & alerts
- CREATE BUDGET

or [follow the guide](https://cloud.google.com/billing/docs/how-to/budgets#add-new-budget)
