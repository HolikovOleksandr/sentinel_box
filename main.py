from app.collectors import collect_basic_info, collect_network_info, collect_system_info


def main() -> None:
    basic_info = collect_basic_info()
    network_info = collect_network_info()
    system_info = collect_system_info()


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


if __name__ == "__main__":
    main()