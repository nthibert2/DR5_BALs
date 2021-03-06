""" Bulk download of spectra from the SDSS database
spectra are from the QSO database and have a redshift range of 1.6-2.1
To generate the links to the FITS files, I am getting the file name from the DR10 catalog of Paris et al. 2014
"""

import numpy as np
from astropy.table import Table, Column
import subprocess
import wget
import tarfile
import shutil
import os



def dr5_download(bals, plates_dir, balq_dir):

    """download a list of plates from SDSS DR5. Extract specific files with specific MJDs and FiberIDs 
        bals: file with BAL quasars from DR5 that also contains plate, mjd, and fiberid for each row.
        plates_dir: directory where you want the plates to be downloaded to
        balq_dir: directory where your data (FITS files) for the DR5 BAL catalog only will be saved
        
        you need to create thses two direcrories in advance if you don't have them on your local machine
        
        """
    
    os.mkdir(plates_dir)
    os.mkdir(balq_dir)

    catalog= Table.read(bals)
    all_plates= catalog['plate'][]
    plates= set(all_plates) #select only the unique values

    links_list= []

    for plate_num in plates:
        links_list.append('http://das.sdss.org/spectro/ss_tar_23/'+str(plate_num).zfill(4)+'.tar.gz')


    #now download. this will take a long time
    
    i= 0
    for line in links_list:
        print "Go take a nap Nathalie! This is gonna take a looong time"
        wget.download(line, out=plates_dir)
        i=+1
        print "\n Downloaded", i, "of", len(links_list), "files"

        
    for p in plates:
        
        mjd_ls= catalog['mjd'][catalog['plate']== p]
        fib_ls= catalog['fiberid'][catalog['plate']== p]
        
        plate_num= str(p).zfill(4)
        print "extracting files from plate", plate_num
        print "plate", plate_num, "has", len(mjd_ls), "spectra from DR5 BAL catalog"
        
        tarball= tarfile.open(plates_dir+plate_num+".tar.gz", "r")
        tarball.extractall()
        tarball.close()
        
        spec_file_names= []
        for f in range(len(mjd_ls)):

            spec_file_names.append(plate_num+"/spSpec/spSpec-"+str(mjd_ls[f])+"-"+plate_num+"-"+str(fib_ls[f]).zfill(3)+".fit")
            
        for spec_file in spec_file_names:
            shutil.copy2(spec_file, balq_dir)

        subprocess.call(["rm", "-R", plate_num])








