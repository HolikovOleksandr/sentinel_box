from app.models import CheckResult
from app.checks import (
    check_default_gateway, 
    check_gateway_reachable, 
    check_internet_reachable,
)
from app.collectors import (
    collect_basic_info,
    collect_network_info,
    collect_system_info,
)


def print_check_result(check: CheckResult) -> None:
    status = "OK" if check.ok else "FAIL"
    print(f"[{status}] {check.details}")

    
def main() -> None:
    basic_info = collect_basic_info()
    network_info = collect_network_info()
    system_info = collect_system_info()

    gateway_check = check_default_gateway(network_info)
    gateway_reachable_check = check_gateway_reachable(network_info)
    internet_reachable_check = check_internet_reachable()

    print("=== Basic host info ===")
    print(f"User: {basic_info.user}")
    print(f"Hostname: {basic_info.hostname}")
    print(f"Working directory: {basic_info.working_directory}")

    print("\n=== Network info ===")
    print(f"Default interface: {network_info.default_interface}")
    print(f"Local IPv4: {network_info.local_ip}")
    print(f"Default gateway: {network_info.default_gateway}")
    print(f"DNS servers: {', '.join(network_info.dns_servers) if network_info.dns_servers else 'None'}")

    print("\n=== System info ===")
    print(f"OS: {system_info.os_name}")
    print(f"OS version: {system_info.os_version}")
    print(f"Kernel version: {system_info.kernel_version}")
    print(f"Architecture: {system_info.architecture}")
    print(f"CPU cores: {system_info.cpu_count}")
    print(f"Total RAM (GB): {system_info.total_memory_gb}")

    print("\n=== Checks ===")
    print_check_result(gateway_check)
    print_check_result(gateway_reachable_check)
    print_check_result(internet_reachable_check)


if __name__ == "__main__":
    main()