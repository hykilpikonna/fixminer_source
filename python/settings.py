import os
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = os.environ["ROOT_DIR"]
REPO_PATH = os.environ["REPO_PATH"]
CODE_PATH = os.environ["CODE_PATH"]
DATA_PATH = os.environ["DATA_PATH"]
COMMIT_DFS = os.environ["COMMIT_DFS"]
BUG_POINT = os.environ["BUG_POINT"]
COMMIT_FOLDER = os.environ["COMMIT_FOLDER"]
FEATURE_DIR = os.environ["FEATURE_DIR"]
DATASET_DIR = os.environ["DATASET_DIR"]
PROJECT_TYPE = os.environ["PROJECT_TYPE"]
REDIS_PORT = os.environ["REDIS_PORT"]
jdk8 = os.environ["JDK8"]

JAR_PATH = Path(ROOT_DIR).parent / 'target/FixPatternMiner-1.0.0-jar-with-dependencies.jar'
