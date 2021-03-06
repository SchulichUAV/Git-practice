from Tools.PrintLog import print_log
import Tools.PrintLog


def mirror(str):
    return str + str[::-1]


def remove_letter(ch, str):
    result = ""
    for letter in str[:]:
        if not letter == ch:
            result += letter
    return result


if __name__ == "__main__":
    print_log(mirror('abc'))
    print_log(mirror('def'))
    print_log(mirror('ghi'))
    print_log(mirror('123'))

'''
def test(did_pass):
    linenum = sys._getframe(1).f_lineno
    if did_pass:
        msg = "Test at line {0} ok.".format(linenum)
    else:
        msg = ("Test at line {0} FAILED.".format(linenum))
    print(msg)

test(mirror("good") == "gooddoog")
test(mirror("Python") == "PythonnohtyP")
test(mirror("") == "")
test(mirror("a") == "aa")

test(remove_letter("b", "") == "")
test(remove_letter("a", "apple") == "pple")
test(remove_letter("a", "banana") == "bnn")
test(remove_letter("z", "banana") == "banana")
test(remove_letter("i", "Mississippi") == "Msssspp")
test(remove_letter("b", "c") == "c")
'''
