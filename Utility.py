def RepresentsNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
