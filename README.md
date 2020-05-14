# Image-to-Image-Translation-Experiments-with-GANs

This repository contains all the code that is used to create the demo for the Cloud and ML final project. The entire application is packaged into a docker image that is available at `sudo007/cml_project2:latest`.

Steps to deploy and run the application on Kubernetes:
1. Start a new cluster on IBM cloud and set up ibm cloud cli tools and set the config of kubctl to ibm cloud cluster.
2. Download the `deployment.yaml` file from this repository
3. Run `kubectl apply -f deployment.yaml`. You should see an output like this:
```
sudarshinityagi$ kubectl apply -f deployment.yaml
deployment.apps/cml-project-deployment created
service/cml-project-service created
```
4. Now we need to find the external IP address on which the service is running, to do that run kubectl get nodes -o yaml | grep external-ip and you will see an output like this:
```
sudarshinityagi$ kubectl get nodes -o yaml | grep external-ip
      ibm-cloud.kubernetes.io/external-ip: 50.23.5.147
```
This is the address that we can access from anywhere to see if the app is running. We also need a port, to find that, run `kubectl describe services test-mnist-service`, the output will be something like this:
```
sudarshinityagi$ kubectl describe services test-mnist-service
Name:                     test-mnist-service
Namespace:                default
Labels:                   <none>
Annotations:              Selector:  app=inference-app
Type:                     NodePort
IP:                       172.21.207.206
Port:                     <unset>  8001/TCP
TargetPort:               8001/TCP
NodePort:                 <unset>  31000/TCP
Endpoints:                172.30.104.143:8001,172.30.104.144:8001
Session Affinity:         None
External Traffic Policy:  Cluster
Events:                   <none>
```
The port against Nodeport is what you're looking for. Therefore, our application is running at `http://50.23.5.147:31000`. Replace the external IP and port according to your outputs.
5. That's it, go to your browser and hit the URL, you should see something like this:
![alt text](https://github.com/SudarshiniTyagi/Image-to-Image-Translation-Experiments-with-GANs/blob/master/demo.jpeg?raw=true)
