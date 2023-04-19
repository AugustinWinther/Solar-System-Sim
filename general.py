def ranges_overlap(range_1: range, range_2: range) -> bool:
    """
    Returns True if range_1 and range_2 overlap.

    Credit: Ned Batchelder (https://bit.ly/30TF0E5)
    """
    return (
        range_1.start <= range_2.start <= range_1.stop or
        range_1.start <= range_2.stop  <= range_1.stop or
        range_2.start <= range_1.start <= range_2.stop or
        range_2.start <= range_1.stop  <= range_2.stop
    )

def sec_to_practical_time_string(sec: int) -> str:
    """Returns a fitting string representing time
    
    sec = 1     -> '1s'.
    sec = 60    -> '1m'.
    sec = 3600  -> '1h'.
    etc.
    """
    if sec < 60:
        return f'{sec}s'
    elif sec < (60*60):
        return f'{int(sec/60)}m'
    elif sec < (60*60*24):
        return f'{int(sec/(60*60))}h'
    elif sec < (60*60*24*365):
        return f'{int(sec/(60*60*24))}d'
    else:
        return f'{int(sec/(60*60*24*365))}y'
