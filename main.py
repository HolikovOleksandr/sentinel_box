from app.checks import (
    check_default_gateway,
    check_gateway_reachable,
    check_internet_reachable,
    check_dns_resolution,
)
from app.collectors import (
    collect_basic_info,
    collect_firewall_rules,
    collect_firewall_status,
    collect_network_info,
    collect_system_info,
    collect_tcp_connection_summary,
    collect_tcp_listening_ports,
    collect_udp_bound_ports,
    collect_exposed_tcp_ports,
    collect_active_tcp_connections,
)
from app.printers import (
    print_basic_info,
    print_firewall_status,
    print_network_info,
    print_system_info,
    print_check_result,
    print_tcp_connection_summary,
    print_tcp_listening_ports,
    print_udp_bound_ports,
    print_exposed_tcp_ports,
    print_active_tcp_connections,
    print_firewall_rules,
)


def main() -> None:
    basic_info = collect_basic_info()
    network_info = collect_network_info()
    system_info = collect_system_info()
    tcp_listening_ports = collect_tcp_listening_ports()
    udp_bound_ports = collect_udp_bound_ports()
    exposed_tcp_ports = collect_exposed_tcp_ports(tcp_listening_ports)
    active_tcp_connections = collect_active_tcp_connections()
    tcp_connection_summary = collect_tcp_connection_summary(active_tcp_connections)
    firewall_status = collect_firewall_status()
    firewall_rules = collect_firewall_rules() if firewall_status.enabled else []

    gateway_check = check_default_gateway(network_info)
    gateway_reachable_check = check_gateway_reachable(network_info)
    internet_reachable_check = check_internet_reachable()
    dns_resolution_check = check_dns_resolution()

    print_basic_info(basic_info)
    print_system_info(system_info)
    print_network_info(network_info)
    print_firewall_status(firewall_status)

    if firewall_status.enabled:
        print_firewall_rules(firewall_rules)

    print("\n=== Checks ===")
    print_check_result(gateway_check)
    print_check_result(gateway_reachable_check)
    print_check_result(internet_reachable_check)
    print_check_result(dns_resolution_check)

    print_tcp_listening_ports(tcp_listening_ports)
    print_exposed_tcp_ports(exposed_tcp_ports)
    print_udp_bound_ports(udp_bound_ports)
    print_active_tcp_connections(active_tcp_connections)
    print_tcp_connection_summary(tcp_connection_summary)


if __name__ == "__main__":
    main()