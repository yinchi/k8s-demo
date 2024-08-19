# PostgreSQL setup for MyApp

## Setup

To start, create folder `mnt/` in the `postgres` directory, then create `passwords.secret.yaml` to store your login details:

```yaml
apiVersion: v1
stringData:
  postgres_password: <admin password here>
  password: <password for myapp database here>
kind: Secret
metadata:
  name: postgres-passwords
  namespace: myapp
type: Opaque
```

## Initialisation

Follow the instructions in the top-level `README.md` to initialise the Kubernetes cluster, which will also create the necessary persistent volume and claim and start the `postgres` service in the `myapp` namespace.

## Testing the database connection

```console
$ kubectl port-forward -n myapp svc/postgres 5432:5432 &> /dev/null &
[1] 798193
$ psql -h localhost -p 5432 -U myapp
Password for user myapp: 
psql (16.3 (Ubuntu 16.3-0ubuntu0.24.04.1), server 16.4)
Type "help" for help.

myapp=> \conninfo
You are connected to database "myapp" as user "myapp" on host "localhost" (address "127.0.0.1") at port "5432".
myapp=> \q
```

