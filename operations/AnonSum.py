import Const
import os
import subprocess


# Compute an anonymous sum of data
def compute(epsilon, budget, lower, upper):
    os.chdir(Const.DIFF_PRIV_PATH)
    #os.chdir('/diffpriv/differential-privacy-master/')
    #out = check_output(['/root/bin/bazel run differential_privacy/operations:priv_sum -- %f %f %f %f'
    #                    % (epsilon, budget, lower, upper)], shell=True)
    subprocess.check_output(['bazel run differential_privacy/operations:priv_sum -- %f %f %f %f'
                             % (epsilon, budget, lower, upper)], shell=True)
    os.chdir(Const.PARENT_DIR)
