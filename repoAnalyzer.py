#!/usr/bin/python3

# importing the requests library
import json
import os
import requests
import re
from outputStats import analyze_csv
from queryMgr import handle_query

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
USER = os.environ.get('MYUSER')
TOKEN = os.environ.get('PAT')


def retrieve_page(owner, repo, page, f, issues, start_line):
    if issues:
        req_url = "{pre}{own}/{rep}/issues/comments?page={p}&per_page={pl}".format(pre=UPREF, own=owner, rep=repo,
                                                                               p=page, pl=pageLines)
    else:
        req_url = "{pre}{own}/{rep}/pulls/comments?page={p}&per_page={pl}".format(pre=UPREF, own=owner, rep=repo,
                                                                                  p=page, pl=pageLines)
    r = requests.get(url=req_url, auth=(USER, TOKEN))

    if r.status_code == 403:
        print("Got rate limit error on {o}/{r} - page {p}".format(o=owner, r=repo, p=page))
        return 0

    if r.status_code != 200:
        print("Page {n} failed! (code={c}) (url={u}) (error={er})".format(n=page, c=r.status_code, u=req_url,
                                                                          er=r.reason))
        return FAIL

    cnt = len(r.json())
    if cnt == 0:
        return cnt

    print(r.json())

    for p_num in range(cnt):
        body = re.sub(r"[^' '-}'\n']+", ' ', r.json()[p_num]['body'].replace(",", " "))
        body = re.sub("\n|\r", " ", body)
        user = r.json()[p_num]['user']['login']
        str = '{idx},{who},{what}'.format(idx=((page - 1) * pageLines) + p_num + 1 + start_line, who=user, what=body)
        f.write(str + '\n')

    print("Page {n} - Done".format(n=page))
    return cnt


def retrieve_all_pages(owner, repo, f, issues, start_line):
    page = 1
    cnt = retrieve_page(owner, repo, page, f, issues, start_line)
    total_cnt = cnt
    while cnt > 0:
        page = page + 1
        cnt = retrieve_page(owner, repo, page, f, issues, start_line)
        total_cnt += cnt

    if cnt == 0:
        print("Retrieved {c} comments in {p} pages".format(c=total_cnt, p=(page - 1)))
    else:
        print("Stopped due to failure on page {p}".format(p=page))

    return total_cnt


def retrieve_repo(owner, repo):
    fname = "{o}_{r}.csv".format(o=owner, r=repo)
    f = open(fname, "w")
    f.write("Id,User,Comment\n")
    print("Retrieving pulls comments for {o}/{r}...".format(o=owner, r=repo))
    comments = retrieve_all_pages(owner, repo, f, 0, 0)
    print("Retrieving issues comments for {o}/{r}...".format(o=owner, r=repo))
    comments += retrieve_all_pages(owner, repo, f, 1, comments)
    print("Retrieved total of {n} comments for {o}/{r}".format(o=owner, r=repo, n=comments))
    f.close()


def append_page_repos(owner, repos, page):
    req_url = "https://api.github.com/orgs/{o}/repos?page={p}&per_page={pp}".format(o=owner, p=page, pp=pageLines)
    r = requests.get(url=req_url, auth=(USER, TOKEN))
    cnt = len(r.json())
    print(cnt)
    for p_num in range(cnt):
        # print(r.json()[p_num])
        repos.append(r.json()[p_num]['name'])
    return cnt


def get_owner_repos_list(owner):
    repos = []
    page = 1
    cnt = append_page_repos(owner, repos, page)
    while cnt > 0:
        page += 1
        cnt = append_page_repos(owner, repos, page)

    return repos


def retrieve_owner(owner):
    repos = get_owner_repos_list(owner)
    print(len(repos))
    print(repos)
    # for repo in repos:
    #     retrieve_repo(owner, repo, f)
    # retrieve_repo(owner, 'nvmx')


def req_test(req_url):
    r = requests.get(url=req_url, auth=(USER, TOKEN))
    # cnt = len(r.json())
    # print(cnt)
    print(r.json())

# 'Accept': 'text/csv',


def watson_test():
    headers = {
        'Content-Type': 'text/plain;charset=utf-8',
        'Accept': 'application/json',
    }

    # params = (
    #     ('version', '2017-10-13'),
    # )

    params = (
        ('version', '2017-10-13'),
        ('consumption_preferences', 'true'),
        ('raw_scores', 'true'),
    )

    data = open('jgunthorpe_comments.txt', 'rb').read()
    response = requests.post('https://api.eu-gb.personality-insights.watson.cloud.ibm.com/instances/1053e341-43be-4f0c-a0c5-a12e251a182c/v3/profile', headers=headers, params=params, data=data, auth=('apikey', 'MauyFCwIWSYKbJ5ynsvxBGRuPl0prAgA2aV091GTRhpI'))
    my_data = response.json()
    print(response)
    with open('jason_raw.json', 'w') as f:
        json.dump(my_data, f)

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.post('https://api.eu-gb.personality-insights.watson.cloud.ibm.com/instances/1053e341-43be-4f0c-a0c5-a12e251a182c/v3/profile?version=2017-10-13', headers=headers, data=data, auth=('apikey', 'MauyFCwIWSYKbJ5ynsvxBGRuPl0prAgA2aV091GTRhpI'))


# def main():
# fname = "{own}_{rep}.json".format(rep=repo, own=owner)
# output = open("output.csv", "w")
# retrieve_repo(repo_owner, repo_name)
# output.close()
# req_test("https://api.github.com/orgs/v3io/frames?page=1&per_page=100")
# req_test("https://api.github.com/repos/Mellanox/nvmx/pulls/comments")
# retrieve_owner("intel")
# retrieve_repo('intel', 'compute-runtime')
# retrieve_repo('v3io', 'frames')
#retrieve_repo('spdk', 'spdk')
#analyze_csv('intel_compute-runtime.csv')
#analyze_csv('v3io_frames.csv')
#d = analyze_csv('openucx_ucx.csv')
#analyze_csv('Mellanox_spdk.csv')
#d = analyze_csv('Mellanox.csv')
#d = analyze_csv('linux-rdma_rdma-core.csv')


watson_test()


#print('\nq to quit, h for help')
#cmd = input('>>> ')
#while cmd != 'q':
#    handle_query(d, cmd)
#    cmd = input('>>> ')

# if __name__ == "__main__":
#    main()
