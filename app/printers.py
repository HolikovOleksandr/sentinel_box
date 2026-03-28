from app.models import (
    BasicHostInfo,
    CheckResult,
    BoundPort,
    FirewallRule,
    FirewallStatus,
    NetworkInfo,
    ProcessConnectionSummary,
    SystemInfo,
    TcpConnection,
)


def print_basic_info(basic_info: BasicHostInfo) -> None:
    print("=== Basic host info ===")
    print(f"User: {basic_info.user}")
    print(f"Hostname: {basic_info.hostname}")
    print(f"Working directory: {basic_info.working_directory}")


def print_network_info(network_info: NetworkInfo) -> None:
    print("\n=== Network info ===")
    print(f"Default interface: {network_info.default_interface}")
    print(f"Local IPv4: {network_info.local_ip}")
    print(f"Default gateway: {network_info.default_gateway}")
    print(
        f"DNS servers: {', '.join(network_info.dns_servers) if network_info.dns_servers else 'None'}"
    )


def print_system_info(system_info: SystemInfo) -> None:
    print("\n=== System info ===")
    print(f"OS: {system_info.os_name}")
    print(f"OS version: {system_info.os_version}")
    print(f"Kernel version: {system_info.kernel_version}")
    print(f"Architecture: {system_info.architecture}")
    print(f"CPU cores: {system_info.cpu_count}")
    print(f"Total RAM (GB): {system_info.total_memory_gb}")


def print_check_result(check: CheckResult) -> None:
    status = "OK" if check.ok else "FAIL"
    print(f"[{status}] {check.details}")


def print_tcp_listening_ports(ports: list[BoundPort]) -> None:
    print("\n=== TCP listening ports ===")

    if not ports:
        print("No TCP listening ports found")
        return

    for port_info in sorted(ports, key=lambda port: (port.port, port.local_address)):
        bind_scope = _get_bind_scope(port_info.local_address)
        process_name = port_info.process_name or "unknown"

        print(
            f"- {port_info.local_address}:{port_info.port} "
            f"({bind_scope}, PID: {port_info.pid}, process: {process_name})"
        )


def print_udp_bound_ports(ports: list[BoundPort]) -> None:
    print("\n=== UDP bound ports ===")

    if not ports:
        print("No UDP bound ports found")
        return

    for port_info in sorted(ports, key=lambda port: (port.port, port.local_address)):
        bind_scope = _get_bind_scope(port_info.local_address)
        process_name = port_info.process_name or "unknown"

        print(
            f"- {port_info.local_address}:{port_info.port} "
            f"({bind_scope}, PID: {port_info.pid}, process: {process_name})"
        )


def print_exposed_tcp_ports(ports: list[BoundPort]) -> None:
    print("\n=== Exposed TCP ports ===")

    if not ports:
        print("No exposed TCP ports found")
        return

    for port_info in sorted(ports, key=lambda port: (port.port, port.local_address)):
        bind_scope = _get_bind_scope(port_info.local_address)
        process_name = port_info.process_name or "unknown"

        print(
            f"- {port_info.local_address}:{port_info.port} "
            f"({bind_scope}, PID: {port_info.pid}, process: {process_name})"
        )


def print_active_tcp_connections(connections: list[TcpConnection]) -> None:
    print("\n=== Active TCP connections ===")

    if not connections:
        print("No active TCP connections found")
        return

    for connection in sorted(
        connections,
        key=lambda item: (
            item.remote_address,
            item.remote_port,
            item.local_address,
            item.local_port,
        ),
    ):
        process_name = connection.process_name or "unknown"

        print(
            f"- {connection.local_address}:{connection.local_port} "
            f"-> {connection.remote_address}:{connection.remote_port} "
            f"({connection.status}, PID: {connection.pid}, process: {process_name})"
        )


def print_tcp_connection_summary(
    summary: list[ProcessConnectionSummary],
) -> None:
    print("\n=== Active TCP connections by process ===")

    if not summary:
        print("No active TCP connections found")
        return

    for item in summary:
        print(f"- {item.process_name}: {item.connection_count}")


def print_firewall_status(firewall_status: FirewallStatus) -> None:
    print("\n=== Firewall ===")
    print(f"Enabled: {'yes' if firewall_status.enabled else 'no'}")
    

def print_firewall_rules(rules: list[FirewallRule]) -> None:
    print("\n=== Firewall rules ===")

    if not rules:
        print("No firewall rules found")
        return

    for rule in sorted(rules, key=lambda item: (item.action, item.app_path.lower())):
        print(f"- {rule.action.upper()}: {rule.app_path}")


def _get_bind_scope(local_address: str) -> str:
    if local_address in {"127.0.0.1", "::1"}: return "local only"
    if local_address in {"0.0.0.0", "::"}: return "all interfaces"
    return "specific interface"