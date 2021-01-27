import global_vars as gv

VALID_RIGHT_OPERATOR = ('!',)
VALID_MIDDLE_OPERATOR = ('+', '-', '*', '/', '^')
VALID_OPERATOR = VALID_MIDDLE_OPERATOR + VALID_RIGHT_OPERATOR

VALID_FUNC_X = ('sin', 'cos', 'tan', 'sqrt', 'abs', 'ln')
VALID_FUNC_X_Y = ('log',)
VALID_FUNC = VALID_FUNC_X + VALID_FUNC_X_Y

VALID_SPECIAL_NUM = ('pi', 'e', 'x', 'y')

VALID_USER_INPUT = VALID_OPERATOR + VALID_FUNC + VALID_SPECIAL_NUM

func_x_y_from_operator = {
    'log': 'L'
}

operator_of_func_x_y = {
    'L': 'log'
}


def is_middle_operator(f):
    return f in VALID_MIDDLE_OPERATOR


def is_right_operator(f):
    return f in VALID_RIGHT_OPERATOR


def is_operator(f):
    return f in VALID_OPERATOR


def is_func_x(f):
    if (len(f) > 1) and (f[0] == '-'):
        f = f[1:]
    return f in VALID_FUNC_X


def is_func_x_y(f):
    if (len(f) > 1) and (f[0] == '-'):
        f = f[1:]
    return f in VALID_FUNC_X_Y


def is_operator_of_func_x_y(f):
    return operator_of_func_x_y.get((f)) != None


def is_func(f):
    if (len(f) > 1) and (f[0] == '-'):
        f = f[1:]
    return f in VALID_FUNC


def is_special_num(f):
    if (len(f) > 1) and (f[0] == '-'):
        f = f[1:]
    return f in VALID_SPECIAL_NUM


def is_num(exp):
    try:
        f = float(exp)
    except:
        return False
    return True


def is_valid_end_of_func(exp):
    return is_num(exp) or is_special_num(exp) or exp == ')'


# turn 3x+2(2+4)sin(5) to 3*x+2*(2+4)*sin(5)
def add_mul_sign(s):
    for i in range(1, len(s)):
        if s[i].isalpha() or s[i] == '(':
            if s[i-1].isdigit() or s[i-1] == ')':
                s = s[:i] + '*' + s[i:]
    return s


# remove spaces in edges of expression inside parenthesis
def strip_spaces(s):
    if len(s) < 1:
        return s

    s = s.strip()
    start = 0
    position = 1

    while position > -1:
        position = s[start:].find('(')
        if position > -1:
            start += position
            end = find_match_parenthesis(s[start:])
            if gv.err == None:
                end += start
            else:
                gv.err = "mismatch parenthesis"
            tmp_s = s[start + 1:end]
            tmp_strip = tmp_s.strip()
            s = s.replace(tmp_s, tmp_strip)
            start += 1

    return s


def find_next_opening_parenthesis(s):
    if len(s) < 1:
        return None
    i = 0

    for i in range(len(s)):
        if s[i] == '(':
            return i
        elif s[i] != ' ':
            return None
    return None


# replacing '0-' for each '-' in the beginning of a new sentance
def arrange_negative_sign(s):
    if len(s) < 1:
        return s

    s = strip_spaces(s)

    if s[0] == '-':
        s = '0' + s

    s = s.replace('(-', '(0-')

    return s


# arrange functions in format f(x,y) as (x)f(y)
def arrange_func_x_y(exp):
    for func in VALID_FUNC_X_Y:
        # remove spaces between function and '('
        while (func + ' ') in exp:
            start = exp.find((func + ' ')) + len(func)
            end = start + find_next_opening_parenthesis(exp[start:])
            if end == None:
                gv.err = f"missing '()' after {func}"
                return None
            exp = exp[:start] + exp[end:]
        # check for valid coma (x,y)
        tmp_s = exp
        while func in tmp_s:
            start = tmp_s.find(func) + len(func)
            end = start + find_match_parenthesis(tmp_s[start:])
            if tmp_s.count(',', start, end) != 1:
                gv.err = f"illegal expression {func}" + tmp_s[start:end] + ")"
                return None
            tmp_s = tmp_s[:(start - len(func))] + tmp_s[end:]
        # arrange f(x,y) as (x) f (y)
        while (func + '(') in exp:
            start = exp.find(func + '(') + len(func)
            end = start + find_match_parenthesis(exp[start:]) + 1
            tmp_s = exp[start:end]
            coma = tmp_s.find(',')
            x = '(' + tmp_s[1:coma] + ')'
            y = '(' + tmp_s[coma + 1:-1] + ')'
            start -= len(func)
            exp = exp[:start] + x + func_x_y_from_operator.get(func) + y + exp[end:]

    return exp


def parse(expression):
    valid_list = []

    if expression == '':
        gv.err = 'empty expression'
        return valid_list

    if expression.count('(') != expression.count(')'):
        gv.err = 'mismatch parenthesis'
        return valid_list

    expression = expression.lower()
    if gv.is_debug_mode:
        print(f'\nuser input: {expression}')
    expression = arrange_negative_sign(expression)
    if gv.is_debug_mode:
        print(f'after removing negative sign: {expression}')
    expression = add_mul_sign(expression)
    if gv.is_debug_mode:
        print(f'after adding mul sign: {expression}')
    expression = arrange_func_x_y(expression)
    if gv.is_debug_mode:
        print(f'after arranging f(x,y): {expression}')

    if gv.err != None:
        return None

    position = 0
    open_parenthesis_counter = 0
    is_operator_mandatory = False
    is_unknown_negative_valid = True
    is_openning_parenthesis_allowd = True
    is_openning_parenthesis_mandatory = False
    is_closing_parenthesis_allowd = False
    word = ''
    unknown_negative = False
    is_in_word = False
    is_building_num = False

    while position < len(expression):
        char_to_parse = expression[position]

        # new word
        if not is_in_word:

            if char_to_parse == ' ':
                position += 1
                continue

            if is_operator_mandatory:
                if not (is_operator(char_to_parse) or is_operator_of_func_x_y(char_to_parse) or char_to_parse == ')'):
                    gv.err = ('missing operator after ' + expression[:position])
                    break

            if is_openning_parenthesis_mandatory:
                if char_to_parse != '(':
                    gv.err = ("missing '(' after " + expression[:position])
                    break

            if char_to_parse == '-' and (not is_operator_mandatory) and is_unknown_negative_valid:
                is_unknown_negative_valid = False
                unknown_negative = True
                is_openning_parenthesis_allowd = True
                is_closing_parenthesis_allowd = False
                word += char_to_parse
                is_in_word = True
                position += 1
                continue

            if is_operator(char_to_parse) or is_operator_of_func_x_y(char_to_parse):
                if is_operator_mandatory:
                    valid_list.append(char_to_parse)
                    if is_middle_operator(char_to_parse) or is_operator_of_func_x_y(char_to_parse):
                        is_unknown_negative_valid = True
                        is_operator_mandatory = False
                        is_openning_parenthesis_allowd = True
                        is_closing_parenthesis_allowd = False
                    # right operator
                    else:
                        is_unknown_negative_valid = False
                        is_operator_mandatory = True
                        is_openning_parenthesis_allowd = False
                        is_closing_parenthesis_allowd = True

                    position += 1
                    continue
                else:
                    gv.err = ("unexpected operator '" + char_to_parse + "' after " + expression[:position])
                    break

            elif char_to_parse == '(':
                if is_openning_parenthesis_allowd:
                    valid_list.append(char_to_parse)
                    is_closing_parenthesis_allowd = False
                    is_openning_parenthesis_mandatory = False
                    position += 1
                    is_unknown_negative_valid = True
                    is_operator_mandatory = False
                    open_parenthesis_counter += 1
                    continue
                else:
                    gv.err = ("unexpected '(' after " + expression[:position])
                    break

            elif char_to_parse == ')':
                if is_closing_parenthesis_allowd:
                    valid_list.append(char_to_parse)
                    position += 1
                    is_unknown_negative_valid = False
                    open_parenthesis_counter -= 1
                    if open_parenthesis_counter == 0:
                        is_closing_parenthesis_allowd = False
                    is_openning_parenthesis_allowd = False
                    is_operator_mandatory = True
                    continue
                else:
                    gv.err = "unexpected empty parenthesis '()'"
                    break

            # beginning of new number or func
            word += char_to_parse
            is_in_word = True
            is_building_num = (char_to_parse.isdigit() or (char_to_parse == '.'))
            position += 1
            continue

        # not a new word
        else:
            # - in the first place, check if valid function or number
            if unknown_negative:
                is_building_num = (char_to_parse.isdigit() or char_to_parse == '.')
                unknown_negative = False
                if not is_building_num and not char_to_parse.isalpha():
                    gv.err = ('missing parameter after ' + expression[:position])
                    break
                continue

            # building a number
            if is_building_num:
                if char_to_parse.isdigit() or char_to_parse == '.':
                    word += char_to_parse
                    position += 1
                    continue

                # end of number
                else:
                    if not is_num(word):
                        gv.err = ("invalid expression '" + word + "'")
                        break
                    else:
                        valid_list.append(word)
                        word = ''
                        is_in_word = False
                        is_building_num = False
                        is_operator_mandatory = True
                        is_openning_parenthesis_allowd = False
                        is_closing_parenthesis_allowd = (open_parenthesis_counter > 0)
                        is_unknown_negative_valid = False
                        continue

            # not a number
            else:

                # building a function
                if char_to_parse.isalpha():
                    word += char_to_parse
                    position += 1
                    continue

                # end of func
                else:
                    if is_func(word) or is_special_num(word):
                        valid_list.append(word)
                        if is_special_num(word):
                            is_operator_mandatory = True
                            is_openning_parenthesis_allowd = False
                            is_closing_parenthesis_allowd = (open_parenthesis_counter > 0)
                        else:
                            is_openning_parenthesis_allowd = True
                            is_openning_parenthesis_mandatory = True
                        word = ''
                        is_in_word = False
                        is_building_num = False
                        is_unknown_negative_valid = True
                        continue
                    # not a valid function
                    else:
                        gv.err = ("'" + word + "' is not a valid function")
                        break

    # handle last word in expression
    if gv.err == None:
        # expression ended in the beginning of a new expression
        if word == '':
            if not is_valid_end_of_func(char_to_parse) and not is_operator_mandatory:
                gv.err = ("invalid end of expression: '" + char_to_parse + "'")

        # expression ended during the building of number or function
        else:
            if is_num(word):
                valid_list.append(word)
            elif is_special_num(word):
                valid_list.append(word)
            else:
                gv.err = ("invalid expression: '" + word + "'")

    # restore original function name
    for func in operator_of_func_x_y:
        for i in range(len(valid_list)):
            if valid_list[i] == func:
                valid_list[i] = operator_of_func_x_y.get(valid_list[i])

    return valid_list


def find_match_parenthesis(l):
    i = 1
    counter = 1

    if l == None or len(l) < 2:
        gv.err = "can't find matching )"
        return None

    while counter > 0 and i < len(l):
        if (l[i]) == '(':
            counter += 1
        elif l[i] == ')':
            counter -= 1
        i += 1

    if counter > 0:
        gv.err = "can't find matching )"
        return None
    else:
        return i - 1


def main():
    print(f"valid expressions are: {VALID_USER_INPUT}\n")

    gv.is_debug_mode = False
    is_test_mode = False

    exp = '  .3^e -( -tan(pi/4) ) ^ 4 +-ln(e^2)'  # -2.962097469297049
    exp = '-e*7^-pi^-3'  # -250700883.2992471
    exp = '-(  -0.5^(3+4) * sqrt( 9 ) / sin(-pi/4))'  # -0.03314563036811942
    exp = '  -.3^pi * sqrt( sin(pi/2) ) + cos(pi/4) /ln(e^2)'  # 0.33078522847446457
    exp = '  -ln(e^(3+6))*.3^pi'  # -0.20491345906928324
    exp = '(-2)^pi'  # illegal -2 ^ pi

    while (True):
        if not is_test_mode:
            exp = input('enter expression (Q = QUIT, ? = HELP): ')

        if exp.lower() == 'q':
            break
        elif exp == '?':
            print(f"\nvalid expressions are: {VALID_USER_INPUT}\n")
            continue

        r = get_result_from_expression(exp)

        print('\nresult:\n-------------------------------------------------')

        if (gv.err != None):
            print(gv.err)
            gv.err = None
        else:
            print(r)

        print('-------------------------------------------------')

        if (is_test_mode):
            break

# main()

