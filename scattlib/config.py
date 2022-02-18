# словарь для отработки параметра '--spheres / --spheroids'
# True для spheres
# False для spheroids
CONFIG_FILES={
    True: 'py-libspheroid/input_sphrs.dat',
    False:'py-libspheroid/input_sphrds.dat'
}

PREFIXES={
    True: 'sphrs',
    False: 'sphrd'
}

WAVELEN_COLUMNS = [
    'Refractive_Index-Real_Part[440nm]',
    'Refractive_Index-Real_Part[675nm]',
    'Refractive_Index-Real_Part[870nm]',
    'Refractive_Index-Real_Part[1020nm]'
]


WVL=[0.440, 0.675, 0.870, 1.020]
