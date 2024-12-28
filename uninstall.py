import platform
import shutil
import os



def uninstall():
    print("Starting uninstallation...")

    # Determine global installation path
    system = platform.system()
    if system == "Windows":
        install_path = os.path.join(os.getenv("APPDATA"), "ospdf")
    else:
        install_path = "/usr/local/bin"

    # Path to the executable
    exec_path = os.path.join(install_path, "ospdf")

    # Remove the executable
    if os.path.exists(exec_path):
        os.remove(exec_path)
        print(f"Removed executable: {exec_path}")
    else:
        print("Executable not found. Nothing to uninstall.")

    # Clean up build files
    temp_dirs = ["build", "dist", "__pycache__"]
    for temp in temp_dirs:
        if os.path.exists(temp):
            shutil.rmtree(temp)
            print(f"Removed directory: {temp}")

    # Remove spec file
    spec_file = "main.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"Removed spec file: {spec_file}")

    print("Uninstallation completed successfully.")


if __name__ == '__main__':
    uninstall()