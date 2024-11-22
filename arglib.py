import re
import inspect

# from icecream import ic


def get_call_site_source_code(current_frame) -> str:
    """
    current_frame = inspect.currentframe()
    """
    # collect caller information
    caller = inspect.getframeinfo(current_frame.f_back, context=0xFFFFFFFFFFFFFFFF)
    positions = caller.positions

    function_call = caller.code_context[positions.lineno - 1 : positions.end_lineno]

    full_call = "".join(function_call)

    col_offset = positions.col_offset
    # trim away the col_offset
    call_site_source_code = full_call[col_offset:]

    # Remove whitespaces and newlines
    # call_site_source_code = re.sub(r"\s+", " ", call_site_source_code)

    # we must parse the function call to detect when it ends based on the number of brackets
    # care must be taken to handle brackets in strings
    # first we must get the offset from the function name
    # then we must count the number of brackets

    function_name_offset = call_site_source_code.find("(")
    open_brackets = 0
    after_funcion_args_offset = function_name_offset - 1
    while True:
        after_funcion_args_offset += 1
        c = call_site_source_code[after_funcion_args_offset]
        if c == "(":
            open_brackets += 1
        if c == ")":
            open_brackets -= 1
        if c == '"' or c == "'":
            # skip the string
            string_end = call_site_source_code[after_funcion_args_offset + 1 :].find(c)
            after_funcion_args_offset += string_end + 1
        if open_brackets == 0:
            after_funcion_args_offset += 1
            break

    # find the next closing bracket or newline starting from after the function args offset
    end_of_call_site = after_funcion_args_offset
    while True:
        c = call_site_source_code[end_of_call_site]
        if c == ")" or c == "\n":
            break
        end_of_call_site += 1

    call_site_source_code = call_site_source_code[:end_of_call_site]

    # ic(call_site_source_code)

    return call_site_source_code


def get_call_site_lasts_comment(source_code: str) -> str:
    comment = re.findall(r"#(.*)", source_code)
    return comment[-1] if comment else ""


def comment_arguments():
    current_frame = inspect.currentframe().f_back
    source_code = get_call_site_source_code(current_frame)
    comment = get_call_site_lasts_comment(source_code)
    comment = comment.strip()

    c_args = []
    c_kwargs = {}

    def capture_args(*args, **kwargs):
        nonlocal c_args, c_kwargs
        c_args = args
        c_kwargs = kwargs

    eval(f"capture_args({comment})")

    return c_args, c_kwargs
