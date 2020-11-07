#!/usr/bin/python3

# importing the requests library
import json
import requests
import re

#repo_owner = "intel"
# repo_name = "compute-runtime"
# owner = "snimrod"
# repo = "TestForComments"
repo_owner = "v3io"
repo_name = "frames"
# repo_name = "storey"
pr_num = ""
# dtype = "reviews"
dtype = "comments"
pageLines = 100
UPREF = "https://api.github.com/repos/"
FAIL = - 1


def handle_page(owner, repo, pr, page):
    URL = "{pre}{own}/{rep}/pulls/{pull}comments?page={p}&per_page={pl}".format(pre=UPREF, own=owner, rep=repo,
                                                                                pull=pr, p=page, pl=pageLines)
    r = requests.get(url = URL)
    if r.status_code != 200:
        print("Page {n} failed! (code={c}) (url={u}) (error={er})".format(n=page, c=r.status_code, u=URL, er=r.reason))
        return FAIL

    cnt = len(r.json())
    if cnt == 0:
        return cnt

    for p_num in range(cnt):
        body = re.sub(r"[^' '-}'\n']+", ' ', r.json()[p_num]['body'].replace(",", " "))
        body = re.sub("\n|\r", " ", body)
        user = r.json()[p_num]['user']['login']
        str = '{idx},{who},{what}'.format(idx=((page - 1) * pageLines) + p_num + 1, who=user, what=body)
        output.write(str + '\n')

    print("Page {n} - Done".format(n=page))
    return cnt


def handle_repo(owner, repo, pr):

    if len(pr) > 0:
        pr = "{pull}/".format(pull=pr)

    print("Retrieving data for {o}/{r}...".format(o=owner, r=repo))
    page = 1
    cnt = handle_page(owner, repo, pr, page)
    total_cnt = cnt
    while cnt > 0:
        page = page + 1
        cnt = handle_page(owner, repo, pr, page)
        total_cnt += cnt

    if cnt == 0:
        print("Retrieved {c} comments in {p} pages".format(c=total_cnt, p=(page-1)))
    else:
        print("Stopped due to failure on page {p}".format(p=page))

# def main():
# fname = "{own}_{rep}.json".format(rep=repo, own=owner)
output = open("output.csv", "w")
handle_repo(repo_owner, repo_name, pr_num)
output.close()


#if __name__ == "__main__":
#    main()