from click import echo, style
import time

def print_progress_current(i, filename, atom_count, file_count):
    echo(
        style(
            f"Processing {filename} with " f"{atom_count} atoms ({i}/{file_count})",
            fg="yellow",
        )
    )


def print_finished_progress(filename, atom_count, elapsed_time):
    echo(
        style(
            f"Processed {filename} with {atom_count} atoms in "
            f"{round(elapsed_time, 2)} s",
            fg="blue",
        )
    )


def print_total_time(elapsed_time, file_count):
    echo(
        style(
            f"Finished - Processed total {file_count} files in "
            f"{round(elapsed_time, 2)} s",
            fg="green",
        )
    )


def print_done_with_option(option_name):
    echo(style(f"Done with {option_name}", fg="green"))


def print_moved_files_summary(filtered_file_paths, file_count, destination_path=None):
    if destination_path:
        echo(
            style(
                f"Moved {len(filtered_file_paths)} out of {file_count} files to "
                f"{destination_path}."
            )
        )
    else:
        echo(style(f"Moved {len(filtered_file_paths)} out of {file_count} files."))
