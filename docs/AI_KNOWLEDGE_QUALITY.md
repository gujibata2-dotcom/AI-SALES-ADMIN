# Knowledge Quality & Decay

Quality dimensions: accuracy, completeness, consistency, freshness, provenance, relevance and uncertainty. Evidence quality also considers source quality, methodology, relevance, recency, independence, replication and consistency. Source count is never a quality proxy.

Knowledge carries `last_verified`, `review_interval` and optional expiry conditions. Aging moves knowledge to STALE or REVERIFY_REQUIRED rather than silently deleting it. Updates follow compare → validate → version → review → publish. If quality declines, rollback restores a previous version while retaining audit evidence.