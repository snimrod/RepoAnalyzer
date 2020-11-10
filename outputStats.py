import csv


def print_str_usage_histogram(word):
    with open('Mellanox.csv', newline='') as csvfile:
        fieldnames = ['line', 'user', 'body']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        d = dict()
        lines = dict()
        # row_count = sum(1 for row in reader)  # fileObject is your csv.reader
        for row in reader:
            if row['user'] in lines.keys():
                lines[row['user']] += 1
            else:
                lines[row['user']] = 1
            if word in row['body'].lower():
                if row['user'] in d.keys():
                    d[row['user']] += 1
                else:
                    d[row['user']] = 1
                # print(row['body'], row['line'])
        for k in lines.keys():
            if k in d.keys():
                d_cnt = d[k]
            else:
                d_cnt = 0
            pref = "{n} {c} {l} ".format(n=k, c=d_cnt, l=lines[k])
            print(pref + "{:.2f}".format(100 * d_cnt / lines[k]))


print_str_usage_histogram('right?')
