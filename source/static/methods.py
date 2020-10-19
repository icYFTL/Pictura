from io import BytesIO
from os import path, mkdir, system, remove
from random import randint
import requests
from shutil import move, rmtree
import sys


def webp_to_png(img: BytesIO):
    # webptools doesn't work
    if not path.exists('tmp'):
        mkdir('tmp')

    if not path.exists('dwebp'):
        # OK...
        r = requests.get(
            'https://files.pythonhosted.org/packages/05/9d/ac0156babdc9ee803bf54b0d47379d98d5f779f0ecaa7f1e199fe39977cf/webptools-0.0.3.tar.gz')
        open(path.join('tmp', 'webtools.tar.gz'), 'wb').write(r.content)
        # I don't give a fuck...
        system(f'tar -xf {path.join("tmp", "webtools.tar.gz")}')
        move('webptools-0.0.3', path.join('tmp', 'webptools-0.0.3'))
        remove(path.join('tmp', 'webtools.tar.gz'))
        src = 'libwebp_linux'
        if sys.platform == 'darwin':
            src = 'libwebp_osx'
        else:
            src = 'libwebp_win64'

        # I DONT GIVE A FUCK

        move(path.join('tmp', 'webptools-0.0.3', 'lib', src, 'bin', 'dwebp'), '.')
        rmtree(path.join('tmp', 'webptools-0.0.3'))

    file = f'tempfile{randint(1000, 10000000)}'  # hehe im lazy
    open(path.join('tmp', file + '.webp'), 'wb').write(img.read())
    system('dwebp ' + path.abspath(path.join('tmp', file + '.webp')) + ' -o ' + path.abspath(
        path.join('tmp', file + '.png')))

    # Piece of shit.

    remove(path.join('tmp', file + '.webp'))

    # I hate python. Where is cool webp libraries?

    return path.join('tmp', file + '.png')
