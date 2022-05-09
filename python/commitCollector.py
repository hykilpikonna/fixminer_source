import json

import pandas as pd

from common.commons import *

REPO_PATH = os.environ["REPO_PATH"]
DATA_PATH = os.environ["DATA_PATH"]
COMMIT_DFS = os.environ["COMMIT_DFS"]
COMMIT_FOLDER = os.environ["COMMIT_FOLDER"]


def getCommitFromRepo(f: PathLike, gitrepo: str, branch: str):
    """

    :param f: Git repo directory
    :param gitrepo: Repo name
    :param branch: Branch name
    :return: None
    """
    file = f'{gitrepo}.commits'
    output, err = shellGitCheckout(f'git -C {f} checkout -f {branch}')
    m = re.search(branch, err)

    while not m:
        time.sleep(10)
        logging.info('Waiting for checkout')

    # Create commits file
    form = json.dumps({"commit": "%H", "commitDate": "%ci", "title": "%f", "committer": "%ce"})
    shellCallTemplate(f"git -C {f} log --no-merges --pretty=format:'{form}' > {file}", enc='latin1')

    # Collect commits
    commits = json.loads(f'[{Path(file).read_text()}]')

    # Convert to DataFrame
    ds = pd.DataFrame.from_dict(commits)
    ds['commitDate'] = pd.to_datetime(ds['commitDate'])
    return ds


def caseCollect(subject):
    if not os.path.exists(COMMIT_FOLDER):
        os.mkdir(COMMIT_FOLDER)
    if not os.path.exists(COMMIT_DFS):
        os.mkdir(COMMIT_DFS)

    subjects = pd.read_csv(join(DATA_PATH, 'subjects.csv'))
    if subject == 'ALL':
        tuples = subjects[['Repo', 'Branch']].values.tolist()
    else:
        # repos = subjects.query("Subject == '{0}'".format(subject)).Repo.tolist()
        tuples = subjects.query("Subject == '{0}'".format(subject))[
            ['Repo', 'Branch']].values.tolist()

    for t in tuples:
        repo, branch = t
        logging.info(repo)
        getCommitFromRepo(join(REPO_PATH, repo), join(COMMIT_FOLDER, repo), branch)

    if subject == 'ALL':
        commits = listdir(COMMIT_FOLDER)
    else:
        commits = [i for i in listdir(COMMIT_FOLDER) if i.startswith(repo)]

    for commit in commits:
        logging.info(commit)
        rDF = makeDF(join(COMMIT_FOLDER, commit))
        repoName = commit.split('.')[0]
        save_zipped_pickle(rDF, join(COMMIT_DFS, repoName + ".pickle"))
        # p.dump(rDF, open(join(COMMIT_DFS, repoName + ".pickle"), "wb"))


def caseClone(subject):
    if not os.path.exists(REPO_PATH):
        os.mkdir(REPO_PATH)

    subjects = pd.read_csv(join(DATA_PATH, 'subjects.csv'))
    if subject == 'ALL':
        gitrepos = subjects.GitRepo.tolist()
    else:
        gitrepos = subjects.query("Subject == '{0}'".format(subject)).GitRepo.tolist()
    os.getcwd()
    os.chdir(REPO_PATH)
    for gitrepo in gitrepos:
        cmd = 'git clone ' + gitrepo
        out = shellCallTemplate(cmd)
