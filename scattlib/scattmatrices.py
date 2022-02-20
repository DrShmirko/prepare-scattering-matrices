#
from libspheroid import lsd, SpheroidCalc
from tqdm.contrib import tenumerate
import pandas as pd
from .config import WAVELEN_COLUMNS, WVL, CONFIG_FILES, PREFIXES
import numpy as np

class MuellerMatrixAeronet(object):
    
    def __init__(self, spheres, wvl = 0.865):
        self.wvl = np.r_[WVL]
        self.spc = SpheroidCalc(CONFIG_FILES[spheres])
        self.spc.wvl=wvl
        self.isSpheres=spheres
        
    def run(self, files, sphericity, skiprows):
        for i, fname in tenumerate(files):
            print(f'Processing file {fname}...')
            self._run0(fname, sphericity, skiprows)
        pass
        
    def _run0(self, file0, sphericity, skiprows):
        ant_tbl = pd.read_csv(file0, skiprows=skiprows)
        all_ok = True
        
        for col_i in WAVELEN_COLUMNS:
            all_ok = all_ok and (col_i in ant_tbl.columns)
        if not all_ok:
            return
        
        # Angstrom exponent
        # 
        # (t1/t0)=(l1/l0)^-a
        # log(t1) - log(t0) = -a(log l1 - log l0)
        # log(t1) = -a log(l1) + log t0 + a log l0
        for i, r in tenumerate(ant_tbl.iterrows()):
            # Достаем 
            re = r[1][32:36].values.astype('float')
            im = r[1][36:40].values.astype('float')
            sp = r[1][52]
            
            # Пропуск итерации, если сферичность выше необходимой
            if sp>sphericity:
                continue
            
            aot = r[1][10:14].values.astype('float')
            dvdlnr = r[1][53:75].values.astype('float')
            re0 = np.interp(self.spc.wvl, self.wvl, re)
            im0 = np.interp(self.spc.wvl, self.wvl, im)
            
            p = np.polyfit(np.log10(self.wvl), np.log10(aot), deg=1)
            aot0 = 10**(np.polyval(p, np.log10(self.spc.wvl)))
            
            self.spc.midx = complex(re0, im0)
            self.spc.sd = dvdlnr
            self.spc.calc()
            foutname = f"out/{PREFIXES[self.isSpheres]}_{i}.out"
            self._saveToFile(foutname)
            
    def _saveToFile(self, foutname):
        volC = self.spc.VolC
        m = self.spc.FMTX/volC
        with open(foutname,"wt") as fout:
            print(f"{self.spc.sca/volC:.4f} {self.spc.ext/volC:.4f} {self.spc.absb/volC:.4f} {volC:4f}", file=fout)
            print(f"theta s11 s12 s13 s14 s21 s22 s23 s24 s31 s32 s33 s34 s41 s42 s43 s44", file=fout)
            for i in range(self.spc.km):
                print(self.spc.angle[i], end=' ', file=fout)
                for j in range(16):
                    print(f"{m[i, j]:.4e}", end=' ', file=fout)
                print(file=fout)
        
    
        
    def finalize(self):
        print('Free internal memory used by dynamic library.')
        self.spc.ndp=0
        self.spc.finalize()
        


class MuellerMatrixCombiner(object):
    def __init__(self, skiprows):
        """
        """
        self.skiprows = skiprows
        pass
        
    def run(self, dirname, sphericity, filename):
        """
        """
        ant_tbl = pd.read_csv(filename, skiprows=self.skiprows)
        all_ok = True
        
        for col_i in WAVELEN_COLUMNS:
            all_ok = all_ok and (col_i in ant_tbl.columns)
        if not all_ok:
            return
            
        for i, r in tenumerate(ant_tbl.iterrows()):
            # Достаем 
            sp = r[1][52] # Sphericity
            
            # Пропуск итерации, если сферичность выше необходимой
            if sp>sphericity:
                continue
            
            fname_spheres = f"out/{PREFIXES[True]}_{i}.out"
            fname_spheroids = f"out/{PREFIXES[False]}_{i}.out"
            res_spheres = self._readFile(fname_spheres)
            res_spheroids = self._readFile(fname_spheroids)
            sp = sp / 100.0
            sca = res_spheres[0]*sp+(1.0-sp)*res_spheroids[0]
            ext = res_spheres[1]*sp+(1.0-sp)*res_spheroids[1]
            absb = ext-sca
            volc = res_spheres[3]*sp+(1.0-sp)*res_spheroids[3]
            data = res_spheres[4]*sp+(1.0-sp)*res_spheroids[4]
            foutname = f"out/total_{i}.out"
            self._saveToFile(foutname, sca, ext, absb, data)
    
    def _readFile(self, fname):
        with open(fname, "rt") as fin:
            sca, ext, absb, volc = map(float,fin.readline().split())
            fin.readline()
            data = np.loadtxt(fin)
        return sca, ext, absb, volc, data
        
    def _saveToFile(self, fname, sca, ext, absb, data):
        with open(fname, "wt") as fout:
            print(f"{sca:.4f} {ext:.4f} {absb:.4f}", file=fout)
            print(f"theta s11 s12 s13 s14 s21 s22 s23 s24 s31 s32 s33 s34 s41 s42 s43 s44", file=fout)
            np.savetxt(fout, data, fmt='%.4e')
        
        