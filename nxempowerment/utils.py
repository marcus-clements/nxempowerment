
import math



def logzero(k: float):
    return 0 if k == 0 else math.log(k, 2)


def sigfigs(value: float, sig_figs: int, min_value: float = 1e-06) -> str:
    if not isinstance(value, float):
        return str(value)
    if abs(value) < min_value:
        return "0"
    return "{{:.{}g}}".format(sig_figs).format(value)

