from __future__ import print_function
# This is a extension of the trifid cipher
import sys
import re

# 64 character dictionary
dictionary = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.?"
)


def build_polybius(pw, dictionary):
    pw_list = [c for c in pw]
    while len(pw_list) > 0:
        letter = pw_list.pop(0)
        if letter in dictionary:
            dictionary = dictionary.replace(letter, '')
        else:
            print((
                "%s is an invalid character. Please only use a-z, A-Z, 0-9, "
                "'.', and '?' to make up your password") % letter)

    dictionary = [c for c in (pw + dictionary)]
    if len(dictionary) != 64:
        print("Oops! an error has occured. Sorry about that :(")
        sys.exit()

    # "quad"fid cipher
    arr_1 = [[dictionary.pop(0) for x in range(4)] for x in range(4)]
    arr_2 = [[dictionary.pop(0) for x in range(4)] for x in range(4)]
    arr_3 = [[dictionary.pop(0) for x in range(4)] for x in range(4)]
    arr_4 = [[dictionary.pop(0) for x in range(4)] for x in range(4)]
    polybius = [arr_1, arr_2, arr_3, arr_4]
    # return the quadfid
    return polybius


def get_position(char, polybius):
    # Returns tuple with z,x,y coords
    z = 0
    x = 0
    y = 0
    for z in range(len(polybius)):
        for li_x in polybius[z]:
            x = polybius[z].index(li_x)
            for li_y in polybius[z][x]:
                y = polybius[z][x].index(li_y)
                if char == polybius[z][x][y]:
                    return (z, x, y)


if __name__ == "__main__":
    stripped_pw = ""
    new_pass = ""
    list_z = []
    list_x = []
    list_y = []

    if len(sys.argv) > 1:
        pw = sys.argv[1]
    else:
        if sys.version_info >= (3, 0):
            pw = input('Please enter a password:\n')
        else:
            pw = raw_input('Please enter a password:\n')

        if len(pw.rstrip()) <= 0:
            print(
                "I need a password to continue... "
                "Try again when you come up with one"
            )
            sys.exit()

    for c in pw:
        if c not in stripped_pw and c in dictionary:
            stripped_pw += c

    # PW must be unique for polybius square
    if len(stripped_pw) < 4:
        print((
            "Password afted reduction is too small to be used. "
            "Use a password with 4 or more unique characters/numbers"))
        sys.exit()
    elif len(stripped_pw) > 64:
        print((
            "Amazingly, your password was larger than possible for "
            "this method of pw encoding. Please only use a-z, A-Z, 0-9, "
            "'.', and '?' to make up your password"))
        sys.exit()

    polybius = build_polybius(stripped_pw, dictionary)

    if sys.version_info >= (3, 0):
        website = input("What website/company is this password for?\n")
    else:
        website = raw_input("What website/company is this password for?\n")
    

    for c in website:
        if c not in dictionary:
            website = website.replace(c, '')

    if len(website.rstrip()) < 8:
        print((
            "The length of the website name is too small."
            " The website name has a 1:1 correlation to pw size."
            " Use a longer website name. Ex: www.abc.com"))

    for c in website:
        pos = get_position(c, polybius)
        list_z.append(str(pos[0]))
        list_x.append(str(pos[1]))
        list_y.append(str(pos[2]))

    stringofnumbers = "%s%s%s" % (
        ''.join(list_z),
        ''.join(list_x),
        ''.join(list_y)
    )

    while(len(stringofnumbers) >= 3):
        z, x, y = stringofnumbers[:3]
        z = int(z)
        x = int(x)
        y = int(y)
        stringofnumbers = stringofnumbers[3:]
        new_pass += polybius[z][x][y]

    if re.search('[0-9]+', new_pass):
        print("Generated password: %s\n" % new_pass)
    else:
        print("Note: password generated did not have a number so I added one")
        new_pass += str(ord(new_pass[:1]))
        print("Generated password: %s\n" % new_pass)
