import os

from subprocess import check_output


# Compute an anonymous sum of data
def compute(epsilon, budget, lower, upper):
    os.chdir('./differential-privacy-master/')
    #os.chdir('/diffpriv/differential-privacy-master/')
    #out = check_output(['/root/bin/bazel run differential_privacy/operations:priv_sum -- %f %f %f %f'
    #                    % (epsilon, budget, lower, upper)], shell=True)
    out = check_output(['bazel run differential_privacy/operations:priv_sum -- %f %f %f %f'
                        % (epsilon, budget, lower, upper)], shell=True)
    print "AnonSum output:\n", out
    os.chdir('../')
    return out
