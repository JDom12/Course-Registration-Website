import subprocess
import os

def run_tests_in_folder(folder):
    print(f"Running tests in {folder}")
    result = subprocess.run(["pytest"], cwd=folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.stderr:
        print("Errors:", result.stderr.decode())

def main():
    base_dir = "."  
    subfolders = ["Admin_Functions", "Professor_Functions", "Course_Management", "Registration"]

    for folder in subfolders:
        folder_path = os.path.join(base_dir, folder)
        run_tests_in_folder(folder_path)

    print("All tests completed!")

if __name__ == "__main__":
    main()
