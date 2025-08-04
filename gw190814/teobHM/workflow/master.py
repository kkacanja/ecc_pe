import os
import shutil

# Parameters
step = 0.005
ecc_min = 0.0
ecc_max = 0.1

# Paths
base_config_path = "base/config.ini"
base_run_path = "base/run.sh"
base_submit_path = "base/submit.sub"
output_parent_dir = "runs"

# Absolute paths (adjust as needed)
base_abs_dir = "/home/kkacanja/ecc_pe/gw190814/teobHM/workflow/runs"
logs_dir = "/home/kkacanja/ecc_pe/gw190814/teobHM/workflow/logs"

# Number of bins
num_bins = int((ecc_max - ecc_min) / step)

for i in range(num_bins):
    current = round(ecc_min + i * step, 5)
    next_val = round(current + step, 5)

    folder_name = f"e_{current:.3f}".replace(".", "p")
    new_dir = os.path.join(output_parent_dir, folder_name)
    os.makedirs(new_dir, exist_ok=True)

    # -------- CONFIG FILE --------
    new_config_path = os.path.join(new_dir, "config.ini")
    shutil.copy(base_config_path, new_config_path)

    with open(new_config_path, "r") as f:
        lines = f.readlines()

    with open(new_config_path, "w") as f:
        in_ecc_block = False
        for line in lines:
            if line.strip().startswith("[prior-eccentricity]"):
                in_ecc_block = True
                f.write(line)
                continue
            if in_ecc_block:
                if line.strip().startswith("min-eccentricity"):
                    f.write(f"min-eccentricity = {current:.5f}\n")
                elif line.strip().startswith("max-eccentricity"):
                    f.write(f"max-eccentricity = {next_val:.5f}\n")
                elif line.strip().startswith("[") and line.strip().endswith("]"):
                    in_ecc_block = False
                    f.write(line)
                else:
                    f.write(line)
            else:
                f.write(line)

    # -------- RUN.SH --------
    run_dst = os.path.join(new_dir, "run.sh")
    with open(base_run_path, "r") as f:
        run_lines = f.readlines()

    config_abs = os.path.join(base_abs_dir, folder_name, "config.ini")
    result_abs = os.path.join(base_abs_dir, folder_name, "result.hdf")

    with open(run_dst, "w") as f:
        for line in run_lines:
            if "--config-file" in line:
                f.write(f"--config-file {config_abs} \\\n")
            elif "--output-file" in line:
                f.write(f"--output-file {result_abs} \\\n")
            else:
                f.write(line)

    # -------- SUBMIT.SUB --------
    submit_dst = os.path.join(new_dir, "submit.sub")
    with open(base_submit_path, "r") as f:
        submit_lines = f.readlines()

    log_prefix = f"teobHM_gw190814_{folder_name}"

    with open(submit_dst, "w") as f:
        for line in submit_lines:
            if line.strip().startswith("executable"):
                f.write(f"executable = {os.path.join(base_abs_dir, folder_name, 'run.sh')}\n")
            elif line.strip().startswith("output"):
                f.write(f"output = {logs_dir}/{log_prefix}.out\n")
            elif line.strip().startswith("error"):
                f.write(f"error = {logs_dir}/{log_prefix}.err\n")
            elif line.strip().startswith("log"):
                f.write(f"log = {logs_dir}/{log_prefix}.log\n")
            else:
                f.write(line)

print("All config, run, and submit files generated in 'runs/'")
