# Architecture

```{kroki}
:type: plantuml
:caption: Right-click -> "Open image in new tab"  to view full-size.

@startuml

cloud "Internet" as my_cloud {
  portout "            https" as cloud443
}

node Host {
  portin "           8000\n                            TLS termination" as host8000
  portin "9000" as host9000
node "kind Docker container" as kind {
 portin "          8000" as 8000
 portin "      9000" as 9000
 [Traefik]
 card "Module A" as svcA {
   [Frontend] as podA_Frontend
   [REST API] as podA_API
 }
 card "Module B" as svcB {
   [Integrated\nApp] as podB
 }
 card "Module C" as svcC {
   [Integrated\nApp] as podC
 }
 card Databases as db {
   [Database\nserver 0] as db0
   [Database\nserver 1] as db1
 }
}
}

cloud443 -- host8000 : " Public reverse proxy\n (e.g. ngrok)               \n\n"
host8000 -- 8000 : "(kubectl port-forward)\n"
host9000 -- 9000 : "(kubectl port-forward)\n"
8000 -- Traefik : " web"
9000 -- Traefik : "dashboard"

Traefik -- podA_Frontend : "HTTPRoute"
Traefik -- podA_API : "HTTPRoute"
Traefik -- podB : "HTTPRoute"
Traefik -- podC : "HTTPRoute"

podA_Frontend . podA_API

podA_API .. db0
podB .. db0
podB .. db1
podC .. db1

@enduml
```

The above figure shows the conceptual design of this demo app. For illustrative purposes, we show additional services and database servers in the figure (as opposed to one of each in the actual implemenation).  We implement a single-node Kubernetes cluster using `kind`, which runs within a Docker container on the host machine.

The Kubernetes Services of the demo app are shown in grey, with the Traefik service providing access to the internal services of the app using `HTTPRoute` objects for configuration.  The internal services of the app can communicate with each other directly using the `kind` node's built-in DNS service.