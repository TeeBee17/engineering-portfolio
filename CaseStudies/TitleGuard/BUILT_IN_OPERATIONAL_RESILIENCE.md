
---

# Operational Resilience: Maintaining High Availability 
## Ensuring Business Continuity During External Dependency Failure

**Scenario:** Total Government Registry Outage (48+ Hours)

## 1. The Incident

In many emerging markets, government digital portals can experience catastrophic downtime due to maintenance, infrastructure failure, or cyberattacks. For most property tech, this results in a **total service blackout**.

## 2. The TitleGuard Resilience Strategy

TitleGuard is engineered with a **"Degraded Graceful Operation"** philosophy. We treat external dependencies as inherently unreliable.

### A. The Circuit Breaker Pattern

When the **Legacy Adapter** detects a 100% failure rate or a response latency exceeding 60 seconds from the government portal, it "trips" the circuit.

* **Action:** The system stops attempting to hit the live government portal to prevent worker pool exhaustion.
* **User Impact:** Instead of a "Request Timeout," the user is immediately informed: *"Live verification is currently unavailable. Viewing the most recent cached record (Ver. 2025-02-05)."*

### B. Intelligent Stale-Cache Serving

While the "Live" link is down, TitleGuard leverages its **PostGIS-backed local replica**.

* **Heuristics:** If a property was verified within the last 30 days, we serve the cached report with a prominent "Stale Data Warning."
* **Reliability:** In real estate, ownership rarely changes hour-by-hour. Serving a 48-hour-old record is 95% more useful than serving an error page.

### C. The Queue-and-Retry Mechanism

For new queries (properties not in the cache), TitleGuard does not fail.

* **Action:** The request is placed in a **Durable Redis Queue**.
* **The "Self-Healing" Loop:** The system polls the government portal with a single "sentinel" request every 5 minutes. As soon as the portal returns a `200 OK`, the circuit is reset, and the queue of pending verifications is processed automatically.

---

## 3. Technical Implementation: The Sentinel & Circuit Breaker

```python
# Conceptual implementation of the Resilience Handler
def fetch_title_data(property_id):
    if circuit_breaker.is_open():
        # Fallback to PostGIS cache immediately
        return get_local_cache(property_id), "CACHED_OFFLINE"

    try:
        data = call_government_portal(property_id)
        circuit_breaker.record_success()
        update_local_cache(property_id, data)
        return data, "LIVE"
    except (Timeout, ConnectionError):
        circuit_breaker.record_failure()
        return get_local_cache(property_id), "STALE_FALLBACK"

```

## 4. Business Impact

* **Brand Trust:** Banks and legal firms can continue their preliminary due diligence without interruption.
* **Operational Efficiency:** Engineers aren't waking up at 3 AM to "fix" a government-side outage; the system self-heals as soon as the dependency recovers.
* **Data Moat:** Over time, TitleGuard's cache becomes a secondary "Shadow Registry," increasing the platform's intrinsic value independent of the government's uptime.

---


