from app.models import CheckResult, NetworkInfo


def check_default_gateway(network_info: NetworkInfo) -> CheckResult:
    if network_info.default_gateway:
        return CheckResult(
            name="default_gateway_present",
            ok=True,
            details=f"Default gateway found: {network_info.default_gateway}",
        )

    return CheckResult(
        name="default_gateway_present",
        ok=False,
        details="Default gateway not found",
    )