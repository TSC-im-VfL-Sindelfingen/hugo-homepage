import argparse

def getArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('--read-mbox', nargs=1, help='Read mails from mbox file instead of stdin')
    parser.add_argument('-o', '--output-folder', nargs=1, help='Set the output folder of the generated files.')
    parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase the verbosity')
    parser.add_argument('--debug', action='store_true', help='Enable python debugger')

    return parser.parse_args()
