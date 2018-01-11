stackOpe = [0] * 255
temp_var_1 = -1
stackOpeTop = temp_var_1
stackNumber = [0] * 255
temp_var_2 = -1
stackNumberTop = temp_var_2
def get_pri(ope):
    global stackOpe
    global stackOpeTop
    global stackNumber
    global stackNumberTop
    temp_var_3 = ope == 40
    if temp_var_3:
        return 0
    temp_var_4 = ope == 43
    temp_var_5 = ope == 45
    temp_var_6 = temp_var_4 or temp_var_5
    if temp_var_6:
        return 1
    temp_var_7 = ope == 42
    temp_var_8 = ope == 47
    temp_var_9 = temp_var_7 or temp_var_8
    if temp_var_9:
        return 2
    temp_var_10 = -1
    return temp_var_10

def compute(ope):
    global stackOpe
    global stackOpeTop
    global stackNumber
    global stackNumberTop
    n = None
    n1 = None
    n2 = None
    temp_var_11 = 1 * stackNumberTop
    temp_var_12 = temp_var_11 + 0
    n1 = stackNumber[temp_var_12]
    stackNumberTop -= 1
    temp_var_13 = 1 * stackNumberTop
    temp_var_14 = temp_var_13 + 0
    n2 = stackNumber[temp_var_14]
    stackNumberTop -= 1
    temp_var_15 = ope == 43
    if temp_var_15:
        temp_var_16 = n2 + n1
        n = temp_var_16
    temp_var_17 = ope == 45
    if temp_var_17:
        temp_var_18 = n2 - n1
        n = temp_var_18
    temp_var_19 = ope == 42
    if temp_var_19:
        temp_var_20 = n2 * n1
        n = temp_var_20
    temp_var_21 = ope == 47
    if temp_var_21:
        temp_var_22 = n2 / n1
        n = temp_var_22
    stackNumberTop += 1
    temp_var_23 = 1 * stackNumberTop
    temp_var_24 = temp_var_23 + 0
    stackNumber[temp_var_24] = n

def deal_ope(ope):
    global stackOpe
    global stackOpeTop
    global stackNumber
    global stackNumberTop
    old_ope = None
    temp_var_25 = stackOpeTop < 0
    temp_var_26 = ope == 40
    temp_var_27 = temp_var_25 or temp_var_26
    if temp_var_27:
        stackOpeTop += 1
        temp_var_28 = 1 * stackOpeTop
        temp_var_29 = temp_var_28 + 0
        stackOpe[temp_var_29] = ope
        return
    temp_var_30 = 1 * stackOpeTop
    temp_var_31 = temp_var_30 + 0
    old_ope = stackOpe[temp_var_31]
    temp_var_32 = get_pri(ope)
    temp_var_33 = get_pri(old_ope)
    temp_var_34 = temp_var_32 > temp_var_33
    if temp_var_34:
        stackOpeTop += 1
        temp_var_35 = 1 * stackOpeTop
        temp_var_36 = temp_var_35 + 0
        stackOpe[temp_var_36] = ope
        return
    while True:
        temp_var_37 = get_pri(ope)
        temp_var_38 = get_pri(old_ope)
        temp_var_39 = temp_var_37 <= temp_var_38
        if not temp_var_39:
            break
        temp_var_40 = 1 * stackOpeTop
        temp_var_41 = temp_var_40 + 0
        old_ope = stackOpe[temp_var_41]
        stackOpeTop -= 1
        temp_var_42 = compute(old_ope)
        temp_var_43 = stackOpeTop < 0
        if temp_var_43:
            break
        temp_var_44 = 1 * stackOpeTop
        temp_var_45 = temp_var_44 + 0
        old_ope = stackOpe[temp_var_45]
    stackOpeTop += 1
    temp_var_46 = 1 * stackOpeTop
    temp_var_47 = temp_var_46 + 0
    stackOpe[temp_var_47] = ope

def deal_bracket():
    global stackOpe
    global stackOpeTop
    global stackNumber
    global stackNumberTop
    temp_var_48 = 1 * stackOpeTop
    temp_var_49 = temp_var_48 + 0
    old_ope = stackOpe[temp_var_49]
    while True:
        temp_var_50 = old_ope != 40
        if not temp_var_50:
            break
        temp_var_51 = 1 * stackOpeTop
        temp_var_52 = temp_var_51 + 0
        old_ope = stackOpe[temp_var_52]
        stackOpeTop -= 1
        temp_var_53 = compute(old_ope)
        temp_var_54 = 1 * stackOpeTop
        temp_var_55 = temp_var_54 + 0
        old_ope = stackOpe[temp_var_55]
    temp_var_56 = 1 * stackOpeTop
    temp_var_57 = temp_var_56 + 0
    old_ope = stackOpe[temp_var_57]
    stackOpeTop -= 1

def main():
    global stackOpe
    global stackOpeTop
    global stackNumber
    global stackNumberTop
    string = "113+(26-2)*4/(2+1)\0"
    i = 0
    value = 0
    flag = 0
    old_ope = None
    while True:
        temp_var_58 = 1 * i
        temp_var_59 = temp_var_58 + 0
        temp_var_60 = ord(string[temp_var_59]) != 0
        if not temp_var_60:
            break
        temp_var_61 = 1 * i
        temp_var_62 = temp_var_61 + 0
        temp_var_63 = ord(string[temp_var_62]) >= 48
        temp_var_64 = 1 * i
        temp_var_65 = temp_var_64 + 0
        temp_var_66 = ord(string[temp_var_65]) <= 57
        temp_var_67 = temp_var_63 and temp_var_66
        if temp_var_67:
            temp_var_68 = value * 10
            temp_var_69 = 1 * i
            temp_var_70 = temp_var_69 + 0
            temp_var_71 = temp_var_68 + ord(string[temp_var_70])
            temp_var_72 = temp_var_71 - 48
            value = temp_var_72
            flag = 1
        else:
            if flag:
                stackNumberTop += 1
                temp_var_73 = 1 * stackNumberTop
                temp_var_74 = temp_var_73 + 0
                stackNumber[temp_var_74] = value
                flag = 0
                value = 0
            temp_var_75 = 1 * i
            temp_var_76 = temp_var_75 + 0
            temp_var_77 = ord(string[temp_var_76]) == 41
            if temp_var_77:
                temp_var_78 = deal_bracket()
            else:
                temp_var_79 = 1 * i
                temp_var_80 = temp_var_79 + 0
                temp_var_81 = deal_ope(ord(string[temp_var_80]))
        i += 1
    if flag:
        stackNumberTop += 1
        temp_var_82 = 1 * stackNumberTop
        temp_var_83 = temp_var_82 + 0
        stackNumber[temp_var_83] = value
    while True:
        temp_var_84 = stackOpeTop >= 0
        if not temp_var_84:
            break
        temp_var_85 = 1 * stackOpeTop
        temp_var_86 = temp_var_85 + 0
        old_ope = stackOpe[temp_var_86]
        stackOpeTop -= 1
        temp_var_87 = compute(old_ope)
    temp_var_88 = 1 * stackNumberTop
    temp_var_89 = temp_var_88 + 0
    value = stackNumber[temp_var_89]
    stackNumberTop -= 1
    temp_var_90 = print("%s = %lf\0" % (string, value))
    return 0

main()