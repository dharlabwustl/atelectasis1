#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys,os,glob,subprocess
import SimpleITK as sitk
import numpy as np
import nibabel as nib
import cv2 as cv
from niwidgets import NiftiWidget, examplet1
import matplotlib.pyplot as plt
import re
from skimage import exposure
import cv2
import pandas as pd

sys.path.append("/storage1/fs1/dharr/Active/ATUL/PROJECTS/NWU/SOFTWARE/")
 
from utilities_simple_latex import * 

def mask_on_image(grayimagefile,maskimagefile,ext_img='jpg'):
    I=cv2.imread(grayimagefile) 
    mask=cv2.imread(maskimagefile) 
    mask1=mask[:,:,0]
    I[:,:,0][mask1>0]=0
    I[:,:,1][mask1>0]=0
    I[:,:,2][mask1>0]=255
    slice_num=maskimagefile[-7:-4]
    filetoseave=maskimagefile.split(slice_num+"."+ext_img)[0] +"superimp"+ str(slice_num)+"." + ext_img
    cv2.imwrite(filetoseave,I)
    return filetoseave


def saveslicesofnifti_1(filename,in_range=(0,200),savetodir="",ismask=False):
    filename_nib=nib.load(filename)
    filename_gray_data_np=filename_nib.get_fdata()
    min_img_gray=np.min(filename_gray_data_np)
    print("MAX VALUE={}".format(np.max(filename_gray_data_np)))
    img_gray_data=0
    if ismask==True:
        filename_gray_data_np[filename_gray_data_np>0]=1
        img_gray_data=filename_gray_data_np.copy()
    else:
        img_gray_data=exposure.rescale_intensity( filename_gray_data_np , in_range=(in_range[0], in_range[1]))
    if not os.path.exists(savetodir):
        savetodir=os.path.dirname(filename)

    for x in range(img_gray_data.shape[2]):
        img_gray_data_flat=img_gray_data[:,:,x].flatten()
        img_gray_data_flat=img_gray_data_flat[img_gray_data_flat>np.min(img_gray_data)]
        if len(img_gray_data_flat)>1:
            cv2.imwrite(os.path.join(savetodir,re.sub('[^a-zA-Z0-9]', '_',os.path.basename(filename).split(".nii")[0])+str("{:03d}".format(x))+".jpg" ),img_gray_data[:,:,x]*255 )


# In[4]:


grayscale_dir=sys.argv[1] #"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/Lungs/RENAMEDUNIQUE"


# In[5]:


masks_dir=sys.argv[2] #os.path.join(grayscale_dir,'lungmask') #"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/output_directory/"
vesselmasks_dir=sys.argv[3] #os.path.join(grayscale_dir,'vessel_output_directory')  ##"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/vessel_output_directory/"
vesselmasks_modified_dir=sys.argv[4] #os.path.join(grayscale_dir,'vessel_mod_output_directory_nooc') ##"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/vessel_mod_output_directory/"
atelectasis_mask_dir=sys.argv[5] 
# output_dir=atelectasis_mask_dir #os.path.join(grayscale_dir,'percentage_output_directory_nooc')  ##"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/percentage_output_directory/"
# command="mkdir -p " + output_dir
# subprocess.call(command,shell=True)
# command="mkdir -p " + vesselmasks_modified_dir
# subprocess.call(command,shell=True)
all_gray_files=glob.glob(os.path.join(grayscale_dir,"*.nii*"))
counter=0
sigma=2   
alpha1=5  
alpha2=15
each_grayfile=sys.argv[9] #all_gray_files[0]
grayfile_basename_noext=os.path.basename(each_grayfile).split(".nii")[0]
vesselmask_filename=os.path.join(vesselmasks_dir,grayfile_basename_noext+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) +'_vessels.nii.gz') #'_vessels.nii.gz')
vesselmask_itk_arr_itk_fn=os.path.join(vesselmasks_modified_dir,grayfile_basename_noext+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) +'_vessels_modfd.nii.gz') 
print(vesselmask_filename)
# load grayscale
print(each_grayfile)
grayfile_itk=sitk.ReadImage(each_grayfile)
grayfile_itk_arr=sitk.GetArrayFromImage(grayfile_itk)
counter+=1

lungmask_filename=os.path.join(masks_dir,grayfile_basename_noext+'_lung_gray_seg_LTRCLobes_R231_bw.nii.gz')
lungmask_itk=sitk.ReadImage(lungmask_filename) # .get_fdata()
lungmask_itk_arr=sitk.GetArrayFromImage(lungmask_itk)
lungmask_itk_arr[grayfile_itk_arr<-400]=np.min(lungmask_itk_arr)
lungmask_itk_arr_itk=sitk.GetImageFromArray(lungmask_itk_arr)
lungmask_itk_arr_itk.CopyInformation(lungmask_itk)
subt_filename=os.path.join(atelectasis_mask_dir,grayfile_basename_noext+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) + "_OCVOC.nii.gz")

print(vesselmask_filename)
if os.path.exists(vesselmask_filename):
    print("I am here")
    vesselmask_itk=sitk.ReadImage(vesselmask_filename)#.get_fdata()
    vesselmask_itk_arr=sitk.GetArrayFromImage(vesselmask_itk)
# #         lungmask_itk_arr[grayfile_itk_arr<-400]=np.min(lungmask_itk_arr)
    lungmask_itk_arr_itk_arr=sitk.GetArrayFromImage(lungmask_itk_arr_itk)

    lungmask_itk_arr_itk_arr[vesselmask_itk_arr>2]=np.min(lungmask_itk_arr_itk_arr)
    lungmask_itk_arr_itk_arr_itk=sitk.GetImageFromArray(lungmask_itk_arr_itk_arr)
    lungmask_itk_arr_itk_arr_itk.CopyInformation(lungmask_itk)
#     cleaned_thresh_img = sitk.BinaryOpeningByReconstruction(lungmask_itk_arr_itk_arr_itk, [3, 3, 3])
#     cleaned_thresh_img = sitk.BinaryClosingByReconstruction(cleaned_thresh_img, [3, 3, 3])
#     cleaned_thresh_img.CopyInformation(lungmask_itk)
#         subt_filename=os.path.join(output_dir,grayfile_basename_noext+"_subt1.nii.gz")


    sitk.WriteImage(lungmask_itk_arr_itk_arr_itk,subt_filename)
    vesselmask_itk_arr[vesselmask_itk_arr<=2]=np.min(vesselmask_itk_arr)
    vesselmask_itk_arr[grayfile_itk_arr<-400]=np.min(vesselmask_itk_arr)
    vesselmask_itk_arr_itk=sitk.GetImageFromArray(vesselmask_itk_arr)
    vesselmask_itk_arr_itk.CopyInformation(vesselmask_itk)
#                         vesselmask_itk_arr_itk_fn=os.path.join(vesselmasks_modified_dir,grayfile_basename_noext+'_3_5_20_vessels_modfd.nii.gz') 
    sitk.WriteImage(vesselmask_itk_arr_itk,vesselmask_itk_arr_itk_fn)


# # In[6]:



image_dir=sys.argv[6] #os.path.join(grayscale_dir,'imagesforpdfs_nooc')


grayfilename=sys.argv[9]  #all_gray_files[0]

grayfile_basename_noext=os.path.basename(grayfilename).split(".nii")[0]

atelectasis_filename=os.path.join(atelectasis_mask_dir,grayfile_basename_noext+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) + "_OCVOC.nii.gz")
if os.path.exists(atelectasis_filename):
    saveslicesofnifti_1(atelectasis_filename,in_range=(0,1),savetodir=image_dir,ismask=True)

    saveslicesofnifti_1(grayfilename,in_range=(-400,200),savetodir=image_dir)

    lung_mask_filename=os.path.join(masks_dir,grayfile_basename_noext+"_lung_gray_seg_LTRCLobes_R231_bw.nii.gz")
    saveslicesofnifti_1(lung_mask_filename,in_range=(0,1),savetodir=image_dir,ismask=True)
    vesselmask_filename=os.path.join(vesselmasks_modified_dir,grayfile_basename_noext+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) +'_vessels_modfd.nii.gz')
    saveslicesofnifti_1(vesselmask_filename,in_range=(0,1),savetodir=image_dir,ismask=True)
    counter=counter+1



directoryname=image_dir #os.path.join(grayscale_dir,'imagesforpdfs_nooc') #"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/imagesforpdfs"
# directoryname
# allfiles=glob.glob(os.path.join(grayscale_dir,"*.nii*"))
files_with1ext=sorted(glob.glob(os.path.join(directoryname,re.sub('[^a-zA-Z0-9]',"_",grayfile_basename_noext)+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) +"_OCVOC*")))
derived_img_ext= "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) +"_OCVOC"
counter=counter+1
for file in files_with1ext:
    number=file[-7:-4]
    basefile=file.split(derived_img_ext)[0] + str(number)+".jpg"  
#     print(basefile)
    if os.path.exists(basefile):
#             print(basefile)
#     print(file)
        filename1=mask_on_image(basefile,file,ext_img='jpg')
#     print(file)



counter=0
calculation_output_directory=sys.argv[7]  #os.path.join(grayscale_dir,'calculation_output_directory_nooc')
atelectasis_percentage_list=[]
grayfile_basename_noext=os.path.basename(grayfilename).split(".nii")[0]
atelectasis_filename=os.path.join(atelectasis_mask_dir,grayfile_basename_noext+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) + "_OCVOC.nii.gz")
# print(atelectasis_filename)
#                 atelectasis_filename=os.path.join(atelectasis_mask_dir,grayfile_basename_noext+"_OCVOC.nii.gz")
# if os.path.exists(atelectasis_filename):
print("I AM HERE")
atelectasis_filename_nib=nib.load(atelectasis_filename)
atelectasis_filename_nib_data=atelectasis_filename_nib.get_fdata()
atelectasis_filename_nib_data=atelectasis_filename_nib_data[atelectasis_filename_nib_data>0]
atelectasis_filename_nib_data_len=atelectasis_filename_nib_data.shape[0]
lung_mask_filename=os.path.join(masks_dir,grayfile_basename_noext+"_lung_gray_seg_LTRCLobes_R231_bw.nii.gz")
lung_mask_filename_nib=nib.load(lung_mask_filename)
lung_mask_filename_nib_data=lung_mask_filename_nib.get_fdata()
lung_mask_filename_nib_data=lung_mask_filename_nib_data[lung_mask_filename_nib_data>0]
lung_mask_filename_nib_data_len=lung_mask_filename_nib_data.shape[0]
print("{}:{}:{}".format(grayfilename,atelectasis_filename_nib_data_len,lung_mask_filename_nib_data_len))
atelectasis_percentage=(atelectasis_filename_nib_data_len/lung_mask_filename_nib_data_len) * 100
atelectasis_percentage_list.append([grayfile_basename_noext,atelectasis_percentage,lung_mask_filename_nib_data_len,atelectasis_filename_nib_data_len])
#         print(lung_mask_filename_nib_data_len)
output_file_csv=os.path.join(calculation_output_directory,grayfile_basename_noext+'CT_ID_and_ateleactasis_volume'+ "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) + "_OCVOC_"+'.csv')
atelectasis_percentage_df=pd.DataFrame(atelectasis_percentage_list)
atelectasis_percentage_df.columns =['FILENAME','atelectasis_percentage','total_lung_voxel','total_atelectasis_voxel']
atelectasis_percentage_df.to_csv(output_file_csv,index=False)
print(output_file_csv)
directory_tosave_images=image_dir
original_ct_fn=grayfilename
filename_=[]
filename_.append([os.path.basename(original_ct_fn).split(".nii")[0]])
filename_df=pd.DataFrame(filename_)
filename_df.columns=['FILENAME']
latexfile_directory=sys.argv[8]  #os.path.join(grayscale_dir,"TEXFILES")
latexfilename=os.path.join(latexfile_directory,re.sub('[^a-zA-Z0-9]', '_',os.path.basename(original_ct_fn).split(".nii")[0])+'.tex')

latex_start(latexfilename)
latex_begin_document(latexfilename)
latex_start_tableNc_noboundary(latexfilename,1)
latex_insert_line_nodek(latexfilename,text=filename_df.to_latex(index=False))
latex_end_table2c(latexfilename)
latex_start_tableNc_noboundary(latexfilename,1)
atelectasis_percentage_df=atelectasis_percentage_df.drop(['FILENAME'], axis=1)
latex_insert_line_nodek(latexfilename,text=atelectasis_percentage_df.to_latex(index=False))
latex_end_table2c(latexfilename)
for each_slice_file in sorted(glob.glob(os.path.join(directory_tosave_images,os.path.basename(original_ct_fn).split(".nii")[0]+'_lung_gray_seg_LTRCLobes_R231_bw*.jpg'))) : ##original_ct_fn_nib_data.shape[2]):
#     print(each_slice_file)
# # #     print(original_ct_fn_nib_data.shape[0])
    slice_num=int(os.path.basename(each_slice_file)[-7:-4])
#     print(slice_num)

    grayscale_slice_fn=os.path.join(directory_tosave_images,re.sub('[^a-zA-Z0-9]', '_',os.path.basename(original_ct_fn).split(".nii")[0])+str("{:03d}".format(slice_num))+".jpg" )
    if     os.path.exists(grayscale_slice_fn):
        print(grayscale_slice_fn)
    vessel_image=os.path.join(directory_tosave_images,re.sub('[^a-zA-Z0-9]', '_',os.path.basename(original_ct_fn).split(".nii")[0])+'_2_5_15_vessels_modfd'+ str("{:03d}".format(slice_num))+".jpg" )
    if     os.path.exists(vessel_image):
        print(vessel_image)
    atelectasismask_image=os.path.join(directory_tosave_images,re.sub('[^a-zA-Z0-9]', '_',os.path.basename(original_ct_fn).split(".nii")[0])+'_2_5_15_OCVOC'+ str("{:03d}".format(slice_num))+".jpg" )
    if     os.path.exists(atelectasismask_image):
        print(atelectasismask_image)
    atelectasismask_gray_superim_image=os.path.join(directory_tosave_images,re.sub('[^a-zA-Z0-9]', '_',os.path.basename(original_ct_fn).split(".nii")[0])+'_2_5_15_OCVOCsuperimp'+ str("{:03d}".format(slice_num))+".jpg" )
    if     os.path.exists(atelectasismask_gray_superim_image):
        print(atelectasismask_gray_superim_image)
    if os.path.exists(grayscale_slice_fn) and os.path.exists(vessel_image) and os.path.exists(atelectasismask_image) and os.path.exists(atelectasismask_gray_superim_image):
        allfilewithbaseprefix=[grayscale_slice_fn,each_slice_file,vessel_image,atelectasismask_image,atelectasismask_gray_superim_image]

        latex_start_tableNc_noboundary(latexfilename,len(allfilewithbaseprefix))
        latex_insertimage_tableNc_v1(latexfilename,allfilewithbaseprefix,len(allfilewithbaseprefix), caption="FIGURE",imagescale=1/(1+len(allfilewithbaseprefix)), angle=90,space=1)
    #     #             print(allfilewithbaseprefix)
        latex_end_table2c(latexfilename)
latex_end(latexfilename)


# # In[ ]:



