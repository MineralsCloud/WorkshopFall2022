'''The slurm supervisor
-- to submit a slurm job to HPC and sip on a cup of coffee.

* creates `job.submitted` after submission
* exit after the job indicated here finishes

TODO: tracking multiple jobs?
TODO: create job from STDIN?
'''

import click
import io
import json
from pathlib import Path
import logging
import os
import time
import sh
import re
import csv


logger = logging.getLogger(__name__)

def get_slurm_job_id(submitted: str) -> int:

    with open(submitted) as fp:
        content = fp.read().strip()
        res = re.search(r"^Submitted batch job (\d+)$", content)
    assert res 
    job_id = int(res.group(1))
    assert job_id

    return job_id

@click.command(help=__doc__)
@click.argument("shell_script")
@click.option("--verbosity", default="WARNING", type=click.Choice(logging._levelToName.values()), help="Logging level")
@click.option("-f", "--force", default=False, is_flag=True, help="Remove job file and restart")
@click.option("-t", "--check-time-interval", type=click.INT, default=15, help="Interval between run squeue in seconds")
def main(verbosity: str, *argv, **kwargs):

    logging.basicConfig(level=verbosity)

    shell_script = kwargs["shell_script"]

    shell_script = Path(shell_script)
    shell_name = shell_script.name
    shell_dir = shell_script.parent
        
    cwd = os.getcwd()
    os.chdir(shell_dir)

    submitted = f"{shell_name}.submitted"

    if Path(submitted).exists() and kwargs.pop("force"):
        try:
            job_id = get_slurm_job_id(submitted)
            sh.scancel(job_id)   # pylint: disable=no-member
        except AssertionError:
            pass
        Path(submitted).unlink()

    if not Path(submitted).exists():
        sh.sbatch(shell_name, _out=submitted)   # pylint: disable=no-member
        time.sleep(5)

    job_id = get_slurm_job_id(submitted)

    logger.debug(f"Found JOB_ID {job_id}")
        
    dt = kwargs.pop("check_time_interval")
    while True:
        try:
            p = sh.squeue("-j", job_id, "-o %all")      # pylint: disable=no-member 
            status = next(csv.DictReader(io.StringIO(p.stdout.decode()), delimiter="|"))
            logger.debug(status)
            # click.echo(json.dumps(status, indent=2))
            time.sleep(dt)
        except (sh.ErrorReturnCode_1, StopIteration):   # pylint: disable=no-member 
            break

    os.chdir(cwd)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter