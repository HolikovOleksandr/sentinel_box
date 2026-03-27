from dataclasses import dataclass

@dataclass
class CommandResult:
    ok: bool
    returncode: int | None
    stdout: str
    stderr: str
