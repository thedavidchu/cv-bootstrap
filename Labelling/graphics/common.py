import warnings
import traceback


def build_warning(msg: str):
    """Build a warning message function"""
    return lambda *args: unimplemented_fnc(msg)


def unimplemented_fnc(msg: str = None):
    warnings.warn(f"Unimplemented: {msg}")


def unimplemented_fnc0():
    warnings.warn("Unimplemented(0)")
    # traceback.print_stack()


def unimplemented_fnc1(arg):
    warnings.warn("Unimplemented(1)")
    # traceback.print_stack()
