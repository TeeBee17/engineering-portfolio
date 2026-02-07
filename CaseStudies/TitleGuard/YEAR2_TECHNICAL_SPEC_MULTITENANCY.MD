This specification outlines the transition of the TitleGuard platform from a single-region deployment to a **Global Multi-Tenant SaaS** architecture. This is a critical milestone for Year 2, focusing on data sovereignty, cost-efficiency, and rapid market entry.



---

# Technical Specification: Multi-Tenant SaaS Architecture (Year 2)

## Document Version: 1.0.0

## Component: Cross-Border Tenant Orchestration

### 1. Executive Summary

To scale TitleGuard across various emerging markets, the architecture must support multiple "Tenants" (e.g., different countries or independent real estate boards) on a shared infrastructure while ensuring strict data isolation, localized compliance, and regional residency.

### 2. Isolation Strategy: "Siloed Schema" Model

We utilize a **Bridge Pattern** for database isolation. While the application code is shared, each tenant (Country/Region) is assigned a dedicated PostgreSQL schema.

#### Why this model?

* **Security:** Prevents accidental data leakage between different countries' registries.
* **Compliance:** Facilitates "Data Residency" requirements where certain countries mandate that land records must not leave national borders.
* **Performance:** Allows for tenant-specific indexing and PostGIS tuning without affecting the global platform.

### 3. High-Level System Components

* **Tenant Context Dispatcher:** A middleware layer in FastAPI that identifies the tenant based on the request (e.g., `ng.titleguard.io` vs `gh.titleguard.io`) and routes the database connection to the correct schema.
* **Global Auth & IAM:** A centralized identity service (using OAuth2/JWT) that manages user permissions across all tenants while restricting data access based on the tenant ID.
* **Localized Logic Engine:** A set of strategy-pattern modules that swap out "Legal Rules" or "Tax Calculations" based on the active tenant's jurisdiction.

### 4. Implementation Logic: Tenant Routing

```python
from fastapi import Request, Depends
from sqlalchemy import create_engine

def get_db_schema(request: Request):
    # Extract tenant ID from subdomain or header
    tenant_id = request.headers.get("X-Tenant-ID") 
    
    # Dynamically set the search path to the tenant's private schema
    engine = create_engine(DATABASE_URL, connect_args={"options": f"-c search_path={tenant_id},public"})
    return engine

@app.get("/property/{id}")
async def get_property(id: str, db=Depends(get_db_schema)):
    # All queries are now scoped to the tenant's specific PostGIS schema
    return db.query(Property).filter(Property.id == id).first()

```

### 5. Strategic Trade-offs

* **Shared vs. Isolated Infrastructure:** We opted for a shared application layer to reduce operational overhead (CI/CD simplicity) but kept isolated schemas to mitigate the risk of a "noisy neighbor" impacting global system stability.
* **Statelessness:** The API remains strictly stateless; tenant context is provided in every request, allowing the system to scale horizontally across multiple cloud availability zones.

---

### Why this document helps land a Principal role:

This specification serves as a IaaBE (**Infrastructure as a Business Enabler.**) The system allows us to launch in a new country in days rather than months.

