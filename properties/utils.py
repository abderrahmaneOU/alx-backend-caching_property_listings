from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    cached_properties = cache.get('all_properties')
    if cached_properties:
        return cached_properties
    properties = Property.objects.all()
    cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

def get_redis_cache_metrics():
    con = get_redis_connection("default")
    info = con.info("stats")
    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    hit_ratio = hits / (hits + misses) if (hits + misses) > 0 else 0
    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": hit_ratio
    }
    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics
