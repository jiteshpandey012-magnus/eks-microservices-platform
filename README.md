# Production-Style Microservices Platform on Kubernetes

A cloud-hosted microservices platform demonstrating containerization, Kubernetes orchestration, CI/CD automation, service discovery, persistent storage, and application deployment on Oracle Cloud Infrastructure (OCI).

The project is being developed incrementally, starting with a working Flask-based User Service backed by MySQL and exposed through NGINX Ingress.

## Architecture

```text
                 Developer
                     |
                     v
               GitHub Repository
                     |
                     v
              GitHub Actions
              Build ARM64 Image
                     |
                     v
                 OCI OCIR
                     |
                     v
        OCI-hosted Kubernetes Cluster
        +---------------------------+
        |                           |
        |  NGINX Ingress Controller |
        |             |             |
        |             v             |
        |       User Service        |
        |        Flask API          |
        |             |             |
        |             v             |
        |       MySQL Service       |
        |             |             |
        |             v             |
        |    50 GiB Persistent      |
        |    OCI Block Volume       |
        +---------------------------+
```

## Technology Stack

| Category           | Technologies                                      |
| ------------------ | ------------------------------------------------- |
| Cloud              | Oracle Cloud Infrastructure (OCI)                 |
| Containerization   | Docker                                            |
| Orchestration      | Kubernetes                                        |
| Container Registry | OCI Container Registry (OCIR)                     |
| CI/CD              | GitHub Actions                                    |
| Ingress            | NGINX Ingress Controller                          |
| Backend            | Python, Flask, Gunicorn                           |
| Database           | MySQL 8.0                                         |
| Storage            | Kubernetes PVC, OCI Block Volume CSI              |
| Networking         | VCN, subnets, security lists, Kubernetes Services |
| Version Control    | Git, GitHub                                       |
| Operating System   | Ubuntu Linux                                      |

## Implemented Components

### User Service

A containerized Flask application deployed to Kubernetes.

Current API endpoints:

| Endpoint  | Purpose                                                 |
| --------- | ------------------------------------------------------- |
| `/`       | Service information                                     |
| `/health` | Application health check                                |
| `/db`     | Verify database connectivity and retrieve MySQL version |

The service uses Kubernetes readiness and liveness probes and retrieves database credentials through Kubernetes Secrets.

### MySQL Database

MySQL runs as a Kubernetes Deployment and is exposed internally through a ClusterIP Service.

Persistent storage is provided by a 50 GiB PersistentVolumeClaim using the `oci-bv` StorageClass backed by OCI Block Volume storage.

Database credentials are supplied through a Kubernetes Secret and are not intended to be stored in Git.

### NGINX Ingress

The NGINX Ingress Controller routes HTTP requests to the User Service.

The current environment exposes the controller through a NodePort. The externally reachable port depends on the cluster's current networking configuration.

### Automated Image Build

A GitHub Actions workflow builds the User Service container image for ARM64 and pushes it to OCI Container Registry (OCIR).

The Kubernetes Deployment pulls the private image using an image pull Secret.

## Cloud Infrastructure

The current environment includes:

* An OCI VCN with public and private subnets.
* A Kubernetes control-plane node and a worker node.
* Calico networking for pod communication.
* NGINX Ingress Controller for HTTP routing.
* OCI Block Volume persistent storage for MySQL.
* OCI Container Registry for application images.

## Repository Structure

```text
eks-microservices-platform/
├── .github/
│   └── workflows/
│       └── build-user-service.yml
├── docs/
├── frontend/
├── ingress/
│   └── user-service-ingress.yaml
├── inventory-service/
├── mysql/
│   └── k8s/
│       └── resources.yaml
├── monitoring/
├── order-service/
├── payment-service/
├── product-service/
├── scripts/
├── user-service/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── k8s/
│       └── deployment.yaml
├── .gitignore
├── LICENSE
└── README.md
```

Some directories are reserved for future implementation. The currently verified application path is the User Service and MySQL.

## API Verification

The current test environment exposes the User Service through the following base URL:

`http://92.4.93.219:32541`

| Test                  | URL path  | Expected result                              |
| --------------------- | --------- | -------------------------------------------- |
| Service information   | `/`       | Service status response                      |
| Health check          | `/health` | `{"status":"UP"}`                            |
| Database connectivity | `/db`     | Database connection status and MySQL version |

These endpoints have been tested successfully in the current environment.

**Note:** The IP address and NodePort are environment-specific and may change. The endpoints currently use HTTP and should not be treated as a production-secure public API.

## Deployment Manifests

The repository contains Kubernetes manifests for:

* User Service Deployment and Service.
* MySQL Deployment and Service.
* MySQL PersistentVolumeClaim.
* NGINX Ingress routing.

The manifests reference existing Kubernetes Secrets for sensitive values. Create the required Secrets and registry credentials securely before deploying to another cluster.

Example verification commands:

```bash
kubectl get nodes
kubectl get deployments,services,pods
kubectl get pvc
kubectl get ingress
```

## Security Considerations

* Do not commit database passwords, registry tokens, or Kubernetes Secret manifests containing credentials.
* Use least-privilege OCI network rules.
* Restrict public NodePort access to authorized sources where possible.
* Configure HTTPS and TLS before exposing the application for production use.
* Back up MySQL data and test restoration procedures.
* Treat this as a learning and portfolio environment until production security, resilience, monitoring, and recovery requirements have been implemented and validated.

## Roadmap

* [x] Deploy Kubernetes control-plane and worker nodes.
* [x] Configure Calico pod networking.
* [x] Deploy MySQL with persistent OCI block storage.
* [x] Deploy the Flask User Service.
* [x] Configure NGINX Ingress and public HTTP access.
* [x] Build and push the User Service image through GitHub Actions.
* [x] Store Kubernetes deployment manifests in Git.
* [ ] Complete repository documentation and deployment instructions.
* [ ] Implement and integrate Product, Inventory, Order, and Payment services.
* [ ] Add monitoring and observability.
* [ ] Implement and test database backup and recovery.
* [ ] Configure HTTPS and review cluster security.
* [ ] Add automated application and deployment tests.

## Author

**Jitesh Pandey**

GitHub: [jiteshpandey012-magnus](https://github.com/jiteshpandey012-magnus)

Project: [eks-microservices-platform](https://github.com/jiteshpandey012-magnus/eks-microservices-platform)
