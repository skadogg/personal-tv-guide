def runtime_to_minutes(runtime_str, round_up = True):
    # Parses the JustWatch runtime_str into minutes
    # Input format: runtime_str = '2h 28min'
    # If round_up, rounds up to the next 15 minute increment
    
    if 'h' in runtime_str:
        # split into hours/minutes
        runtime_split = runtime_str.split("h")
        runtime_minutes = (int(runtime_split[0]) * 60) + int(runtime_split[1].split("min")[0])
    else:
        runtime_minutes = int(runtime_str.split("min")[0])
    
    if round_up:
        return runtime_minutes + 15 - (runtime_minutes % 15)
    else:
        return runtime_minutes
