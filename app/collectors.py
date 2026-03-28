import socket
from app.models import BasicHostInfo, FirewallRule, FirewallStatus, NetworkInfo, ProcessConnectionSummary, SystemInfo, BoundPort
from app.shell_utils import run_command
import platform
import psutil


def collect_network_info() -> NetworkInfo:
    route_resilt = run_command(["route", "-n", "get", "default"])
    resolv_result = run_command(["cat", "/etc/resolv.conf"])

    interface = None
    ip_v4 = None
    gateway = None
    dns_servers = []

    if route_resilt.returncode == 0:
        for line in route_resilt.stdout.splitlines():
            line = line.strip()
            
            if line.startswith('interface'):
                interface = line.split(':', 1)[1].strip()

            if line.startswith("gateway:"):
                gateway = line.split(":", 1)[1].strip()


    if resolv_result.returncode == 0:
        for line in resolv_result.stdout.splitlines():
            line = line.strip()

            if line.startswith("nameserver"):
                parts = line.split()

                if len(parts) >= 2:
                    dns_servers.append(parts[1])

    if interface:
        ip_result = run_command(["ipconfig", "getifaddr", interface])

        if ip_result.returncode == 0 and ip_result.stdout:
            ip_v4 = ip_result.stdout

    return NetworkInfo(
        default_interface=interface,
        default_gateway=gateway,
        dns_servers=dns_servers,
        local_ip=ip_v4,
    )


def collect_basic_info() -> BasicHostInfo:
    return BasicHostInfo(
        user=run_command(['whoami']).stdout.strip(),
        hostname=run_command(['hostname']).stdout.strip(),
        working_directory=run_command(['pwd']).stdout.strip(),
    )


def collect_system_info() -> SystemInfo:
    total_memory_bytes = psutil.virtual_memory().total
    total_memory_gb = round(total_memory_bytes / (1024 ** 3), 2)

    return SystemInfo(
        os_name=platform.system(),
        os_version=platform.mac_ver()[0] or platform.release(),
        kernel_version=platform.release(),
        architecture=platform.machine(),
        cpu_count=psutil.cpu_count(),
        total_memory_gb=total_memory_gb,
    )


def collect_tcp_listening_ports() -> list[BoundPort]:
    listening_ports = []

    try:
        connections = psutil.net_connections(kind="inet")
    except psutil.AccessDenied:
        print("Run app with sudo to see all listening ports")
        return listening_ports

    for connection in connections:
        if connection.status != "LISTEN": continue
        if not connection.laddr: continue

        try:
            process_name = (
                psutil.Process(connection.pid).name()
                if connection.pid is not None
                else None
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = None

        listening_ports.append(
            BoundPort(
                protocol="tcp",
                local_address=connection.laddr.ip,
                port=connection.laddr.port,
                pid=connection.pid,
                process_name=process_name,
            )
        )

    return listening_ports

def collect_udp_bound_ports() -> list[BoundPort]:
    bound_ports = []
    seen = set()

    try:
        connections = psutil.net_connections(kind="inet")
    except psutil.AccessDenied:
        print("Run app with sudo to see all UDP bound ports")
        return bound_ports

    for connection in connections:
        if connection.type != socket.SOCK_DGRAM: continue
        if not connection.laddr: continue
        if connection.laddr.port == 0: continue

        try:
            process_name = (
                psutil.Process(connection.pid).name()
                if connection.pid is not None
                else None
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = None

        key = (
            "udp",
            connection.laddr.ip,
            connection.laddr.port,
            connection.pid,
        )

        if key in seen: continue
        seen.add(key)

        bound_ports.append(
            BoundPort(
                protocol="udp",
                local_address=connection.laddr.ip,
                port=connection.laddr.port,
                process_name=process_name,
                pid=connection.pid,
            )
        )

    return bound_ports


def collect_exposed_tcp_ports(tcp_ports: list[BoundPort]) -> list[BoundPort]:
    exposed_ports = []

    for port_info in tcp_ports:
        if port_info.local_address in {"127.0.0.1", "::1"}: continue
        exposed_ports.append(port_info)

    return exposed_ports

import socket
import psutil

from app.models import TcpConnection


def collect_active_tcp_connections() -> list[TcpConnection]:
    tcp_connections = []
    seen = set()

    try:
        connections = psutil.net_connections(kind="inet")
    except psutil.AccessDenied:
        print("Run app with sudo to see all active TCP connections")
        return tcp_connections

    for connection in connections:
        if connection.type != socket.SOCK_STREAM: continue
        if connection.status == "LISTEN": continue
        if not connection.laddr or not connection.raddr: continue

        try:
            process_name = (
                psutil.Process(connection.pid).name()
                if connection.pid is not None
                else None
            )

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            process_name = None

        key = (
            connection.laddr.ip,
            connection.laddr.port,
            connection.raddr.ip,
            connection.raddr.port,
            connection.status,
            connection.pid,
        )

        if key in seen: continue
        seen.add(key)

        tcp_connections.append(
            TcpConnection(
                local_address=connection.laddr.ip,
                local_port=connection.laddr.port,
                remote_address=connection.raddr.ip,
                remote_port=connection.raddr.port,
                status=connection.status,
                pid=connection.pid,
                process_name=process_name,
            )
        )

    return tcp_connections


def collect_tcp_connection_summary(
    connections: list[TcpConnection],
) -> list[ProcessConnectionSummary]:
    summary = {}

    for connection in connections:
        process_name = connection.process_name or "unknown"

        if process_name not in summary: 
            summary[process_name] = 0

        summary[process_name] += 1

    result = []

    for process_name, connection_count in summary.items():
        result.append(
            ProcessConnectionSummary(
                process_name=process_name,
                connection_count=connection_count,
            )
        )

    return sorted(result, key=lambda item: (-item.connection_count, item.process_name))


def collect_firewall_status() -> FirewallStatus:
    result = run_command(
        ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--getglobalstate"]
    )

    if result.returncode != 0:
        return FirewallStatus(enabled=False)

    output = result.stdout.lower()

    if "firewall is enabled" in output:
        return FirewallStatus(enabled=True)

    if "firewall is disabled" in output:
        return FirewallStatus(enabled=False)

    return FirewallStatus(enabled=False)


def collect_firewall_rules() -> list[FirewallRule]:
    firewall_rules = []

    listapps_result = run_command(
        ["/usr/libexec/ApplicationFirewall/socketfilterfw", "--listapps"]
    )

    if listapps_result.returncode != 0 or not listapps_result.stdout:
        return firewall_rules

    app_paths = []

    for line in listapps_result.stdout.splitlines():
        line = line.strip()

        if not line: continue
        if line.startswith("ALF:"): continue

        app_paths.append(line)

    for app_path in app_paths:
        status_result = run_command(
            [
                "/usr/libexec/ApplicationFirewall/socketfilterfw",
                "--getappblocked",
                app_path,
            ]
        )

        if status_result.returncode != 0: continue
        output = status_result.stdout.lower()

        if "not blocked" in output: action = "allow"
        elif "blocked" in output: action = "block"
        else: action = "unknown"

        firewall_rules.append(FirewallRule(action=action, app_path=app_path))

    return firewall_rules