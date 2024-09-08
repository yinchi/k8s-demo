# Database setup

To set up a database server, first create a mount definition in `kind.yaml`.  This allows a persistent volume in the Kubernetes cluster to be linked to a directory on the host machine. An example has been provided in `kind.yaml`:

```yaml
extraMounts:
  # Add a mount for every persistent volume required
  - hostPath: /home/yinchi/k8s-db-test/mnt/postgres0
    containerPath: /myapp/postgres0
```

Next, install the Helm charts required for creating the database service and associated Kubernetes resources, for example by editing and running the `init.sh` initialisation script.  Currently, we instantiate one PostgreSQL instance:

```bash
# Secret for passwords, PersistentVolume and PersistentVolumeClaim
helm upgrade -i postgres0-additional \
   ./charts/postgres-additional \
  -n myapp \
  --values values/postgres0/pvc.yaml --values values/postgres0/secret.yaml

# Public chart for the PostgreSQL service, using the additional resources defined above
helm upgrade -i postgres0 \
  oci://registry-1.docker.io/bitnamicharts/postgresql \
  -n myapp \
  --values values/postgres0/main.yaml \
  --wait --timeout 60s
```

See also: [](helm.md)

```{note}
The Bitnami Postgres [Helm chart](https://artifacthub.io/packages/helm/bitnami/postgresql) used in this demo includes a default database and user, in our case, these are both called `myapp`.  In other use cases, one may wish to execute their own startup SQL scripts before launching the corresponding API services.

This is especially important in a production setting where there may be multiple database roles and permission settings that need to be set explicitly.  For example, see the [PostgreSQL documentation](https://www.postgresql.org/docs/current/sql-commands.html) for `CREATE USER` and `GRANT`.
```

## Database administration

Database administration tools should be installed **outside** of the Kubernetes cluster.  Use `kubectl port-forward` to expose ports as necessary.  Recommended database administration tools include:

- [pgadmin4](https://snapcraft.io/pgadmin4) for PostgreSQL
- [Mongo Express](https://hub.docker.com/_/mongo-express/)
- [SQLite Browser](https://snapcraft.io/sqlitebrowser)
- [Beekeeper Studio](https://snapcraft.io/beekeeper-studio) (multi-dialect)
- [dbGate](https://dbgate.org/download-community/) (multi-dialect)

## Direct database server access

In addition to `kubectl port-forward`, one can also connect to each database server directly using `kubectl exec`.  For example:

```console
$ alias k
alias k='kubectl'
$ cat test.sql
\dt;
select * from public.testmodel;
$ k cp ./test.sql postgres0-0:/tmp/test.sql
Defaulted container "postgresql" out of: postgresql, init-chmod-data (init)
$ k exec -it postgres0-0 -- psql -U myapp -f "/tmp/test.sql"
Defaulted container "postgresql" out of: postgresql, init-chmod-data (init)
Password for user myapp:
         List of relations
 Schema |   Name    | Type  | Owner
--------+-----------+-------+-------
 public | testmodel | table | myapp
(1 row)

 id | data1 |   data2
----+-------+------------
  1 | one   | two
  2 | text  | string
  5 | port  | forwarding
  4 | aaaaa | bbbbb
(4 rows)
```