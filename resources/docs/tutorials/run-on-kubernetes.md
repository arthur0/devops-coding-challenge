# Setting up MultiVAC on Kubernetes 
<!-- TODO: Explain each one manifest -->
You only need apply [manifests](../../manifests/) \o/


### Deploy Mongo

```bash
kubectl apply -f mongo-service.yaml

# Using statefulset to persistent storage
kubectl apply -f mongostatefulset
```

### Deploy Redis

```bash
# Creating a secret
kubectl create secret generic multivac-secret --from-literal=password="isaacasimov" --from-literal=secret-key="foundation" 

# For all redis configuration see this doc:
# https://github.com/antirez/redis/blob/unstable/redis.conf
kubectl apply -f redis-settings-cm.yaml

kubectl apply -f redis-service.yaml

kubectl apply -f redis-deploy 
```


### Deploy MultiVAC
```bash
# Finding the Redis and Mongo endpoints
kubectl get svc -l app=multivac
NAME                  TYPE        CLUSTER-IP      [...]
multivac-mongo        ClusterIP   10.23.253.45    [...]
multivac-redis        ClusterIP   10.23.250.39    [...]

# You should adapt the multivac settings ConfigMap, to handle
# these endpoints by editing 'mongo_server' and 'redis_host' values.
# Then, you can create the ConfigMap.
kubectl apply -f multivac-settings-cm.yaml

# Finnaly, you can create the MultiVAC Deployment and Service
kubectl apply -f multivac-service.yaml
kubectl apply -f multivac-deploy.yaml
```

### Testing Multivac
```bash
# --> Use label selectors!

# Get all Multivac related resources (including db and cache)
kubectl get all -l=app=multivac
# Get all Multivac db (mongo) related resources
kubectl get all -l=app=multivac,role=db
# Get all Multivac cache (redis) related resources
kubectl get all -l=app=multivac,role=cache
# Get all Multivac web-server (flask) related resources
kubectl get all -l=app=multivac,role=web-server

# --> Logging: Use label selectors!
kubectl logs -l=app=multivac 

# --> Perform requests
# Util tool
kubectl run dnstools --image=radial/busyboxplus:curl -i --tty
> curl multivac-web-server:5000
Welcome to Multivac!

> curl multivac-web-server:5000
INSUFFICIENT DATA FOR MEANINGFUL ANSWER.

>  curl -X POST -F 'data=fiat lux' multivac-web-server:5000/multivac/data
{"response": "MultiVAC updated!"}

> curl multivac-web-server:5000/multivac
INSUFFICIENT DATA FOR MEANINGFUL ANSWER.
> curl multivac-web-server:5000/multivac
INSUFFICIENT DATA FOR MEANINGFUL ANSWER.
# [...] Ctrl+D

# Revert the entropy process is hard, takes a long time
# So, the MultiVAC worker job role is is to advance it.
# It's a kind of time machine.
kubectl apply -f multivac-worker-job.yaml

# Testing again
kubectl attach <your dns tools pod> -c dnstools -i -t

# \o/
> curl multivac-web-server:5000/multivac
fiat lux
```

Next steps
* Vault as the Secret manager
* Use a reverse proxy system (Envoy, NGINX) to expose our MultiVAC to world
  * It's already possible by using a service with `LoadBalacer` type (but)
    * `kubectl expose svc multivac-web-server --type=LoadBalancer`
  * Flask’s built-in server is not suitable for production [link](http://flask.pocoo.org/docs/1.0/deploying/)
* Use a cronjob for our time machine 
* Review and improve the all docs

<!-- 
> Mongo Tutorial https://lakshminp.com/docker-mongodb 

> Mongo reference: https://github.com/docker-library/mongo/tree/master/4.0

> Redis Related issue: https://github.com/docker-library/redis/issues/46 -->
