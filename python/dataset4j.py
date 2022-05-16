from __future__ import annotations

from datetime import date

from pandas import DataFrame

from common.commons import *
from commitCollector import *
from settings import *

from otherDatasets import markBugFixingPatches, prepareFiles


DATASET_PATH = Path(REPO_PATH)
DATASET = os.environ["dataset"]
PROJECT_LIST = os.environ["PROJECT_LIST"]


def load_commits(repo: str, git_url: str, branch: str) -> DataFrame:
    """
    Load commits of a repo

    :param repo: Repo name (e.g. "fuse")
    :param git_url: Git clone url (e.g. "https://github.com/jboss-fuse/fuse.git")
    :param branch: Git branch (e.g. "6.3.0.redhat")
    :return: Commits DataFrame
    """
    commits_pickle = Path(join(COMMIT_DFS, f'{repo}-fix.pickle.gz'))

    # Load existing commits
    if commits_pickle.is_file():
        return pd.read_pickle(commits_pickle)

    # Clone new commits
    if not (DATASET_PATH / repo).exists():
        shellCallTemplate('git config --global http.postBuffer 157286400')
        shellCallTemplate(f'git -C {DATASET_PATH} clone {git_url}')
        logging.info(f'Git repo cloned: {repo}')

    commits = getCommitFromRepo(join(REPO_PATH, repo), join(COMMIT_DFS, repo), branch)
    commits = markBugFixingPatches(commits, repo)
    commits.to_pickle(commits_pickle)

    return commits


def create_dataset(cfg: dict, project_list: str = PROJECT_LIST):
    """
    Create dataset

    :param cfg: config.yml dictionary
    :param project_list: Comma-separated list of git project names (projects must exist in dataset.csv)
    :return:
    """
    pj_list: list[str] = project_list.split(',')

    # Ensure directories exist
    DATASET_PATH.mkdir(exist_ok=True, parents=True)
    if not os.path.exists(COMMIT_DFS):
        os.mkdir(COMMIT_DFS)

    # Find project repo urls in dataset.csv
    dataset: DataFrame = pd.read_csv(join(ROOT_DIR, 'data', 'dataset.csv'))
    if pj_list == ['ALL']:
        repos = dataset[['Repo', 'GitRepo', 'Branch']].values.tolist()
    else:
        repos = dataset[dataset.Repo.isin(pj_list)][['Repo', 'GitRepo', 'Branch']].values.tolist()

    # Loop through repos
    for repo, src, branch in repos:
        print(f'Processing {repo}')
        commits = load_commits(repo, src, branch)
        print(f'> Obtained {len(commits)} commits.')

        # keep only commits that has moves
        commits = commits[[any(c == 'M' for c in dic.values()) for dic in commits.files]]
        # keep only commits that are changing java files (.java)
        commits = commits[[all(k.endswith('.java') for k in dic) for dic in commits.files]]
        # not a revert commit
        # commits = commits[~commits.log.apply(lambda x: x.startswith('Revert'))]
        # commits = commits[commits.files.apply(lambda x: len(x) == 1)]
        # commits['cocci'] = commits.log.apply(lambda x: True if re.search('cocci|coccinelle', x) else False)
        # coccis = commits[commits.cocci].commit.values.tolist()
        fixes = commits[commits.fixes.str.len() != 0].commit.values.tolist()

        # Filter end dates if configured
        if 'limitCommitsBeforeDays' in cfg['fixminer']:
            value = eval(str(cfg['fixminer']['limitCommitsBeforeDays']))
            latest_commit = commits.commitDate.iloc[0]

            if isinstance(value, datetime.timedelta):
                end_date = latest_commit - value
            elif isinstance(value, float) or isinstance(value, int):
                end_date = latest_commit - datetime.timedelta(days=value)
            else:
                raise NotImplementedError(f'Unknown limitCommitsBeforeDays type: {type(value)}. '
                                          f'Only timedelta and int/float (days) are supported.')

            print(f'> Has {len(commits)} commits before filtering for date < {end_date}')
            commits = commits[commits.commitDate < end_date]

        commits = commits[commits.commit.isin(fixes)]
        print(f'> Has {len(commits)} comments after filtering')

        parallelRun(prepareFiles, commits[['commit', 'files']].values.tolist(), repo)
