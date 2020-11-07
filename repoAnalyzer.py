#!/usr/bin/python3

# importing the requests library
import json
import requests
import re

# owner = "intel"
# repo = "compute-runtime"
# owner = "snimrod"
# repo = "TestForComments"
owner = "v3io"
# repo = "frames"
repo = "storey"
pr = ""
# dtype = "reviews"
dtype = "comments"
pageLines = 100


def handle_page(owner, repo, pr, dtype, page):
    if len(pr) > 0:
        pr = "{pull}/".format(pull = pr)

    URL = "https://api.github.com/repos/{own}/{rep}/pulls/{pull}{type}?page={p}&per_page={pl}".format(own = owner, rep = repo, pull = pr, type = dtype, p = page, pl = pageLines)
    print(URL)
    r = requests.get(url = URL)

    print(r.status_code)
    cnt = len(r.json())
    print (cnt)

    for i in range(cnt):
        body = re.sub(r"[^' '-}'\n']+", ' ', r.json()[i]['body'].replace(","," "))
        body = re.sub("\n|\r", " ", body)
        user = r.json()[i]['user']['login']
        str = '{idx},{who},{what}'.format(idx=((page - 1) * pageLines) + i + 1, who=user, what=body)
        output.write(str + '\n')
    return cnt

# api-endpoint
# URL = "https://api.github.com/repos/{own}/{rep}/pulls/{pull}{type}
# ?page={p}&per_page=100".format(own = owner, rep = repo, pull = pr, type = dtype, p = page)
# URL = "https://api.github.com/repos/v3io/frames/pulls/comments?page=5&per_page=110"
# URL = "https://api.github.com/repos/intel/compute-runtime/pulls/239/comments?page=1&per_page=100"
# URL = "https://api.github.com/repos/intel/compute-runtime/pulls/239/reviews?page=1&per_page=100"
# URL = "https://api.github.com/repos/intel/compute-runtime/pulls/256/comments"
# URL = "https://api.github.com/repos/intel/compute-runtime/comments"
# URL = "https://api.github.com/repos/intel/compute-runtime/issues/comments"

# URL = "https://api.github.com/repos/Mellanox/ucx/pulls/comments"
# URL = "https://api.github.com/repos/snimrod/TestForComments/pulls/reviews"
# URL = "https://api.github.com/repos/intel/compute-runtime/pulls/256/reviews"
# sending get request and saving the response as response object


output = open("output.csv", "w")

i = 1
while handle_page(owner, repo, pr, dtype, i) > 0:
    i = i + 1

output.close()

# print(r.content)

# extracting data in json format
# data = r.json()

# fname = "{own}_{rep}.json".format(rep=repo, own=owner)

# with open(fname, 'w') as f:
#        json.dump(data, f)

# print(data)
