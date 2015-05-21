import os
import subprocess


def generate(from_file, x, y, filenames, type='.png'):
    filenames = filenames.split()
    with open('local01.tff', 'w') as m:
        print('generated local file')

    yield "convert {0} local01.miff".format(from_file)
    for i, filename in enumerate(filenames):
        l = "convert local01.miff -crop {0}x{1}+{2}+0 {3}{4}"
        yield l.format(x, y, i * x, filename, type)
    yield "rm local01.miff"


def main():
    rendered_name = 'RENDERED_icons.png'
    icons = "VTX V2X XALL BIX PERP CCEN EXM"
    file_strings = generate(rendered_name, 32, 32, icons)
    for line in file_strings:
        subprocess.Popen(line.split())


main()
