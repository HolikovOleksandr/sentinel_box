from result_model import CommandResult
import subprocess as sp


def run_command(command):
    try:
        result = sp.run(
            command, 
            capture_output=True, 
            text=True
        )

        return CommandResult(
            ok=result.returncode == 0,
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )

    except FileNotFoundError as err:
        return CommandResult(
            ok=False,
            returncode=None,
            stdout="",
            stderr=str(err),
        )