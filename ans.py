ans_f='csie'
ans_r='bot'
ans_b='code'
ans_l='toc'
ans_door='flrb'
ans_demo='DEMO'
def check_Q_f(text):
    if text==ans_f or text==ans_demo:
        return True
    return False
def check_Q_r(text):
    if text==ans_r or text==ans_demo:
        return True
    return False
def check_Q_b(text):
    if text==ans_b or text==ans_demo:
        return True
    return False
def check_Q_l(text):
    if text==ans_l or text==ans_demo:
        return True
    return False
def check_Q_door(text):
    if text==ans_door or text==ans_demo:
        return True
    return False

