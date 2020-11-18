import csv
from engineer import Engineer


def print_str_usage_histogram(f, word):
    with open(f, newline='') as csvfile:
        fieldnames = ['line', 'user', 'body']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        d = dict()
        lines = dict()
        # row_count = sum(1 for row in reader)  # fileObject is your csv.reader
        for row in reader:
            # +1 to user lines
            if row['user'] in lines.keys():
                lines[row['user']] += 1
            else:
                lines[row['user']] = 1

            # +1 to user usage of this word
            if word in row['body'].lower():
                if row['user'] in d.keys():
                    d[row['user']] += 1
                else:
                    d[row['user']] = 1

        for k in lines.keys():
            if k in d.keys():
                d_cnt = d[k]
            else:
                d_cnt = 0
            pref = "{n} {c} {l} ".format(n=k, c=d_cnt, l=lines[k])
            print(pref + "{:.2f}".format(100 * d_cnt / lines[k]))


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

            # check pos words
            for pos in positives:
                if pos in body:
                    # if user == 'vasilyMellanox':
                    #     af.write("{x},{y}\n".format(x=user, y=body))
                    if user in pos_words.keys():
                        pos_words[user] += 1
                    else:
                        pos_words[user] = 1
            if customized_pos(body):
                # if user == 'vasilyMellanox':
                # af.write("{x},{y}\n".format(x=user, y=body))
                if user in pos_words.keys():
                    pos_words[user] += 1
                else:
                    pos_words[user] = 1

            # check neg words
            for neg in negatives:
                if neg in body:
                    # print(user, body)
                    if user in neg_words.keys():
                        neg_words[user] += 1
                    else:
                        neg_words[user] = 1
            if customized_neg(body):
                # print(user, body)
                # af.write("{u},{b}\n".format(u=user, b=body))
                if user in neg_words.keys():
                    neg_words[user] += 1
                else:
                    neg_words[user] = 1

        # dump summary
        neg_d = dict()
        pos_d = dict()
        for u_id in lines.keys():
            # if (lines[u_id] > 50) and (d_val(neg_words, u_id) > 0):
            if lines[u_id] > 50:
                neg_d[u_id] = 100*d_val(neg_words, u_id)/lines[u_id]

            # if (lines[u_id] > 50) and (d_val(pos_words, u_id) > 0):
            if lines[u_id] > 50:
                pos_d[u_id] = 100*d_val(pos_words, u_id)/lines[u_id]

            # print(d_val(pos_d, u_id))
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
        for eng in neg_l:
            txt = "{id}) {u} - {n:.2f} ({l})".format(id=i, u=eng[0], n=eng[1], l=lines[eng[0]])
            print(txt)
            af.write("{s}\n".format(s=txt))
            i += 1

        pos_l = sorted(pos_d.items(), key=lambda item: item[1])
        pos_l.reverse()
        header = "\nHighest positive ratio"
        print(header)
        af.write("{s}\n".format(s=header))
        i = 1
        for eng in pos_l:
            txt = "{id}) {u} - {n:.2f} ({l})".format(id=i, u=eng[0], n=eng[1], l=lines[eng[0]])
            print(txt)
            af.write("{s}\n".format(s=txt))
            i += 1

        af.close()
