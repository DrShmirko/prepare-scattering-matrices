#!/usr/bin/env python3

import click

from scattlib.config import CONFIG_FILES
from scattlib.scattmatrices import MuellerMatrixAeronet,\
                                    MuellerMatrixCombiner



@click.group()
def cli():
    pass

#@cli.command()
#@click.option('--nlines','-n', default=5, type=int, 
#                help='Столько данных читает из файла')
#@click.option('--spheres/--spheroids', default=False, 
#                help='Использовать сферрические ядра')
#@click.option('--sphericity', type=click.FloatRange(1.0, 99.0),
#                default=40.0, help='Доля сферического аэрозоля')
#@click.option('--skiprows','-s', default=0, type=int,
#                help='Количество пропускаемых строк')
#@click.argument('filename', nargs=1, type=click.Path(exists=True), 
#                required=True)
def do_process(nlines, spheres, sphericity, skiprows, filename):
    filename = (filename,)
    mc = MuellerMatrixAeronet(spheres)
    mc.run(filename, sphericity, skiprows)
    mc.finalize()
    return


#@cli.command()
#@click.option('--skiprows','-s', default=0, type=int,
#                help='Количество пропускаемых строк')
#@click.option('--dirname', nargs=1, 
#                type=click.Path(exists=True, 
#                    dir_okay=True, file_okay=False), 
#                required=True)
#@click.option('--sphericity', type=click.FloatRange(1.0, 99.0),
#                default=40.0, help='Доля сферического аэрозоля')
#@click.argument('filename', nargs=1, type=click.Path(exists=True), 
#                required=True)
def do_combine(skiprows, dirname, sphericity, filename):
    cb = MuellerMatrixCombiner(skiprows)
    cb.run(dirname, sphericity, filename)
    pass
    
@cli.command()
@click.option('--skiprows','-s', default=0, type=int,
                help='Количество пропускаемых строк')
@click.option('--sphericity', type=click.FloatRange(1.0, 99.0),
                default=40.0, help='Доля сферического аэрозоля')
@click.argument('filename', nargs=1, type=click.Path(exists=True), 
                required=True)
def do_alljob(skiprows, sphericity, filename):
    click.echo("Building spheoidal matrices....")
    do_process(5, False, sphericity, skiprows, filename)
    click.echo("Building spherical matrices....")
    do_process(5, True, sphericity, skiprows, filename)
    click.echo("Combine both of them....")
    do_combine(skiprows, "out/", sphericity, filename)
                

if __name__ == '__main__':
    cli()