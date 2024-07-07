from click import echo, style


def print_progress_current(i, filename, atom_count, total_file_count):
    echo(
        style(
            f"Processing {filename} with "
            f"{atom_count} atoms ({i+1}/{total_file_count})",
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


def print_done_with_option(option_name=None):
    echo(style(f"Done with {option_name}", fg="green"))
