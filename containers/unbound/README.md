# Networking

Unbound and Pihole containers must be on the same network for unbound to work as intended.

Since docker creates a default network for Pihole called `pihole_default`, we can simply direct unbound to it as an external network.

```yaml 
networks:
  pihole_default:
    external: true
```