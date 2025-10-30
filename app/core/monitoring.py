from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter(
    "recommendation_requests_total",
    "Total de requisições de recomendação",
    ["strategy", "cache_hit"]
)

REQUEST_LATENCY = Histogram(
    "recommendation_request_latency_seconds",
    "Latência das requisições de recomendação",
    ["strategy"]
)
