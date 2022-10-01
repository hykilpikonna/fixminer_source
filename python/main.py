from __future__ import annotations

import inspect
import requests

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


def job_start_redis(db_dir: str | Path | None = None, redis_port: int | None = None,
                    root_dir: str | Path | None = None):
    db_dir = db_dir or join(DATA_PATH, 'redis')
    redis_port = redis_port or REDIS_PORT or 6399
    root_dir = root_dir or Path(__file__).parent

    redis_shutdown(redis_port)
    print(db_dir)
    redis_start(root_dir, db_dir, redis_port)


def job_richedit():
    job_start_redis()
    cmd = f"JAVA_HOME='{jdk8}' java -jar '{JAR_PATH}' {args.prop} RICHEDITSCRIPT"
    print(f"Running command: {cmd}")
    output = os.system(cmd)
    logging.info(output)


def job_actionSI():
    from pairs import actionPairs, createPairs, importAction

    job_start_redis()
    matches = actionPairs()
    createPairs(matches)
    importAction()


def job_compare():
    job_start_redis()
    cmd = f"JAVA_HOME='{jdk8}' java -jar '{JAR_PATH}' {args.prop} COMPARE"
    output = shellCallTemplate4jar(cmd)
    logging.info(output)


def job_cluster():
    from abstractPatch import cluster

    job_start_redis()
    cluster(join(DATA_PATH, 'actions'), join(DATA_PATH, 'pairs'), 'actions')


def job_tokenSI():
    from pairs import tokenPairs, importTokens

    tokenPairs()
    importTokens()


def job_clusterTokens():
    from abstractPatch import cluster

    dbDir = join(DATA_PATH, 'redis')
    redis_start(dbDir, REDIS_PORT, PROJECT_TYPE)
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


def job_patternOperations():
    from sprinferIndex import patternOperations

    patternOperations()


def job_patchManyBugs():
    from patchManyBugs import buildAll

    buildAll()


def job_patchIntro():
    from sprinferIndex import patchCoreIntro

    patchCoreIntro()


def job_validateIntro():
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
