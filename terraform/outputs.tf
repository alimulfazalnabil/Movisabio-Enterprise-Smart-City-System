output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "redis_hostname" {
  value = azurerm_redis_cache.redis.hostname
}

output "iot_hub_hostname" {
  value = azurerm_iothub.iothub.hostname
}
