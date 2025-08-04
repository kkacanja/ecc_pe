import os
import subprocess

# Get current working directory
#base_dir = os.getcwd()
base_dir = os.path.expanduser('~/ecc_pe/gw200105/seobHM/workflow/runs')

# Loop through all subdirectories starting with 'e_'
for dirname in sorted(os.listdir(base_dir)):
    dirpath = os.path.join(base_dir, dirname)
    submit_file = os.path.join(dirpath, 'submit.sub')

    # Check if it's a directory and has a submit file
    if os.path.isdir(dirpath) and os.path.isfile(submit_file):
        print(f"[INFO] Submitting job in: {dirname}")
        try:
            result = subprocess.run(['condor_submit', 'submit.sub'], cwd=dirpath, check=True, capture_output=True, text=True)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to submit job in {dirname}")
            print(e.stderr.strip())
    else:
        print(f"[SKIP] No submit.sub in {dirname}")
