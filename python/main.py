import inspect

from common.commons import *
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('prop', help='config.yml file path')
    parser.add_argument('job', help='job name')

    args = parser.parse_args()

    # Automatically set root to be the path of the current file
    args.root = str(Path(__file__).parent.absolute())

    if args.root is None or args.job is None or args.prop is None:
        parser.print_help()
        exit(-1)
    return args


def job_dataset4j():
    from dataset4j import create_dataset

    create_dataset(cfg)


def job_dataset4c():
    from otherDatasets import core

    core()


def job_richedit():
    dbDir = join(DATA_PATH, 'redis')
    stopDB(dbDir, REDIS_PORT)
    cmd = f"JAVA_HOME='{jdk8}' java -jar '{JAR_PATH}' {args.prop} RICHEDITSCRIPT "
    output = shellCallTemplate(cmd)
    logging.info(output)


def job_actionSI():
    from pairs import actionPairs, createPairs, importAction

    matches = actionPairs()
    createPairs(matches)
    importAction()


def job_compare():
    # cmd = "mvn exec:java -f '/data/fixminer_source/'
    # -Dexec.mainClass='edu.lu.uni.serval.richedit.akka.compare.CompareTrees'
    # -Dexec.args='"+ " shape " + join(DATA_PATH,"redis") +" ALLdumps-gumInput.rdb " +
    # "clusterl0-gumInputALL.rdb /data/richedit-core/python/data/richEditScript'"
    cmd = f"JAVA_HOME='{jdk8}' java -jar '{JAR_PATH}' {args.prop} COMPARE "
    output = shellCallTemplate4jar(cmd)
    logging.info(output)


def job_cluster():
    from abstractPatch import cluster

    dbDir = join(DATA_PATH, 'redis')
    startDB(dbDir, REDIS_PORT, PROJECT_TYPE)
    cluster(join(DATA_PATH, 'actions'), join(DATA_PATH, 'pairs'), 'actions')


def job_tokenSI():
    from pairs import tokenPairs, importTokens

    tokenPairs()
    importTokens()


def job_clusterTokens():
    from abstractPatch import cluster

    dbDir = join(DATA_PATH, 'redis')
    startDB(dbDir, REDIS_PORT, PROJECT_TYPE)
    cluster(join(DATA_PATH, 'tokens'), join(DATA_PATH, 'pairsToken'), 'tokens')


def job_codeflaws():
    from otherDatasets import codeflaws

    codeflaws()


def job_indexClusters():
    from sprinferIndex import runSpinfer, test, divideCoccis, removeDuplicates

    runSpinfer()
    test()
    divideCoccis()
    removeDuplicates()

    # from patchManyBugs import patchCore
    # patchCore()
    # # from patchManyBugs import patched
    # # patched()
    # from patchManyBugs import exportSosPatches
    # exportSosPatches()
    # from validate_manybugs import validate
    #
    # validate()


def job_patternOperations():
    from sprinferIndex import patternOperations

    patternOperations()


def job_patchManyBugs():
    from patchManyBugs import buildAll

    buildAll()

    # from patchManyBugs import patchCore
    # patchCore()
    # # from patch_validate import patch_validate_mine
    # # patch_validate_mine()
    # from patchManyBugs import patched
    # patched()
    # from patchManyBugs import exportSosPatches
    # exportSosPatches()


def job_patchIntro():
    from sprinferIndex import patchCoreIntro

    patchCoreIntro()
    # from sprinferIndex import patched
    # patched()


def job_validateIntro():
    # from patch_validate_introClass2 import patch_validate
    # patch_validate()
    from test_patched_file import patch_validate

    patch_validate()


def job_checkCorrectIntro():
    from test_patched_file import checkCorrect

    checkCorrect()


def job_manybugs():
    from getManybugs import export

    export()


def job_validateMany():
    from patch_validate import patch_validate

    patch_validate()


def job_introclass():
    from getIntroClass import export

    export()


def job_stats():
    from stats import statsNormal

    statsNormal(True)


def job_datasetDefects4J():
    from defects4JDataset import core

    core()


def job_bug():
    from bugstats import bStats

    bStats()


def job_defects4j():
    from stats import defects4jStats

    defects4jStats()


def job_patterns():
    from stats import exportAbstractPatterns

    exportAbstractPatterns()


def job_pipeline():
    fs = [job_dataset4j, job_richedit, job_actionSI, job_compare, job_cluster, job_tokenSI,
          job_compare, job_stats, job_patterns]

    for i, f in enumerate(fs):
        print(f'Running {i + 1}: {f.__name__}...')
        f()


JOBS = {name[4:]: f for name, f in inspect.getmembers(sys.modules[__name__])
        if inspect.isfunction(f) and name.startswith('job_')}


if __name__ == '__main__':
    args = parse_args()
    setLogg()

    cfg, _ = setEnv(args)

    # Parse job
    job: str = args.job.strip()
    if job not in JOBS:
        print(f'Job "{job}" is not supported. Available jobs: {", ".join(JOBS.keys())}')
        exit(-1)

    from settings import *
    pd.options.mode.chained_assignment = None

    print(f'Executing {job}...')
    JOBS[job]()
