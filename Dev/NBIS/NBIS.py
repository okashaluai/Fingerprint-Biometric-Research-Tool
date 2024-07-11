import os
import platform
import subprocess
from enum import Enum


class LibName(Enum):
    MINDTCT: str = "mindtct"
    NFIQ: str = "nfiq"
    BOZORTH3: str = "bozorth3"


def get_exe_lib_path(lib_name: LibName) -> str:
    absolute_path = os.path.dirname(__file__)

    # Windows 64 bit
    if os.name.startswith('nt'):
        full_path = os.path.join(absolute_path, "Windows", f"{lib_name.value}.exe")
    # Linux - Linux 64 bit
    elif platform.system() == 'Linux':
        full_path = os.path.join(absolute_path, "Linux", lib_name.value)
    else:
        raise Exception("System/Platform not supported!")

    return full_path


def detect_minutiae(images_dir_path: str, templates_dir_path: str) -> None:
    images_files_paths = os.listdir(images_dir_path)
    for image_file in images_files_paths:
        if not image_file.lower().endswith('.png'):
            raise Exception('Image file should have .png extension!')

        image_file_name = os.path.splitext(os.path.basename(image_file))[0]
        template_file_path = os.path.abspath(os.path.join(templates_dir_path, image_file_name))
        image_file_path = os.path.abspath(os.path.join(images_dir_path, image_file))
        run_process(get_exe_lib_path(LibName.MINDTCT), f'"{image_file_path}" "{template_file_path}"')

    # Keep only .min and .xyt files
    for template_file in os.listdir(templates_dir_path):
        if not (template_file.lower().endswith('.min') or template_file.lower().endswith('.xyt')):
            os.remove(os.path.join(templates_dir_path, template_file))


def match_templates(first_xyt_template_path, second_xyt_template_path) -> int:
    first_xyt_template_path = f'"{first_xyt_template_path}"'
    second_xyt_template_path = f'"{second_xyt_template_path}"'
    stdout = run_process(get_exe_lib_path(LibName.BOZORTH3), f"{first_xyt_template_path} {second_xyt_template_path}")

    # Parse the output to extract the matching score
    score_line = stdout.strip().split('\n')[-1]
    score = int(score_line.split()[0])
    return score


def get_image_quality(image_path: str) -> int:
    stdout = run_process(get_exe_lib_path(LibName.NFIQ), image_path)

    # Parse the output to extract the image quality
    image_quality_line = stdout.strip().split('\n')[-1]
    image_quality = int(image_quality_line.split()[0])
    return image_quality


def run_process(exe_lib_path: str, arguments: str) -> str:
    # Give the lib an execution permission
    # TODO: this command corrupts NBIS executables on Windows.
    # if not os.access(exe_lib_path, mode=os.X_OK):
    #     os.chmod(exe_lib_path, mode=stat.S_IRWXU + stat.S_IRWXG + stat.S_IROTH + stat.S_IXOTH)

    # Execute lib
    print(arguments)
    completed_process = subprocess.run(
        args=f'"{exe_lib_path}" {arguments}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        universal_newlines=True
    )

    if completed_process.stderr:
        print(completed_process.stderr)
        raise Exception(completed_process.stderr)
    return completed_process.stdout
