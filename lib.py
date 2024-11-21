import re
import inspect


def get_call_site_source_code(current_frame) -> str:
    """
    current_frame = inspect.currentframe()
    """
    # collect caller information
    caller = inspect.getframeinfo(current_frame.f_back, context=0xFFFFFFFFFFFFFFFF)
    positions = caller.positions

    function_call = caller.code_context[positions.lineno - 1 : positions.end_lineno]

    # Remove whitespaces and newlines
    call_site_source_code = re.sub("\s+", " ", "".join(function_call))
    return call_site_source_code


def get_call_site_lasts_comment(source_code: str) -> str:
    comment = re.findall(r"#(.*)", source_code)
    return comment[-1] if comment else ""


def add():
    current_frame = inspect.currentframe()
    source_code = get_call_site_source_code(current_frame)
    comment = get_call_site_lasts_comment(source_code)
    # strip whitespaces
    comment = comment.strip()
    # split by whitespaces
    comment = comment.split()
    # parse integers
    input_ints = [int(i) for i in comment]
    # sum integers
    result = sum(input_ints)
    return result
