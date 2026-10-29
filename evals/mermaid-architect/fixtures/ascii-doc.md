# Request Path

A request enters through the load balancer, reaches the API, and the API reads from the database.

```text
+--------+     +---------------+     +-----+     +----------+
| Client | --> | Load balancer | --> | API | --> | Database |
+--------+     +---------------+     +-----+     +----------+
```

The load balancer spreads traffic across API instances.
