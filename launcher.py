import argparse
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

import requests
import yaml
from dateutil.relativedelta import relativedelta

TG_TOKEN = 'bot1667933988:AAFhCZ-1poke3ARNRx9BYd-Hb93jjAc-P7s'
TG_CHAT_ID = 219458549


def log_tg(msg: str):
    print(msg)
    requests.get(f"https://api.telegram.org/{TG_TOKEN}/sendMessage",
                 params={'chat_id': TG_CHAT_ID, 'text': msg})


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Launch FixMiner')
    p.add_argument('-d', type=int, help='How many days to retrieve before the last commit')
    p.add_argument('-a', type=str, help='What absolute date as the end time (yyyy-mm-dd)')

    args = p.parse_args()
    with open('launcher.config.yml') as f:
        cfg = yaml.safe_load(f)

    days = args.d or args.a
    assert days, 'Must specify either -d or -a'

    def run(days: str):
        data = Path(cfg['data-generated']).with_suffix('.absolute' if args.a else '.relative')
        day_path = data / days

        if day_path.is_dir():
            print(f'{days} already processed, skipping.')
            return

        generated_cfg = {
            'java': {
                '8home': cfg['java-home']
            },
            'spinfer': {
                'home': cfg['spinfer']
            },
            'coccinelle': {
                'home': cfg['coccinelle']
            },
            'dataset': {
                'inputPath': str(day_path / 'patches'),
                'repo': cfg['data-repo']
            },
            'fixminer': {
                'projectType': 'java',
                'datapath': str(day_path),
                'pjName': 'patches',
                'portDumps': 6399,
                'numOfWorkers': 36,
                'hostname': 'localhost',
                'hunkLimit': 2,
                'patchSize': 50,
                'projectList': 'ALL',
                'inputPath': str(day_path / 'patches'),
                'redisPath': str(day_path / 'redis'),
                'srcMLPath': '/usr/bin/srcml'
            }
        }

        # Absolute vs Relative timing
        if args.d:
            generated_cfg['fixminer']['limitCommitsBeforeDays'] = days
        elif args.a:
            generated_cfg['fixminer']['limitCommitsAbsoluteDate'] = days

        with open("config_tmp.yml", 'w') as file:
            yaml.dump(generated_cfg, file)

        log_tg(f'Executing fixminer on commits before {days}.')
        ret = os.system('python python/main.py config_tmp.yml pipeline')
        assert ret == 0, f'Error! Return code is {ret} when running fixminer'
        log_tg('Done')


    # Relative Days
    try:
        if args.d:
            days = int(days)
            while True:
                run(str(days))
                days += 90
        if args.a:
            days = datetime.strptime(days, '%Y-%m-%d')
            while True:
                run(days.strftime('%Y-%m-%d'))
                days -= relativedelta(months=3)

    except KeyboardInterrupt as e:
        log_tg(f'Interrupted. Before interrupt, it was processing {days}')
        # print(f'Deleting folder for {days}...')
        raise e

    except AssertionError as e:
        log_tg(str(e))
        raise e
