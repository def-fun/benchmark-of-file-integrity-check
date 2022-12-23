#!/usr/bin/env python3
"""
benchmark of file integrity check tools and algorithms
"""
import os.path
import time
import subprocess
import sys

tools_and_algorithms = [
    {"tool": "cfv",
     "cmd": "cfv -C -rr -t {algo} -p {path} -f {temp_file}",
     "algorithms": ['crc', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'],
     },
    {"tool": 'rhash',
     "cmd": "rhash --{algo} -r {path} -o {temp_file}",
     "algorithms": ['crc32', 'crc32c', 'md4', 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                    'sha3-224', 'sha3-256', 'sha3-384', 'sha3-512', 'tiger', 'tth', 'btih', 'aich', 'ed2k',
                    'whirlpool', 'gost12-256', 'gost12-512', 'gost94', 'gost94-cryptopro', 'ripemd160',
                    'has160', 'snefru128', 'snefru256', 'edonr256', 'edonr512', 'blake2b', 'blake2s'],
     },
    {"tool": 'find-x-sum',
     "cmd": "find {path} -type f -exec {algo} {{}} \\; > {temp_file}",
     "algorithms": ['md5sum', 'sha1sum', 'sha256sum', 'sha384sum', 'sha512sum'],
     },
]


def benchmark_tools_and_algorithms(tool_and_algorithm: dict, path: str, circles=3):
    time_count = {k: 0 for k in tool_and_algorithm['algorithms']}
    results = []  # [algorithm, seconds, filesize]
    for algo in tool_and_algorithm['algorithms']:
        temp_file = f'/tmp/test-{tool_and_algorithm["tool"]}-{algo}.sfv'
        for _ in range(circles):
            if os.path.isfile(temp_file):
                os.remove(temp_file)
            t0 = time.time()
            out = subprocess.check_call([tool_and_algorithm['cmd'].format(path=path, algo=algo, temp_file=temp_file)],
                                        shell=True)
            t1 = time.time()
            time_count[algo] += (t1 - t0)
        results.append([algo, round(time_count[algo] / circles, 3), os.path.getsize(temp_file)])
    results.sort(key=lambda ele: ele[1], reverse=False)
    print(f'# benchmark for {tool_and_algorithm["tool"]}, {circles} circle(s)')
    print('%-20s%-20s%-20s' % ('algorithm', 'seconds', 'filesize'))
    print('-' * 50)
    for r in results:
        print('%-20s%-20s%-20s' % tuple(r))
    print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <path-to-dir>')
        sys.exit(1)

    test_path = sys.argv[1]
    print(f'test path: {test_path}')
    for tool_and_algo in tools_and_algorithms:
        benchmark_tools_and_algorithms(tool_and_algorithm=tool_and_algo, path=test_path, circles=3)
