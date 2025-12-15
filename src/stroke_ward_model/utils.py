def minutes_to_ampm(minutes: int) -> str:
    """
    Convert minutes since simulation start to a 12-hour AM/PM clock time.

    Parameters
    ----------
    minutes : int
        Minutes since simulation start.

    Returns
    -------
    str
        Time formatted as 'H:MM AM/PM'
    """
    minutes_today = minutes % 1440

    hour24 = minutes_today // 60
    minute = minutes_today % 60

    ampm = "AM" if hour24 < 12 else "PM"
    hour12 = hour24 % 12 or 12

    return f"{hour12}:{minute:02d} {ampm}"
