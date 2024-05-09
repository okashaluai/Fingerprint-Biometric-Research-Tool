import subprocess
import os
from Dev.DTOs import Response

absolute_path = os.path.dirname(__file__)


def mindtct(file_in: str, file_out: str) -> Response:
    mindtct_path = os.path.join(absolute_path, "mindtct")
    argv1 = f'"{file_in}"'
    argv2 = f'"{file_out}"'
    arguments = f"-m1 {argv1} {argv2}"

    try:
        exe_process = subprocess.Popen(
            f"{mindtct_path} {arguments}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        exe_process.wait()

        stdout, stderr = exe_process.communicate()

        return Response(success=False, data=None,
                        error=None if not stderr else f"Error running mindtct: {stderr.decode('utf-8')}")

    except Exception as e:
        # print(f"Exception occurred while running mindtct: {e}")
        return Response(success=False, data=None, error=e)


response = mindtct("/home/yazan/Desktop/NBIS/Main/bin/1.jpeg", "/home/yazan/Desktop/x")

print(response.success)
print(response.data)
print(response.error)
