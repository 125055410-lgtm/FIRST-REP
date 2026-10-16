## Hipótesis del Proyecto

### Problema / Contexto
En entornos de red locales (LAN) con alto tráfico y dispositivos IoT heterogéneos, los picos de congestión y los escaneos no autorizados comprometen la latencia y la seguridad del sistema.

### Hipótesis
Creemos que al implementar un algoritmo de enrutamiento dinámico basado en priorización de tráfico (QoS) junto con un sistema de detección de anomalías en tiempo real sobre la red, lograremos mantener una baja latencia en servicios críticos y mitigar accesos no autorizados.

### Criterio de Validación
Sabremos que la hipótesis es correcta si, bajo una simulación de carga extrema y ataques de escaneo de puertos:
- La latencia en los paquetes de alta prioridad se mantiene por debajo de los **15 ms**.
- La tasa de pérdida de paquetes disminuye en un **40%** en comparación con el enrutamiento estándar.
- Se detectan y bloquean las conexiones sospechosas en menos de **2 segundos**.
