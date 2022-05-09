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


def filter_commits(commits: DataFrame, end_date: date) -> DataFrame:
    return commits[commits.commitDate < end_date]


def createDS(project_list: str = PROJECT_LIST):
    """

    :param project_list: Comma-separated list of git project names (projects must exist in dataset.csv)
    :return:
    """
    pjList: list[str] = project_list.split(',')

    # Ensure directories exist
    DATASET_PATH.mkdir(exist_ok=True)
    if not os.path.exists(COMMIT_DFS):
        os.mkdir(COMMIT_DFS)

    # Find project repo urls in dataset.csv
    subjects: DataFrame = pd.read_csv(join(ROOT_DIR, 'data', 'dataset.csv'))
    if pjList == ['ALL']:
        tuples = subjects[['Repo', 'GitRepo', 'Branch']].values.tolist()
    else:
        tuples = subjects[subjects.Repo.isin(pjList)][['Repo', 'GitRepo', 'Branch']].values.tolist()

    # Loop through repos
    for repo, src, branch in tuples:
        logging.info(f'Processing {repo}')
        commits = load_commits(repo, src, branch)

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
        # links = commits[commits.links.str.len()!=0].commit.values.tolist()

        # bugs = set(fixes).union(links).union(coccis)
        # bugs = set(fixes)#.union(coccis)
        commits = commits[commits.commit.isin(fixes)]
        print(len(commits))
        # for s in a.commit.values.tolist():
        parallelRun(prepareFiles, commits[['commit', 'files']].values.tolist(), repo)

    # # if job == 'clone':
    # for repo,src in subjects[['Repo','GitRepo']].values.tolist():
    #     if(pjList != ['ALL']):
    #         if repo in pjList:
    #             print(repo)
    #             cmd = 'git -C ' + DATASET_PATH + ' clone ' + src
    #             shellCallTemplate(cmd)
    #             logging.info(repo)

    # caseClone(subject)

    # caseCollect(subject)
    # # elif job == 'fix':
    # from filterBugFixingCommits import caseFix
    #
    # caseFix(subject)
    # #
    # # # elif job =='brDownload':
    # from bugReportDownloader import caseBRDownload
    #
    # caseBRDownload(subject)
    # # # elif job =='brParser':
    # from bugReportParser import step1
    #
    # step1(subject)
    #
    # # elif job =='dataset':
    #
    # if not isfile(join(DATA_PATH, 'singleBR.pickle')):
    #
    #     brs = load_zipped_pickle(join(DATA_PATH, subject + "bugReportsComplete.pickle"))
    #
    #     subjects = pd.read_csv(join(DATA_PATH, 'subjects.csv'))
    #
    #
    #     def getCommit(x):
    #         bid, project = x
    #
    #         subjects = pd.read_csv(join(DATA_PATH, 'subjects.csv'))
    #         repo = subjects.query("Subject == '{0}'".format(project)).Repo.tolist()[0]
    #         commits = load_zipped_pickle(join(DATA_PATH, COMMIT_DFS, repo + '.pickle'))
    #         correspondingCommit = commits.query("fix =='{0}'".format(bid)).commit.tolist()
    #         if len(correspondingCommit) == 1:
    #             return [bid, correspondingCommit[0], project]
    #         else:
    #             return None
    #             print('error')
    #
    #
    #     wl = brs[['bid', 'project']].values.tolist()
    #     dataL = parallelRunMerge(getCommit, wl)
    #
    #     commits = pd.DataFrame(
    #         columns=['bid', 'commit', 'project'],
    #         data=list(filter(None.__ne__, dataL)))
    #
    #     save_zipped_pickle(commits, join(DATA_PATH, 'singleBR.pickle'))
    # else:
    #     commits = load_zipped_pickle(join(DATA_PATH, 'singleBR.pickle'))
    #     subjects = pd.read_csv(join(DATA_PATH, 'subjects.csv'))
    # logging.info('done matching commits')
    # commits['repo'] = commits.project.apply(lambda x: subjects.query("Subject == '{0}'".format(x)).Repo.tolist()[0])
    #
    # workList = commits[['commit', 'repo']].values.tolist()
    # from dataset import prepareFiles
    #
    # parallelRun(prepareFiles, workList)
