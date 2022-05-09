from common.commons import *

if __name__ == '__main__':
    args = getRun()
    setLogg()

    setEnv(args)

    job = args.job

    from python.settings import *
    # job = "cluster"
    pd.options.mode.chained_assignment = None

    # subject = 'ALL'
    # rootType = 'if'

    print(job)

    if job == 'dataset4j':
        from dataset4j import create_dataset

        create_dataset()

    elif job == 'dataset4c':
        from otherDatasets import core

        core()

    elif job == 'richedit':
        dbDir = join(DATA_PATH, 'redis')
        stopDB(dbDir, REDIS_PORT)
        cmd = f"JAVA_HOME='{jdk8}' java -jar {JAR_PATH} {args.prop} RICHEDITSCRIPT "
        output = shellCallTemplate(cmd)
        logging.info(output)

    elif job == 'actionSI':
        from pairs import actionPairs, createPairs, importAction

        matches = actionPairs()
        createPairs(matches)
        importAction()

    elif job == 'compare':
        # cmd = "mvn exec:java -f '/data/fixminer_source/'
        # -Dexec.mainClass='edu.lu.uni.serval.richedit.akka.compare.CompareTrees'
        # -Dexec.args='"+ " shape " + join(DATA_PATH,"redis") +" ALLdumps-gumInput.rdb " +
        # "clusterl0-gumInputALL.rdb /data/richedit-core/python/data/richEditScript'"
        cmd = f"JAVA_HOME='{jdk8}' java -jar {JAR_PATH} {args.prop} COMPARE "
        output = shellCallTemplate4jar(cmd)
        logging.info(output)

    elif job == 'cluster':
        from abstractPatch import cluster

        dbDir = join(DATA_PATH, 'redis')
        startDB(dbDir, REDIS_PORT, PROJECT_TYPE)
        cluster(join(DATA_PATH, 'actions'), join(DATA_PATH, 'pairs'), 'actions')

    elif job == 'tokenSI':
        from pairs import tokenPairs, importTokens

        tokenPairs()
        importTokens()

    elif job == 'clusterTokens':
        from abstractPatch import cluster

        dbDir = join(DATA_PATH, 'redis')
        startDB(dbDir, REDIS_PORT, PROJECT_TYPE)
        cluster(join(DATA_PATH, 'tokens'), join(DATA_PATH, 'pairsToken'), 'tokens')

    elif job == 'codeflaws':
        from otherDatasets import codeflaws

        codeflaws()

    elif job == 'indexClusters':
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

    elif job == 'patternOperations':
        from sprinferIndex import patternOperations

        patternOperations()

    elif job == 'patchManyBugs':
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

    elif job == 'patchIntro':
        from sprinferIndex import patchCoreIntro

        patchCoreIntro()
        # from sprinferIndex import patched
        # patched()

    elif job == 'validateIntro':
        # from patch_validate_introClass2 import patch_validate
        # patch_validate()
        from test_patched_file import patch_validate

        patch_validate()

    elif job == 'checkCorrectIntro':
        from test_patched_file import checkCorrect

        checkCorrect()

    elif job == 'manybugs':
        from getManybugs import export

        export()

    elif job == 'validateMany':
        from patch_validate import patch_validate

        patch_validate()

    elif job == 'introclass':
        from getIntroClass import export

        export()

    elif job == 'stats':
        from stats import statsNormal

        statsNormal(True)

    elif job == 'datasetDefects4J':
        from defects4JDataset import core

        core()

    elif job == 'bug':
        from bugstats import bStats

        bStats()

    elif job == 'defects4j':
        from stats import defects4jStats

        defects4jStats()

    elif job == 'patterns':
        from stats import exportAbstractPatterns

        exportAbstractPatterns()

    else:
        logging.error('Unknown job %s', job)
