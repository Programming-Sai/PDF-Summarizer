import subprocess
import platform
import shutil
import os


def install():
    print("Starting installation...")
    base_dir = os.getcwd()
    # Step 1: Use PyInstaller to create a standalone executable
    print("Creating standalone executable with PyInstaller...")
    main_script_path = os.path.join(base_dir, "ospdf", "main.py")
    if not os.path.exists(main_script_path):
        print(f"Error: Script file '{main_script_path}' does not exist.")
        return
    subprocess.run(["pyinstaller", "--onefile", main_script_path], check=True)

    # Step 2: Determine global installation path
    system = platform.system()
    if system == "Windows":
        install_path = os.path.join(os.getenv("APPDATA"), "ospdf")
    else:
        install_path = "/usr/local/bin"

    # Step 3: Move the executable
    exec_name = "main.exe" if system == "Windows" else "main"
    source_path = os.path.join("dist", exec_name)
    target_path = os.path.join(install_path, "ospdf")

    os.makedirs(install_path, exist_ok=True)
    shutil.move(source_path, target_path)
    print(f"Moved executable to {target_path}")

    # Step 4: Make it globally accessible (for Unix/Linux)
    if system != "Windows":
        os.chmod(target_path, 0o755)

    print("Installation completed successfully.")




if __name__ == '__main__':
    install()