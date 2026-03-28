from dataclasses import dataclass


@dataclass
class CommandResult:
    ok: bool
    returncode: int | None
    stdout: str | None
    stderr: str | None


@dataclass
class BasicHostInfo:
    user: str
    hostname: str
    working_directory: str


@dataclass
class NetworkInfo:
    default_interface: str | None
    local_ip: str | None
    default_gateway: str | None
    dns_servers: list[str]


@dataclass
class SystemInfo:
    os_name: str
    os_version: str
    kernel_version: str
    architecture: str
    cpu_count: int | None
    total_memory_gb: float | None


@dataclass
class CheckResult:
    name: str
    ok: bool
    details: str


@dataclass
class ListeningPort:
    protocol: str
    local_address: str
    port: int
    pid: int | None
    process_name: str | None