def format_float(value: float) -> str:
    result = '{:.10f}'.format(value).rstrip('0')
    return result[:-1] if result[-1] == '.' else result