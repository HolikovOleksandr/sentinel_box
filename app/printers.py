from app.models import (
    BasicHostInfo,
    CheckResult,
    ListeningPort,
    NetworkInfo,
    SystemInfo,
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


def print_tcp_listening_ports(ports: list[ListeningPort]) -> None:
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


def _get_bind_scope(local_address: str) -> str:
    if local_address in {"127.0.0.1", "::1"}: return "local only"
    if local_address in {"0.0.0.0", "::"}: return "all interfaces"
    return "specific interface"