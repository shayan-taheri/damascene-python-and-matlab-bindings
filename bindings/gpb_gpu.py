import numpy as np
import os
from scipy.weave import inline,converters

cuda_drv_path="/usr/lib/nvidia-current"
cuda_sdk_path="/usr/local/cuda/C/lib"
cuda_path="/usr/local/cuda/lib"
acml_path="/home/local/amueller/acml4.4.0/ifort64/lib"

objects="combine.cu_o rotate.cu_o skeleton.cu_o kmeans.cu_o nonmax.cu_o gradient.cu_o parabola.cu_o spectralPb.cu_o stencilMVM.cu_o localcues.cu_o gpb.cu_o texton.cu_o lanczos.cu_o convert.cu_o Stencil.cpp_o globalPb.cu_o filters.cpp_o intervening.cu_o".split(" ")
objects_dir=[os.path.join("../obj/release/",obj) for obj in objects]
libraries="cuda cutil cudart cublas acml".split()
library_dirs=[cuda_path,cuda_sdk_path,cuda_drv_path,acml_path]

def gpb(image):
    [height, width]=image.shape[:2]
    borders=np.zeros([height,width],np.float32)
    orientations=np.zeros([8,width,height],np.float32)
    textons=np.zeros([height,width],np.int32)
    padded_image=np.zeros([height,width,4],np.uint8)
    padded_image[:,:,:3]=image.astype(np.uint8)
    code="""
         gpb((unsigned int*)&padded_image(0,0),width,height,&borders(0,0),&textons(0,0),&orientations(0,0));
         """
    inline(code,['padded_image','textons','width', 'height','borders','orientations'], type_converters=converters.blitz, compiler = 'gcc',headers=['"gpb.h"'],include_dirs=['.'],extra_objects=objects_dir,libraries=libraries,library_dirs=library_dirs,verbose=0,force=1)
    orientations=orientations.T
    return [borders,textons,orientations]


if __name__ == "__main__":
    import Image
    import matplotlib.pyplot as plt
    image=Image.open('../damascene/polynesia.ppm')
    data=np.array(image.getdata()).reshape(image.size[1],image.size[0],3)
    [borders,textons,orientations]=gpb(data);

    plt.matshow(borders)
    plt.matshow(textons)
    plt.show()

