print_colors = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m"
}

log_level = 0


def log(prefix_color, message_type_name, message):
    s = "{}[{}] {}{}".format(
        print_colors[prefix_color],
        message_type_name,
        message,
        print_colors["ENDC"]
    )

    print(s)


def debug(message):
    if log_level > 4:
        log("OKBLUE", "DEBUG", message)


def info(message):
    if log_level > 3:
        log("HEADER", "INFO", message)


def warning(message):
    if log_level > 1:
        log("WARNING", "WARNING", message)


def error(message):
    if log_level > 0:
        log("FAIL", "ERROR", message)


def success(message):
    if log_level > 2:
        log("OKGREEN", "SUCCESS", message)
