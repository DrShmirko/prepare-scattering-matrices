#!/usr/bin/env python3

import click

from scattlib.config import CONFIG_FILES
from scattlib.scattmatrices import MuellerMatrixAeronet


@click.command()
@click.option('--nlines','-n', default=5, type=int, 
                help='Столько данных читает из файла')
@click.option('--spheres/--spheroids', default=False, 
                help='Использовать сферрические ядра')
@click.option('--sphericity', type=click.FloatRange(1.0, 99.0),
                default=1.0, help='Доля сферического аэрозоля')
@click.argument('files', nargs=-1, type=click.Path(exists=True), 
                required=True)
def do_process(nlines, spheres, sphericity, files):
    mc = MuellerMatrixAeronet(spheres)
    mc.run(files, sphericity)
    mc.finalize()
    return
    
    
if __name__ == '__main__':
    do_process()