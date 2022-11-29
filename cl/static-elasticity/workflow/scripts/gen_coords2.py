import subprocess
import re
import sys
import argparse

LEXER_PATTERN = rb"k\(\s+\d+\) = \((\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+)\), wk =\s+(\d+\.\d+)"
LEXER = re.compile(LEXER_PATTERN)

STATE_KPTS_BEFORE = 0
STATE_KPTS_READING = 4
STATE_KPTS_READING_CART = 1
STATE_KPTS_READING_CRYST = 2
STATE_KPTS_AFTER = 3

def parse_args():
    parser = argparse.ArgumentParser(description='Get mesh grid with weights/multiplicities.')
    parser.add_argument('--input', default=None)
    parser.add_argument('--output', default=None)
    parser.add_argument('--type', default='cryst')
    args = parser.parse_args()
    return args.input, args.output

class KPointsGenerator:
    def __init__(self, input_filename=None, output_filename=None):
        self.input_filename = input_filename
        self.output_filename = output_filename
    def write_output(self):
        if self.output_filename:
            self.write_result()
        else:
            self.prompt_result()
    def _read_process_output(self, process):
        state = STATE_KPTS_BEFORE
        kpts_results_cart = []
        kpts_results_cryst = []
        while True:
            line_bytes = process.stdout.readline()
            lex_result = LEXER.search(line_bytes)
            if re.search(rb'number of k points', line_bytes):
                state = STATE_KPTS_READING
                continue
            if state in [
                    STATE_KPTS_READING,
                    STATE_KPTS_READING_CART,
                    STATE_KPTS_READING_CRYST
                    ]:
                if re.search(rb'cart. coord. in units', line_bytes):
                    state = STATE_KPTS_READING_CART
                    continue
                if re.search(rb'cryst. coord.', line_bytes):
                    state = STATE_KPTS_READING_CRYST
                    continue
            if state == STATE_KPTS_BEFORE:
                if lex_result:
                    state = STATE_KPTS_READING
            if state == STATE_KPTS_READING_CART:
                if not lex_result:
                    #state = STATE_KPTS_AFTER
                    pass
                else:
                    kpts_results_cart.append(lex_result.groups())
            if state == STATE_KPTS_READING_CRYST:
                if not lex_result:
                    state = STATE_KPTS_AFTER
                else:
                    kpts_results_cryst.append(lex_result.groups())
            if state == STATE_KPTS_AFTER:
                process.kill()
                break
        return kpts_results_cart, kpts_results_cryst
    def _create_process(self):
        if self.input_filename:
            return subprocess.Popen(
                    ['pw.x', '-in', self.input_filename],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL)
        else:
            return subprocess.Popen(['pw.x'],
                    stdin=sys.stdin,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL)
    def get_result(self, key='cryst'):
        process = self._create_process()
        self.kpts_results_cart, self.kpts_results_cryst = self._read_process_output(process)
        if key == 'cryst':
            return b"\n".join([b'\t'.join(line) for line in self.kpts_results_cryst])
        elif key == 'cart':
            return b"\n".join([b'\t'.join(line) for line in self.kpts_results_cart])
        else:
            raise RuntimeError('Wrong Key.')
    def write_result(self, output_filename=None, key='cryst'):
        with open(output_filename if output_filename else self.output_filename, 'wb') as f:
            f.write(self.get_result(key))
    def prompt_result(self, key='cryst'):
        print(self.get_result(key).decode())

if __name__ == '__main__':
    in_file, out_file = parse_args()
    generator = KPointsGenerator(in_file, out_file)
    generator.write_output()
