# Resource_constrained_observability_stackdevops-assignment/

```
├── README.md
├── PERFORMANCE_REPORT.md
├── WALKTHROUGH.md               # (Optional: notes for your video script)
│
├── sensor-service/
│   ├── sensor.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── configs/
│   │   └── logging.conf
│   └── tests/
│       ├── test_metrics.py
│       └── test_healthcheck.py
│
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   ├── victoria-metrics/
│   │   ├── vm-single-config.yaml   # (if using VictoriaMetrics)
│   ├── grafana/
│   │   ├── dashboards/
│   │   │   └── sensor-dashboard.json
│   │   └── provisioning/
│   │       ├── dashboards/
│   │       └── datasources/
│   │           └── datasource.yml
│
├── docker-compose.yml
│
├── scripts/
│   ├── profile_cpu.sh              # py-spy, cpu flamegraph
│   ├── load_test.sh                # ab/hey test scripts
│   └── debug_metrics.sh            # curl metrics health check
│
├── diagrams/
│   ├── architecture.png
│   └── pipeline-flow.png
│
└── .github/
    └── workflows/
        ├── ci.yml                  # Lint, tests, build image
        └── security.yml            # Basic static checks
```