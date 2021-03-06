
#include <mex.h>
#include "gpb.h"

void mexFunction(int nOut, mxArray *pOut[],
		 int nIn, const mxArray *pIn[])
{
  mwSize width, height;
  float* borders;
  float* orientations;
  int* textons;
  unsigned int *in_image;
  mwSize dims[3];
  mwSize orientation_dims[3];

  if((nIn != 1) || (nOut != 3))
    mexErrMsgTxt("Usage: border,textons,orientations = gpb(image)");
if (!mxIsClass(pIn[0],"uint8") || mxGetNumberOfDimensions(pIn[0]) != 3) {
		mexErrMsgTxt("Usage: th argument must be a unsigned int matrix");
	}
  const mwSize *indims= mxGetDimensions(pIn[0]);
  if (indims[0]!=4)
	  mexErrMsgTxt("Image needs to be of shape 4 x widht x height");
  width = indims[2];
  height = indims[1];
  mexPrintf("width %d, height %d\n",width,height);
  mexPrintf("Element-size: %d, sizeof(int): %d, sizeof(char) %d\n",mxGetElementSize(pIn[0]),sizeof(int),sizeof(unsigned char));
  dims[0]=width; dims[1]=height; //for rgb0
  mexPrintf("width: %d height: %d\n",width, height);
  pOut[0]=mxCreateNumericMatrix(height,width,mxSINGLE_CLASS,mxREAL);
  pOut[1]=mxCreateNumericMatrix(height,width,mxINT32_CLASS,mxREAL);
  orientation_dims[0]=width; orientation_dims[1]=height; orientation_dims[2]=8;
  pOut[2]=mxCreateNumericArray(3,orientation_dims,mxSINGLE_CLASS,mxREAL);

  borders=(float*) mxGetPr(pOut[0]);
  textons=(int*) mxGetPr(pOut[1]);
  orientations=(float*) mxGetPr(pOut[2]);

  in_image = (unsigned int*) mxGetData(pIn[0]);
  gpb(in_image,height,width,borders,textons,orientations); 
}
