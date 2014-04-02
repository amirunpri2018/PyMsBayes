#!/usr/bin/env python

"""
Dirichlet process calculations.
"""

import os
import sys
import argparse

from pymsbayes.utils import argparse_utils

_program_info = {
    'name': os.path.basename(__file__),
    'author': 'Jamie Oaks',
    'version': 'Version 0.1.0',
    'description': __doc__,
    'copyright': 'Copyright (C) 2013 Jamie Oaks',
    'license': 'GNU GPL version 3 or later',}

def main():
    parameter_options = ['concentration', 'ncats']
    description = '{name} {version}'.format(**_program_info)
    parser = argparse.ArgumentParser(description = description,
            formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version',
            action='version',
            version='%(prog)s ' + _program_info['version'],
            help='report version and exit')
    parser.add_argument('parameter',
            choices=parameter_options,
            nargs=1,
            help = ('The parameter provided. The two options are:\n'
                    '`concentration`: the concentration parameter\n'
                        '\tof the Dirichlet process.\n'
                    '`ncats`: the expected (mean) number of\n'
                        '\tcategories for the dirichlet\n'
                        '\tprocess.\n'
                    'You provide one of these two parameters along\n'
                    'with the number of elements (taxon pairs),\n'
                    'and this program calculates and returns the\n'
                    'other one accordingly.'))
    parser.add_argument('parameter_value',
            metavar='X',
            type=argparse_utils.arg_is_positive_float,
            help=('Value of the parameter'))
    parser.add_argument('--shape',
            required = False,
            type=argparse_utils.arg_is_positive_float,
            help = ('Shape parameter of a gamma hyperprior on the\n'
                    'concentration parameter of the Dirichlet\n'
                    'process. If provided, the program will\n'
                    'calculate a corresponding scale parameter\n'
                    'for the gamma hyperprior such that the\n'
                    'mean of the gamma hyperprior is equal to\n'
                    'the reported concentration parameter and the\n'
                    'prior expectation for the number of\n'
                    'categories is equal to `ncats`.'))
    parser.add_argument('npairs',
            metavar='N',
            type=argparse_utils.arg_is_nonnegative_int,
            help='Number of elements (i.e., number of taxon pairs).')

    args = parser.parse_args()

    from pymsbayes.utils.stats import Partition
    p = Partition('0' * args.npairs)

    results = dict(zip(parameter_options,
            [None for k in parameter_options]))
    args.parameter = args.parameter[0]
    if args.parameter == 'concentration':
        results['concentration'] = args.parameter_value
        results['ncats'] = p.get_dpp_expected_num_cats(args.parameter_value)

    elif args.parameter == 'ncats':
        results['ncats'] = args.parameter_value
        results['concentration'] = p.get_dpp_concentration(args.parameter_value)

    else:
        raise Exception('parameter option {0} is not valid'.format(
                args.parameter))

    if args.shape:
        results['shape'] = args.shape
        results['scale'] = results['concentration'] / args.shape
        parameter_options.extend(['shape', 'scale'])
        
    sys.stdout.write('number_of_elements = {0}\n'.format(args.npairs))
    for key in parameter_options:
        sys.stdout.write('{0} = {1}\n'.format(
                key,
                results[key]))

if __name__ == '__main__':
    main()
