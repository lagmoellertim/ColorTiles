import sys
import io

print_colors = {
    "NONE": "",
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m"
}

log_level = 5
component_specific_log_level = {}


def handle_log(prefix_color, message_type_name, message, component, current_log_level):
    compare_log_level = log_level
    if component.upper() in component_specific_log_level.keys():
        compare_log_level = component_specific_log_level[component.upper()]

    if compare_log_level >= current_log_level:
        print(
            "{}[{}][{}] {}{}".format(
                print_colors[prefix_color],
                message_type_name,
                component.upper(),
                message,
                print_colors["ENDC"]
            )
        )


def debug(component, message):
    handle_log("OKBLUE", "DEBUG", message, component, 5)


def info(component, message):
    handle_log("NONE", "INFO", message, component, 4)


def success(component, message):
    handle_log("OKGREEN", "SUCCESS", message, component, 3)


def warning(component, message):
    handle_log("WARNING", "WARNING", message, component, 2)


def error(component, message):
    handle_log("FAIL", "ERROR", message, component, 1)


def exception(component, exception):
    buffer = io.StringIO()

    sys.print_exception(exception, buffer)
    exception_message = "{} {}".format(exception.__class__, exception)

    debug(component, buffer.getvalue())
    error(component, exception_message)
