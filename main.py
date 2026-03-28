from app.checks import (
    check_default_gateway,
    check_gateway_reachable,
    check_internet_reachable,
    check_dns_resolution,
)
from app.collectors import (
    collect_basic_info,
    collect_network_info,
    collect_system_info,
    collect_tcp_listening_ports,
)
from app.printers import (
    print_basic_info,
    print_network_info,
    print_system_info,
    print_check_result,
    print_tcp_listening_ports,
)


def main() -> None:
    basic_info = collect_basic_info()
    network_info = collect_network_info()
    system_info = collect_system_info()
    tcp_listening_ports = collect_tcp_listening_ports()

    gateway_check = check_default_gateway(network_info)
    gateway_reachable_check = check_gateway_reachable(network_info)
    internet_reachable_check = check_internet_reachable()
    dns_resolution_check = check_dns_resolution()

    print_basic_info(basic_info)
    print_network_info(network_info)
    print_system_info(system_info)

    print("\n=== Checks ===")
    print_check_result(gateway_check)
    print_check_result(gateway_reachable_check)
    print_check_result(internet_reachable_check)
    print_check_result(dns_resolution_check)
    print_tcp_listening_ports(tcp_listening_ports)


if __name__ == "__main__":
    main()