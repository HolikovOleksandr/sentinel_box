from app.models import CheckResult, NetworkInfo
from app.shell_utils import run_command


def check_default_gateway(network_info: NetworkInfo) -> CheckResult:
    if network_info.default_gateway:
        return CheckResult(
            name="default_gateway_present",
            details=f"Default gateway found: {network_info.default_gateway}",
            ok=True,
        )

    return CheckResult(
        name="default_gateway_present",
        details="Default gateway not found",
        ok=False,
    )

def check_gateway_reachable(network_info: NetworkInfo) -> CheckResult:
    gateway = network_info.default_gateway

    if not gateway:
        return CheckResult(
            name="gateway_reachable",
            details="Cannot check gateway reachability: default gateway not found",
            ok=False,
        )
    
    ping_result = run_command(["ping", "-c", "1", gateway])

    if ping_result.returncode == 0:
        return CheckResult(
            name="gateway_reachable",
            details=f"Gateway is reachable: {gateway}",
            ok=True
        )
    
    return CheckResult(
        name="gateway_reachable",
        details=f"Gateway is not reachable: {gateway}",
        ok=False,
    )


def check_internet_reachable(target: str = '1.1.1.1') -> CheckResult:
    ping_result = run_command(['ping', '-c', '1', target])

    if ping_result.returncode == 0:
        return CheckResult(
            name='Internet reachable',
            details=f"Internet is reachable via {target}",
            ok=True,
        )
    
    return CheckResult(
        name="internet_reachable",
        details=f"Internet is not reachable via {target}",
        ok=False,
    )
