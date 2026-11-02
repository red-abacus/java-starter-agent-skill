# Operations and Observability

Read when: Establishing reliability goals or alerting, or changing health, shutdown, resource sizing, scaling, placement, metrics, or tracing.

Use only the sections relevant to the task. [Handbook index](../java-spring-guidelines.md).

## Sections

- [Operations and observability](#operations-and-observability)
- [Reliability goals and alerting](#reliability-goals-and-alerting)
- [Health and availability](#health-and-availability)
- [Graceful shutdown](#graceful-shutdown)
- [Resource budgets and JVM sizing](#resource-budgets-and-jvm-sizing)
- [Replicas and autoscaling](#replicas-and-autoscaling)
- [Availability during maintenance and failures](#availability-during-maintenance-and-failures)
- [Metrics and tracing](#metrics-and-tracing)

## Operations and observability

### Reliability goals and alerting

Treat reliability goals and alerting as project-specific decisions. During project discovery, establish critical workflows and acceptable availability, response times, or processing delays. Scale the discussion to application maturity and introduce service-level objectives when useful, with targets based on user needs.

Agree concrete targets and alert configuration with the user during the affected operational implementation, reusing explicit project decisions. Define actionable alerts, their recipients, and the expected response. Reuse existing monitoring infrastructure where appropriate and document accepted limitations for a POC/MVP.

Health checks and metrics support these decisions; their presence does not establish reliability targets or an alerting policy. This kit does not prescribe a universal availability percentage, latency threshold, monitoring backend, or notification destination.

### Health and availability

Use Spring Boot Actuator health checks by default for new deployed applications. Expose an explicit, minimal set of management endpoints and configure access deliberately alongside SecurityFilterChain. Probe-accessible responses provide only required health information; additional diagnostic detail and management access are project decisions.

Distinguish overall health, liveness, and readiness. Overall health includes configured dependency indicators. Liveness concerns whether the application needs restarting and remains independent of databases and external providers. Choose readiness dependencies according to whether their failure prevents useful application traffic; a provider outage does not automatically make the whole instance unready.

When management uses a separate port, also make availability probes accessible on the application port so checks exercise its web infrastructure. Configure the relevant paths and access rules explicitly. Select probe timing and startup allowances for the deployment environment.

Use the [deployment defaults](delivery-gke.md#delivery-infrastructure) where no project requirement overrides them, and select specific readiness dependencies for the application. Verify actual probe responses, endpoint access, and dependency-failure behavior in the target application.

### Graceful shutdown

Use bounded graceful shutdown by default for deployed applications. Set `server.shutdown: graceful` explicitly and select `spring.lifecycle.timeout-per-shutdown-phase` for the application. Confirm that the container entry point delivers the termination signal to the application. Allow active HTTP requests to finish within the configured budget as the web server stops admitting new requests.

Coordinate application shutdown with GKE load-balancer draining and Kubernetes `terminationGracePeriodSeconds`. Budget for the applicable shutdown phases, any `preStop` hook, and a margin; the Spring timeout applies per phase, while Kubernetes enforces the Pod's overall termination grace period. Choose concrete durations and any draining hook for the actual routing and workload configuration rather than copying universal values.

Stop accepting new background work during shutdown. Finish, safely interrupt, or recover active tasks according to the workflow's agreed delivery requirements, configuring relevant schedulers, executors, and consumers explicitly. Graceful shutdown does not replace durable recovery for work that must survive termination.

Verify termination during active HTTP traffic and relevant background processing, including behavior when the budget expires. Test against the selected runtime and deployment setup before claiming rollout behavior works.

### Resource budgets and JVM sizing

Configure explicit CPU and memory requests and a memory limit through Helm values for each deployed application/environment. Choose CPU limits according to platform policy and workload behavior; do not automatically equate them with requests. Account for CPU throttling when validating startup and response times.

When using Paketo buildpacks, start with their container-aware memory calculator rather than adding competing heap flags. Budget for heap, metaspace, thread stacks, direct buffers, other native memory, and appropriate headroom. The Java heap must not consume the entire container memory budget. Preserve established sizing mechanisms in other image types unless a change is justified.

Select concrete allocations per project and validate startup, including migrations, and representative traffic. Adjust using observed memory consumption, garbage collection, CPU throttling, and latency. Provisional POC allocations should be documented and revisited as usage becomes known.

Keep the selected JVM's default garbage collector unless measurements justify a change. Introduce detailed JVM tuning to address demonstrated needs and verify its effect with the actual image and resource settings.

### Replicas and autoscaling

Choose scaling per application and environment. Start with fixed replicas for simple, predictable workloads and introduce Horizontal Pod Autoscaler (HPA) when variable demand justifies it. One replica is acceptable for development or cost-sensitive POCs where interruption is acceptable. For production APIs with availability requirements, start with at least two replicas and plan their distribution across appropriate nodes or zones.

When adopting HPA, explicitly select minimum/maximum replicas, meaningful metrics, and scaling behavior. Use CPU utilization when it reflects demand, with resource requests configured for utilization-based targets. Use workload metrics such as queue backlog or concurrency when they better represent capacity needs. Use scale-down stabilization to avoid repeatedly removing and recreating replicas; choose concrete settings during project development.

Budget database connections and downstream capacity across the maximum replica count, including rollout overlap. Verify that scheduled tasks, shared state, and background processing behave correctly with multiple replicas, and validate the selected scaling behavior under representative demand. Concrete replica counts and autoscaling settings belong to the target project.

### Availability during maintenance and failures

Use PodDisruptionBudgets (PDBs) and explicit replica placement for deployments with availability requirements. During implementation, discuss availability needs, disruption budgets, placement rules, and cluster capacity with the user before finalizing these settings. Reuse explicit project decisions already supplied; the general defaults do not settle the concrete configuration.

Align the PDB with minimum replicas and the capacity required to serve traffic. With two replicas, allowing one unavailable can be a starting point when the remaining replica can handle demand. PDBs constrain supported voluntary evictions, such as node drains; they cannot prevent unexpected node failures.

Spread replicas across nodes and add zone distribution when availability requirements and cluster topology justify it. Choose preferred versus strict topology spread deliberately: preferred spreading permits scheduling when ideal placement is unavailable, while strict constraints can leave Pods pending. Select rules that fit the project's actual capacity and availability requirements.

Verify node-drain behavior, replacement scheduling, and serving capacity with fewer healthy replicas. Keep these controls optional for single-replica POCs where interruption is acceptable.

### Metrics and tracing

Use Micrometer metrics by default. Start with framework instrumentation for HTTP requests, JVM resources, connection pools, and configured executors. Add business metrics for important workflow outcomes, processing durations, and pending work, measuring the outcomes they actually represent.

Keep metric tag values bounded, for example operation, provider, and outcome. Put identifier-level diagnostics in appropriate logs or traces under the existing logging policy. Keep management access under the adopted endpoint-access policy and select the monitoring backend and export configuration per project.

Add distributed tracing when operational needs justify it, preferring Micrometer Tracing with OpenTelemetry and OTLP. Preserve correlation between logs and ProblemDetail.traceId using the configured tracing/correlation context. Propagate context through HTTP clients built with Spring Boot's configured builders and across asynchronous boundaries.

Choose tracing backend, sampling, and export settings per project, with dependencies compatible with its Spring Boot version. Verify instrumentation, propagation, and configured export where those behaviors are required; adding logging annotations alone does not establish them.

## Primary references

Consult documentation matching the target project's versions when verifying framework behavior.

- [Google SRE: defining and refining service-level objectives](https://sre.google/workbook/implementing-slos/)
- [Spring Boot Actuator endpoints and availability probes](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html)
- [Spring Boot Micrometer metrics](https://docs.spring.io/spring-boot/reference/actuator/metrics.html)
- [Micrometer metric naming and tag values](https://docs.micrometer.io/micrometer/reference/concepts/naming.html)
- [Spring Boot Micrometer tracing](https://docs.spring.io/spring-boot/reference/actuator/tracing.html)
- [Spring Boot graceful shutdown](https://docs.spring.io/spring-boot/reference/web/graceful-shutdown.html)
- [GKE load-balancer draining and termination timing](https://docs.cloud.google.com/kubernetes-engine/docs/troubleshooting/load-balancing#customize_timeouts)
- [Kubernetes container resource requests and limits](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
- [Kubernetes Horizontal Pod Autoscaler](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/)
- [GKE Horizontal Pod Autoscaler](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/horizontalpodautoscaler)
- [Paketo Java memory calculator](https://paketo.io/docs/reference/java-reference/#memory-calculator)
- [Kubernetes disruptions and PodDisruptionBudgets](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)
- [Kubernetes Pod topology spread constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/)
