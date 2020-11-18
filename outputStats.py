import csv
from engineer import Engineer


def all_same_char(s):
    n = len(s)
    for i in range(1, n):
        if s[i] != s[0]:
            return False

    return True


def customized_pos(txt):
    if txt.startswith('right'):
        return True
    if ('because' in txt) and not('receiving this because you authored' in txt):
        return True


def customized_neg(txt):
    if ('don\'t do' in txt) and not('please don\'t do' in txt) and not('we don\'t do' in txt)\
            and not('i don\'t do' in txt):
        return True
    if ('don\'t write' in txt) and not('please don\'t write' in txt) and not('we don\'t write' in txt)\
            and not('i don\'t do' in txt):
        return True
    if all_same_char(txt):
        return True
    if (len(txt) < 10) and txt.endswith('?'):
        return True
    if txt.startswith('don\'t') and not(txt.startswith('don\'t you')) and not(txt.startswith('don\'t we')):
        return True
    if txt.startswith('do not'):
        return True
    if txt.startswith('any good reason'):
        return True
    if txt.startswith('I don\'t understand why you'):
        return True
    if txt.startswith('what is this ?') or txt.startswith('what is this?'):
        return True

    return False


def analyze_csv(f):
    newf = 'analysis_for_'+ f
    af = open(newf, "w")
    with open(f, newline='') as csvfile:
        positives = ['tnx', 'thank', '10x', 'right?', 'right ?', 'imo', 'imho', 'i think', 'maybe',
                     'consider', 'you are right', 'you\'re right', ' correct ', ':)', ';)', 'nice catch', 'afaik',
                     'afaiu', 'can you', '(;', '(:', '):', ':(', ':-)', ';-)', ':-(', '(-:', '(-;', 'great job',
                     'well done', 'amazing job', 'nicely done', 'it\'s a good idea', 'it is a good idea',
                     'it is recommended to', 'it\'s recommended to', 'I might be mistaken here', 'my mistake',
                     'i agree', 'my bad', 'this is great', 'looks good']

    # cheap poitives: 'pls', 'plz', 'please'

        negatives = ['ugly', 'stupid', 'very bad', 'you shouldn\'t', '.don\'t', ',don\'t', '.do not', ',do not', '??',
                     '???', 'can you make the code more readable', '. don\'t', ', don\'t', '. do not', ', do not',
                     'you must make the code readable']

        fieldnames = ['line', 'user', 'body']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)

        engs = dict()

        for row in reader:
            user = row['user']
            body = row['body'].lower()
            if ('jenkins' in user) or ('github' in user) or ('mlx3im' in user):
                continue

            # Create user if new or increment lines if known
            if user in engs:
                engs[user].inc_comments()
            else:
                engs[user] = Engineer(user)

            eng = engs[user]

            # check pos words
            for pos in positives:
                if pos in body:
                    eng.pos_found(body)
            if customized_pos(body):
                eng.pos_found(body)

            # check neg words
            for neg in negatives:
                if neg in body:
                    eng.neg_found(body)
            if customized_neg(body):
                eng.neg_found(body)

        i = 0
        for u, e in engs.items():
            e.dump(af)

        header = "\nHighest negative ratio"
        print(header)
        af.write("{s}\n".format(s=header))
        i = 1
        neg_l = sorted(engs, key=lambda name: engs[name].neg_rate())
        neg_l.reverse()
        for key in neg_l:
            if engs[key].comments_cnt() > 50:
                txt = "{id}) {u}: {n:.2f} ({l})".format(id=i, u=key, n=100*engs[key].neg_rate(), l=engs[key].comments)
                print(txt)
                af.write("{s}\n".format(s=txt))
                i += 1

        header = "\nHighest positive ratio"
        print(header)
        af.write("{s}\n".format(s=header))
        i = 1
        pos_l = sorted(engs, key=lambda name: engs[name].pos_rate())
        pos_l.reverse()
        for key in pos_l:
            if engs[key].comments_cnt() > 50:
                txt = "{id}) {u}: {n:.2f} ({l})".format(id=i, u=key, n=100 * engs[key].pos_rate(), l=engs[key].comments)
                print(txt)
                af.write("{s}\n".format(s=txt))
                i += 1

    af.close()

    return engs
