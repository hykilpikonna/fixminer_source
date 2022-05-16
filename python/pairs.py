from common.commons import *
import redis

DATA_PATH = os.environ["DATA_PATH"]
ROOT = os.environ["ROOT_DIR"]
INNER_DATA_PATH = join(ROOT, 'data')
PROJECT_TYPE = os.environ["PROJECT_TYPE"]
REDIS_PORT = os.environ["REDIS_PORT"]


def importTokens():
    pairsAction = join(DATA_PATH, 'pairsToken')
    redis_db = redis.StrictRedis(host="localhost", port=int(REDIS_PORT), db=1)
    pairs = get_filepaths(pairsAction, '.txt')
    for pair in pairs:
        split = pair.split("/")
        shapeName = split[-3]
        shapeSize = split[-2]
        cluster = split[-1].replace('.txt', '')
        cmd = "bash " + join(INNER_DATA_PATH, 'redisSingleImport.sh') + " " + pair + " "+REDIS_PORT+" " + shapeName + "-" + shapeSize + "-" + cluster;  # +, portInner,f.getName()+"-"+pair.getName().split("\\.")[0]);

        o, e = shellGitCheckout(cmd)
        print(o)
        indexFile = pair.replace('.txt', '.index')
        with open(indexFile, 'r') as iFile:
            idx = iFile.readlines()
        for i in idx:
            k, v = i.split(',')
            key = shapeName + "-" + shapeSize + "-" + cluster + "-" + k
            redis_db.hset('filenames', key, v.strip())
    redis_db.set("level", "l2")


def importAction():
    pairsShapes = join(DATA_PATH, 'pairs')
    redis_db = redis.StrictRedis(host="localhost", port=int(REDIS_PORT), db=1)
    pairs = get_filepaths(pairsShapes, '.txt')
    for pair in pairs:
        split = pair.split("/")
        shapeName = split[-2]
        sizeCluster = split[-1].replace('.txt', '')
        cmd = "bash " + join(INNER_DATA_PATH, 'redisSingleImport.sh') + " " + pair + " "+REDIS_PORT+" " + shapeName + "-" + sizeCluster;

        o, e = shellGitCheckout(cmd)
        print(o)
        indexFile = pair.replace('.txt', '.index')
        with open(indexFile, 'r') as iFile:
            idx = iFile.readlines()
        for i in idx:
            k, v = i.split(',')
            key = shapeName + "-" + sizeCluster + "-" + k
            #redis_db.set(key, v.strip())
            redis_db.hset('filenames',key,v.strip())
    redis_db.set("level","l1")


def tokenPairs():
    shapes = listdir(join(DATA_PATH, 'actions'))
    shapes = [f for f in shapes if isdir(join(DATA_PATH, 'actions', f))]

    if os.path.exists(join(DATA_PATH, 'pairsToken')):
        import shutil
        shutil.rmtree(join(DATA_PATH, 'pairsToken'))

    for shape in shapes:
        sizes = listdir(join(DATA_PATH, 'actions', shape))
        sizes = [f for f in sizes if isdir(join(DATA_PATH, 'actions', shape, f))]
        for sf in sizes:
            if sf.startswith('.'):
                continue
            clusters = listdir(join(DATA_PATH, 'actions', shape, sf))
            for cluster in clusters:
                if cluster.startswith('.'):
                    continue
                files = listdir(join(DATA_PATH, 'actions', shape, sf, cluster))
                if len(files) > 1:
                    indexCompared = []
                    if not os.path.exists(join(DATA_PATH, 'pairsToken', shape, sf)):
                        os.makedirs(join(DATA_PATH, 'pairsToken', shape, sf))

                    indexFile = join(DATA_PATH, 'pairsToken', shape, sf, cluster + '.index')
                    if isfile(indexFile):
                        test = pd.read_csv(indexFile, header=None, index_col=0)
                        test.rename(columns={1: 'filename'}, inplace=True)

                        newFiles = [i for i in files if i not in test.filename.values.tolist()]
                        for newFile in newFiles:
                            test = test.append(pd.DataFrame(columns=['filename'], data=[newFile]), ignore_index=True)
                        indexCompared = test.index.values.tolist()
                        test.to_csv(indexFile, header=None)
                    else:
                        with open(indexFile, 'w') as out:
                            # csv_out = csv.writer(out)

                            for idx, val in enumerate(files):
                                out.write(str(idx) + ',' + val + '\n')
                                indexCompared.append(str(idx))

                    pairs = list(itertools.combinations(indexCompared, 2))

                    pairsFile = join(DATA_PATH, 'pairsToken', shape, sf, cluster + '.txt')
                    if isfile(pairsFile):
                        test = pd.read_csv(pairsFile, header=None)
                        test['pairs'] = test.apply(lambda x: tuple([x[0], x[1]]), axis=1)
                        newPairs = [i for i in pairs if i not in test['pairs'].values.tolist()]
                        with open(pairsFile, 'w') as out:
                            # csv_out = csv.writer(out)
                            for row in newPairs:
                                a, b = row
                                out.write(a + ',' + b + '\n')
                    else:
                        with open(pairsFile, 'w') as out:
                            # csv_out = csv.writer(out)
                            for row in pairs:
                                a, b = row
                                out.write(a + ',' + b + '\n')


def actionPairs():
    redis_db = redis.StrictRedis(host="localhost", port=int(REDIS_PORT), db=0)
    keys = redis_db.hkeys("dump")

    matches = pd.DataFrame(keys, columns=['pairs_key'])

    matches['pairs_key'] = matches['pairs_key'].apply(lambda x: x.decode())
    matches['root'] = matches['pairs_key'].apply(lambda x: x.split('/')[0])
    matches['size'] = matches['pairs_key'].apply(lambda x: x.split('/')[1])
    matches['file'] = matches['pairs_key'].apply(lambda x: x.split('/')[2])
    matches['fileName'] = matches['pairs_key'].apply(lambda x: '_'.join(x.split('/')[2].split('_')[:-1]))

    matches['hunk'] = matches['pairs_key'].apply(lambda x: x.split('/')[2].split('_')[-1])

    return matches


def createPairs(matches):
    if len(matches) == 0:
        return True
    roots = matches.root.unique().tolist()
    # roots = listdir(join(DATA_PATH,'EnhancedASTDiffgumInput'))
    if os.path.exists(join(DATA_PATH, 'pairs')):
        import shutil
        shutil.rmtree(join(DATA_PATH, 'pairs'))
    for root in roots:
        # if root.startswith('.'):
        #     continue
        rootMatch = matches[matches['root'] == root]
        sizes = rootMatch['size'].unique().tolist()
        for sf in sizes:
            # if sf == '1':
            #     continue
            match = rootMatch[rootMatch['size'] == sf]
            files = match.file.unique().tolist()

            if len(files) > 1:
                files
                indexCompared = []
                if not os.path.exists(join(DATA_PATH, 'pairs', root)):
                    os.makedirs(join(DATA_PATH, 'pairs', root))


                indexFile = join(DATA_PATH, 'pairs', root, sf + '.index')
                if isfile(indexFile):
                    test = pd.read_csv(indexFile, header=None, index_col=0)
                    test.rename(columns={1: 'filename'}, inplace=True)

                    newFiles = [i for i in files if i not in test.filename.values.tolist()]
                    for newFile in newFiles:
                        test = test.append(pd.DataFrame(columns=['filename'], data=[newFile]), ignore_index=True)
                    indexCompared = test.index.values.tolist()
                    test.to_csv(indexFile, header=None)
                else:

                    with open(indexFile, 'w') as out:
                        # csv_out = csv.writer(out)

                        for idx, val in enumerate(files):
                            out.write(str(idx) + ',' + val + '\n')
                            indexCompared.append(str(idx))

                pairs = list(itertools.combinations(indexCompared, 2))

                # import csv
                pairsFile = join(DATA_PATH, 'pairs', root, sf + '.txt')
                if isfile(pairsFile):
                    test = pd.read_csv(pairsFile, header=None)
                    test['pairs'] = test.apply(lambda x: tuple([x[0], x[1]]), axis=1)
                    newPairs = [i for i in pairs if i not in test['pairs'].values.tolist()]
                    with open(pairsFile, 'w') as out:
                        # csv_out = csv.writer(out)
                        for row in newPairs:
                            a, b = row
                            out.write(a + ',' + b + '\n')
                else:
                    with open(pairsFile, 'w') as out:
                        # csv_out = csv.writer(out)
                        for row in pairs:
                            a, b = row
                            out.write(a + ',' + b + '\n')
    return False
