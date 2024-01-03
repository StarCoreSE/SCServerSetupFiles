import requests
import zipfile
import os
import subprocess
import time
import shutil

def download_file(url, target_path):
    response = requests.get(url, stream=True)
    with open(target_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def copy_starcore_configs(server_folders):
    starcore_configs_folder = "starcore-configs"
    if os.path.exists(starcore_configs_folder):
        for server_folder in server_folders:
            target_folder = server_folder
            if not os.path.exists(target_folder):
                shutil.copytree(starcore_configs_folder, target_folder, dirs_exist_ok=True)
            else:
                # Copy instance folder contents
                instance_folder_src = os.path.join(starcore_configs_folder, "Instance")
                instance_folder_dst = os.path.join(target_folder, "Instance")
                if os.path.exists(instance_folder_src):
                    shutil.copytree(instance_folder_src, instance_folder_dst, dirs_exist_ok=True)

                # Copy plugins folder
                plugins_folder_src = os.path.join(starcore_configs_folder, "Plugins")
                plugins_folder_dst = os.path.join(target_folder, "Plugins")
                if os.path.exists(plugins_folder_src):
                    shutil.copytree(plugins_folder_src, plugins_folder_dst, dirs_exist_ok=True)

                # Copy torch.cfg
                torch_cfg_src = os.path.join(starcore_configs_folder, "torch.cfg")
                torch_cfg_dst = os.path.join(target_folder, "torch.cfg")
                if os.path.exists(torch_cfg_src):
                    shutil.copy(torch_cfg_src, torch_cfg_dst)

def setup_server(num_servers):
    server_folders = []
    for i in range(1, num_servers + 1):
        server_folder = f"torch-server-starcore-{str(i).zfill(2)}"
        os.makedirs(server_folder, exist_ok=True)
        server_folders.append(server_folder)

    # Copy starcore-configs to each server folder
    copy_starcore_configs(server_folders)

    for server_folder in server_folders:
        # Define the URLs and paths
        zip_url = "https://build.torchapi.com/job/Torch/job/master/lastSuccessfulBuild/artifact/bin/torch-server.zip"
        git_repo_url = "https://github.com/StarCoreSE/StarcoreMTWorld.git"
        zip_path = os.path.join(server_folder, "torch-server.zip")
        extract_dir = server_folder
        git_target_path = os.path.join(extract_dir, "Instance", "Saves", "StarcoreMTWorld")

        # Download the zip file
        print(f"Downloading Torch Server for {server_folder}...")
        download_file(zip_url, zip_path)

        time.sleep(5)  # Delay for 5 seconds

        # Unzip the file into the server folder
        print(f"Unzipping Torch Server for {server_folder}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        time.sleep(5)  # Delay for 5 seconds

        # Clone the world from the git repository into the correct directory
        print(f"Downloading World for {server_folder}...")
        os.makedirs(git_target_path, exist_ok=True)

        if not os.listdir(git_target_path):
            subprocess.run(["git", "clone", git_repo_url, git_target_path])
        else:
            print(f"Directory {git_target_path} is not empty. Skipping cloning.")

        print(f"Setup complete for {server_folder}!\n")

        # Clean up the zip file
        os.remove(zip_path)

def main():
    num_servers = int(input("How many servers do you want to set up? "))
    setup_server(num_servers)

    # Remind the user to set port, server name, and world name
    print("Please remember to set the port, server name, and world name.")
    print("Set them in the torch UI when launching each .exe in the directory.")

if __name__ == "__main__":
    main()
