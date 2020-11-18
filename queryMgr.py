CMDS = ['get_pos', 'get_neg']


def print_help():
    print('q = quit')
    print('Use format <command> <user> [<focus>]')
    print("available commands: {c}".format(c=CMDS))


# We know the command and the user are both legal
def handle_cmd(engs, cmd, user, focus):
    if cmd == CMDS[0]:
        # get_pos
        for cmt in engs[user].positives:
            if len(focus) == 0:
                print("--> {c}".format(c=cmt))
            else:
                if focus in cmt:
                    print("--> {c}".format(c=cmt))
    elif cmd == CMDS[1]:
        # get neg
        for cmt in engs[user].negatives:
            if len(focus) == 0:
                print("--> {c}".format(c=cmt))
            else:
                if focus in cmt:
                    print("--> {c}".format(c=cmt))
    else:
        return


def validate_syntax(engs, query):
    words = query.split(" ")

    if not words[0] in CMDS:
        print('-E- Unrecognized command')
        return False, None, None, None

    if not words[1] in engs.keys():
        print('-E- Unrecognized user')
        return False, None, None, None

    if len(words) < 2 or len(words) > 3:
        print('-E- Expecting two arguments')
        return False, None, None, None

    if len(words) == 2:
        return True, words[0], words[1], ""
    else:
        return True, words[0], words[1], words[2]


def handle_query(engs, query):
    if query == 'h':
        print_help()
        return

    valid, cmd, user, focus = validate_syntax(engs, query)
    if not valid:
        return

    # focus is an option to even focus the command (e.g: in get_pos/neg it filters specifies a word to filter)
    # every command can implement it's own focus word
    handle_cmd(engs, cmd, user, focus)
