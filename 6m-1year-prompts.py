import os
import time

def zero_out_data(file_path, dry_run=True):
    """Zero out data in the file."""
    with open(file_path, 'wb') as f:
        f.write(b'\0' * os.path.getsize(file_path))
    if not dry_run:
        os.remove(file_path)

def get_saved_space(start_time, dry_run=True):
    """Calculate the amount of space that would be saved."""
    saved_space = 0
    for dirpath, dirnames, filenames in os.walk("/path/to/directory"):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.getctime(file_path) < start_time:
                file_size = os.path.getsize(file_path)
                saved_space += file_size
                if not dry_run:
                    zero_out_data(file_path)
    return saved_space

if __name__ == '__main__':
    dry_run = True

    # Get current time
    now = time.time()

    # Calculate saved space after 6 months
    start_time_6_months_ago = now - 180 * 24 * 60 * 60
    saved_space_6_months = get_saved_space(start_time_6_months_ago, dry_run)
    gb_saved_space_6_months = saved_space_6_months / 1e9
    tb_saved_space_6_months = saved_space_6_months / 1e12

    # Calculate saved space after 1 year
    start_time_1_year_ago = now - 365 * 24 * 60 * 60
    saved_space_1_year = get_saved_space(start_time_1_year_ago, dry_run)
    gb_saved_space_1_year = saved_space_1_year / 1e9
    tb_saved_space_1_year = saved_space_1_year / 1e12

    print("--- 6 Months ---")
    print("Saved space: {:.2f} GB / {:.2f} TB".format(gb_saved_space_6_months, tb_saved_space_6_months))
    print("--- 1 Year ---")
    print("Saved space: {:.2f} GB / {:.2f} TB".format(gb_saved_space_1_year, tb_saved_space_1_year))

    # Prompt user to select a time period to zero out data
    while True:
        choice = raw_input("Choose a time period to zero out data ("6m" / "1y"): ")
        if choice == '6m':
            start_time = start_time_6_months_ago
            break
        elif choice == '1y':
            start_time = start_time_1_year_ago
            break
        else:
            print("Invalid choice, please try again.")

  # Zero out data
saved_space = 0
if not dry_run:
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'w') as f:
                    f.write("\0" * zero_out_size)
                saved_space += zero_out_size
            except Exception as e:
                print("Error zeroing out file:", full_path)
                print("Error:", e)

# Save to log file
if saved_space > 0:
    with open("zeroed_saved_space_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {saved_space / 1024 / 1024 / 1024:.2f} GB zeroed out\n")
