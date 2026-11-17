\# BeastEats Helm Deployment Guide



\## 1. Overview



BeastEats is deployed on Kubernetes using Helm. The Helm chart manages the application's Deployment and Service, while integrating with existing Kubernetes PersistentVolumeClaims and Secrets.



\*\*Chart:\*\* `beasteats-app`  

\*\*Release:\*\* `beasteats`  

\*\*Namespace:\*\* `beasteats-dev`  

\*\*Application image:\*\* `beasteats:1.0.0`  

\*\*Container port:\*\* `8000`



\## 2. Helm Chart Structure



```text

helm/

├── README.md

└── beasteats-app/

&#x20;   ├── Chart.yaml

&#x20;   ├── values.yaml

&#x20;   ├── values-dev.yaml

&#x20;   ├── values-prod.yaml

&#x20;   └── templates/

&#x20;       ├── deployment.yaml

&#x20;       ├── service.yaml

&#x20;       ├── pvc.yaml

&#x20;       ├── ingress.yaml

&#x20;       └── tests/

&#x20;           └── test-connection.yaml

```



\## 3. Configuration



\- `values.yaml`: Base configuration.

\- `values-dev.yaml`: Development overrides.

\- `values-prod.yaml`: Production-like configuration example.



The application uses an existing PVC named `beasteats-app-data`, mounted at `/app/instance`.



The application Secret is `beasteats-app-secret`, containing the `SECRET\_KEY` key.



Ingress is managed separately using Traefik in the current development environment.



\*\*Note:\*\* The production values file is a configuration example, not a production deployment. It must use environment-specific storage and Secrets before actual production use.



\## 4. Prerequisites



\- Kubernetes cluster

\- kubectl

\- Helm

\- Existing namespace `beasteats-dev`

\- Existing PVC `beasteats-app-data`

\- Existing Secret `beasteats-app-secret`

\- Application image available to the cluster



\## 5. Validate the Chart



```powershell

helm lint .\\helm\\beasteats-app

```



Render development manifests:



```powershell

helm template beasteats .\\helm\\beasteats-app `

&#x20; -n beasteats-dev `

&#x20; -f .\\helm\\beasteats-app\\values-dev.yaml

```



\## 6. Install the Application



```powershell

helm install beasteats .\\helm\\beasteats-app `

&#x20; -n beasteats-dev `

&#x20; -f .\\helm\\beasteats-app\\values-dev.yaml

```



For an existing release, use `helm upgrade` instead.



\## 7. Upgrade the Application



```powershell

helm upgrade beasteats .\\helm\\beasteats-app `

&#x20; -n beasteats-dev `

&#x20; -f .\\helm\\beasteats-app\\values-dev.yaml

```



\## 8. Inspect the Release



```powershell

helm status beasteats -n beasteats-dev

helm history beasteats -n beasteats-dev

helm get values beasteats -n beasteats-dev

```



\## 9. Rollback



Inspect revision history:



```powershell

helm history beasteats -n beasteats-dev

```



Rollback to a selected revision:



```powershell

helm rollback beasteats 3 -n beasteats-dev

```



Verify:



```powershell

helm status beasteats -n beasteats-dev

```



\## 10. Run Helm Tests



The chart includes a Helm test hook that creates a temporary BusyBox Pod and checks the application's health endpoint through the Kubernetes Service.



```powershell

helm test beasteats -n beasteats-dev

```



Expected result: test suite phase `Succeeded`.



\## 11. Kubernetes Verification



```powershell

kubectl get deployments,services,pods,pvc -n beasteats-dev

```



Check application logs:



```powershell

kubectl logs deployment/beasteats -n beasteats-dev

```



\## 12. Access the Application



The application is exposed through the Traefik Ingress.



Start a port-forward:



```powershell

kubectl port-forward service/traefik 8081:80 -n traefik

```



In another terminal:



```powershell

curl.exe -H "Host: app.beasteats.local" http://localhost:8081/health

```



Check the menu API:



```powershell

curl.exe -H "Host: app.beasteats.local" http://localhost:8081/api/menu

```



\## 13. Troubleshooting



```powershell

kubectl get pods -n beasteats-dev

kubectl describe pod <pod-name> -n beasteats-dev

kubectl logs <pod-name> -n beasteats-dev

kubectl get events -n beasteats-dev --sort-by=.metadata.creationTimestamp

helm status beasteats -n beasteats-dev

helm test beasteats -n beasteats-dev

```



\## 14. Current Deployment Status



The development deployment has been validated with:



\- Helm chart linting.

\- Development manifest rendering.

\- Kubernetes Deployment and Service.

\- Existing PVC integration.

\- Kubernetes Secret integration.

\- Traefik Ingress health endpoint.

\- Menu API verification.

\- Helm revision history and rollback.

\- Successful Helm automated test hook.



The application is running in the local KIND cluster.



