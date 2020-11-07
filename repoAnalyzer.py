#!/usr/bin/python3

# importing the requests library
import json
import requests
import re
import time

repo_owner = "intel"
repo_name = "compute-runtime"
# owner = "snimrod"
# repo = "TestForComments"
# repo_owner = "v3io"
# repo_name = "frames"
# repo_name = "storey"
pageLines = 100
UPREF = "https://api.github.com/repos/"
FAIL = - 1


def retrieve_page(owner, repo, page, issues):
    if issues:
        req_url = "{pre}{own}/{rep}/issues/comments?page={p}&per_page={pl}".format(pre=UPREF, own=owner, rep=repo,
                                                                               p=page, pl=pageLines)
    else:
        req_url = "{pre}{own}/{rep}/pulls/comments?page={p}&per_page={pl}".format(pre=UPREF, own=owner, rep=repo,
                                                                              p=page, pl=pageLines)
    r = requests.get(url=req_url)

    if r.status_code == 403:
        print("Got rate limit error, sleeping and retrying")
        time.sleep(1.1)
        r = requests.get(url=req_url)

    if r.status_code != 200:
        print("Page {n} failed! (code={c}) (url={u}) (error={er})".format(n=page, c=r.status_code, u=req_erl,
                                                                          er=r.reason))
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


def retrieve_all_pages(owner, repo, issues):
    page = 1
    cnt = retrieve_page(owner, repo, page, issues)
    total_cnt = cnt
    while cnt > 0:
        page = page + 1
        cnt = retrieve_page(owner, repo, page, issues)
        total_cnt += cnt

    if cnt == 0:
        print("Retrieved {c} comments in {p} pages".format(c=total_cnt, p=(page - 1)))
    else:
        print("Stopped due to failure on page {p}".format(p=page))

    return total_cnt


def handle_repo(owner, repo):
    print("Retrieving pulls comments for {o}/{r}...".format(o=owner, r=repo))
    comments = retrieve_all_pages(owner, repo, 0)
    print("Retrieving issues comments for {o}/{r}...".format(o=owner, r=repo))
    comments += retrieve_all_pages(owner, repo, 1)
    print("Retrieved total of {n} comments for {o}/{r}".format(o=owner, r=repo, n=comments))


# def main():
# fname = "{own}_{rep}.json".format(rep=repo, own=owner)
output = open("output.csv", "w")
handle_repo(repo_owner, repo_name)
output.close()

# if __name__ == "__main__":
#    main()
