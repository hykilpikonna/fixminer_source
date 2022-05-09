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
    content = Path(file).read_text().replace("\n", ",")
    commits = json.loads(f'[{content}]')

    # Convert to DataFrame
    ds = pd.DataFrame.from_dict(commits)
    ds['commitDate'] = pd.to_datetime(ds['commitDate'])
    return ds
