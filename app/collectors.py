import socket

from app.models import BasicHostInfo, NetworkInfo, SystemInfo, BoundPort
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
                pid=connection.pid,
                process_name=process_name,
            )
        )

    return bound_ports