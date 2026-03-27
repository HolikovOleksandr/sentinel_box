from app.models import CommandResult
import subprocess


def run_command(command) -> CommandResult:
    try:
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True
        )

        return CommandResult(
            ok=result.returncode == 0,
            returncode=result.returncode,
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
        )

    except FileNotFoundError as err:
        return CommandResult(
            ok=False,
            returncode=None,
            stdout=None,
            stderr=str(err).strip(),
        )