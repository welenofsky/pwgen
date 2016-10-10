from __future__ import print_function
# This is a extension of the trifid cipher
import sys
import re
import argparse

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
    polybius = [[[dictionary.pop(0) for x in range(4)] for x in range(4)] for x in range(4)]
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


def get_input(message):
    if sys.version_info >= (3,0):
        return input(message)
    return raw_input(message)


def generate_pw(pw = None, website = None):
    stripped_pw = ""
    new_pass = ""
    list_z = []
    list_x = []
    list_y = []

    if not pw:
        pw = get_input("Please enter a password:\n")

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

    if not website:
        website = get_input("What website/company is this password for?\n")

    if len(website.rstrip()) < 8:
        print((
            "The length of the website name is too small."
            " The website name has a 1:1 correlation to pw size."
            " Use a longer website name. Ex: www.abc.com"))

    for c in website:
        if c not in dictionary:
            website = website.replace(c, '')

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

    if not re.search('[0-9]+', new_pass):
        # Add number if none were used, based on first letter in pw used
        new_pass += str(ord(stripped_pw[:1]))

    return new_pass


def main():
    parser = argparse.ArgumentParser(description="Generates passwords based on the quad-fid internet friendly cipher.")
    parser.add_argument("-p", metavar="PASSWORD", type=str,
                        help="The master password, you only need to use one for all websites.")
    parser.add_argument("-w", metavar="WEBSITE", type=str,
                        help="The website you are generating the password for.")
    args = parser.parse_args()

    new_pass = generate_pw(args.p, args.w)

    print(new_pass)


main()