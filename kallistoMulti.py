#!/usr/bin/env python
"""
Run kallisto on multiple files
"""

import argparse
import os
import re
import shlex
import subprocess
import sys

def get_args():
    """
    Get command line arguments
    """

    parser = argparse.ArgumentParser(
        description="Run kallisto on multiple samples",
        epilog="Any additional, unknown, arguments will be passed to kallisto. These must go after the input files.")
    #parser.add_argument("inputs",
    #                    metavar="FASTQ",
    #                    nargs="+",
    #                    help="Input FASTQ files")
    parser.add_argument("-i", "--index",
                        help="Path to kallisto index",
                        required=True)
    parser.add_argument("-o", "--output-dir",
                        help="Path to output directory",
                        required=True)
    parser.add_argument("-1", "--read1",
                        help="FASTQ files containing first read in pair",
                        nargs="+")
    parser.add_argument("-2", "--read2",
                        help="FASTQ files containing second read in pair",
                        nargs="+")
    args, unknown = parser.parse_known_args()
    kal_opts = " ".join(unknown)

    return args, kal_opts


#def pair_inputs(inputs, regex1, regex2):
#    """
#    Take a list of inputs and pair them based on two regular expressions
#    """
#
#    inputs1 = []
#    inputs2 = []
#
#    for input_file in inputs:
#        if re.search(regex1, input_file):
#            inputs1.append(input_file)
#        elif re.search(regex2, input_file):
#            inputs2.append(input_file)
#        else:
#            sys.exit("""An input did not match either regex. You may need to
#                     adjust your patterns""")
#
#    if len(inputs1) == len(inputs2):
#        pairs = zip(inputs1, inputs2)
#        return pairs
#    else:
#        sys.exit("""Different numbers of inputs matched each regualar
#                 expression. You may need to adjust your patterns.""")


def main():
    """
    Run main code
    """

    args, kal_opts = get_args()

    #input_pairs = pair_inputs(args.inputs, args.regex1, args.regex2)
    input_pairs = zip(args.read1, args.read2)

    failed = 0
    sample_count = 0

    print "Beginning kallisto quantification on multiple samples...\n"
    for pair in input_pairs:
        sample = os.path.basename(pair[0])
        sample = sample.split(".")[0]
        sample_count += 1
        print "Quantifying sample", sample_count, "of", len(pairs), "-", sample
        cmd_str = "kallisto quant --index " + args.index + " --output-dir "
        cmd_str += args.output_dir + "/" + sample + " " + kal_opts + " "
        cmd_str += pair[0] + " " + pair[1]
        cmd = shlex.split(cmd_str)
        failed = subprocess.call(cmd)
        if failed:
            sys.exit("kallisto command '" + cmd_str + "' failed to run")
        print "Sample", sample, "complete\n"
    print "Done!"

if __name__ == "__main__":
    main()
