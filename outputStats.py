import csv
from engineer import Engineer


def d_val(d, key):
    if key in d:
        return d[key]
    else:
        return 0


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
    af.write('User,Comments,Positive words, negative words\n')
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
        pos_words = dict()
        neg_words = dict()
        lines = dict()
        lengths = dict()

        engs = dict()

        for row in reader:
            user = row['user']
            body = row['body'].lower()
            if ('jenkins' in user) or ('github' in user) or ('mlx3im' in user):
                continue

            # +1 to user lines
            if user in lines.keys():
                lines[user] += 1
                lengths[user] += len(body)
            else:
                lines[user] = 1
                lengths[user] = len(body)

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
                    if user in pos_words.keys():
                        pos_words[user] += 1
                    else:
                        pos_words[user] = 1
            if customized_pos(body):
                eng.pos_found(body)
                if user in pos_words.keys():
                    pos_words[user] += 1
                else:
                    pos_words[user] = 1

            # check neg words
            for neg in negatives:
                if neg in body:
                    eng.neg_found(body)
                    if user in neg_words.keys():
                        neg_words[user] += 1
                    else:
                        neg_words[user] = 1
            if customized_neg(body):
                eng.neg_found(body)
                if user in neg_words.keys():
                    neg_words[user] += 1
                else:
                    neg_words[user] = 1

        # dump summary
        neg_d = dict()
        pos_d = dict()
        for u_id in lines.keys():
            if lines[u_id] > 50:
                neg_d[u_id] = 100*d_val(neg_words, u_id)/lines[u_id]
                pos_d[u_id] = 100*d_val(pos_words, u_id)/lines[u_id]

            pref = "{u},{c},{p_w},{p_p:.2f},{n_w},{n_p:.2f},{a_l}".format(u=u_id, c=lines[u_id],
                                                                          p_w=d_val(pos_words, u_id),
                                                                          p_p=d_val(pos_d, u_id),
                                                                          n_w=d_val(neg_words, u_id),
                                                                          n_p=d_val(neg_d, u_id),
                                                                          a_l=int(lengths[u_id]/lines[u_id]))
            print(pref)
            af.write(pref+'\n')

        neg_l = sorted(neg_d.items(), key=lambda item: item[1])
        neg_l.reverse()
        header = "\nHighest negative ratio"
        print(header)
        af.write("{s}\n".format(s=header))
        i = 1
        for neg in neg_l:
            txt = "{id}) {u} - {n:.2f} ({l})".format(id=i, u=neg[0], n=neg[1], l=lines[neg[0]])
            print(txt)
            af.write("{s}\n".format(s=txt))
            i += 1

        pos_l = sorted(pos_d.items(), key=lambda item: item[1])
        pos_l.reverse()
        header = "\nHighest positive ratio"
        print(header)
        af.write("{s}\n".format(s=header))
        i = 1
        for pos in pos_l:
            txt = "{id}) {u} - {n:.2f} ({l})".format(id=i, u=pos[0], n=pos[1], l=lines[pos[0]])
            print(txt)
            af.write("{s}\n".format(s=txt))
            i += 1

        af.close()
