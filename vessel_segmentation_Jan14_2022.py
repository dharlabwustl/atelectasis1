#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itk
import vtk
import numpy as np
import sys,os,glob,subprocess


# In[2]:


# I_file='/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/Lungs/AHB1235/AHB1235_20200228084958_C_A_P_+cm_2.5_B20s.nii.gz'
# I_mask_file='/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/output_directory/AHB1235_20200228084958_C_A_P_+cm_2.5_B20s_lung_gray_seg_LTRCLobes_R231_bw.nii.gz'
# I_seg_file='/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/output_directory/AHB1235_20200228084958_C_A_P_+cm_2.5_B20s_lung_gray_seg_gt_neg500LTRCLobes_R231.nii.gz'


# In[3]:


# image = itk.imread(I_file,itk.ctype("float"))
# lung_mask = itk.imread(I_mask_file,itk.ctype("float"))
# image_mat=itk.GetArrayFromImage(image)
# lung_mask_mat=itk.GetArrayFromImage(lung_mask)
# image_mat[lung_mask_mat<1]=np.min(image_mat)
# image=itk.GetImageFromArray(image_mat)
# output_filename="testing.nii.gz"
# median = itk.median_image_filter(image, radius=2)

# itk.imwrite(median, output_filename)


# In[4]:


# hessian_image = itk.hessian_recursive_gaussian_image_filter(image, sigma=1)


# In[5]:


# vesselness_filter = itk.Hessian3DToVesselnessMeasureImageFilter[itk.ctype("float")].New()


# In[6]:


# output_filename="testing1.nii.gz"
# vesselness_filter.SetInput(hessian_image)
# vesselness_filter.SetAlpha1(0.5)
# vesselness_filter.SetAlpha2(2.0)
# # image=sitk.GetImageFromArray((sitk.GetArrayFromImage(image)*sitk.GetArrayFromImage(lung_mask))*)
# itk.imwrite(vesselness_filter, output_filename)


# In[7]:


# image_mat=itk.GetArrayFromImage(image)


# In[8]:


# directory_name='/home/atul/Documents/KAGGLE/datasets/NBI_DATASET/manifest-1586193031612/NSCLC-Radiomics/niigzfiles'
# master_directory='/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA'
directory_name=sys.argv[1] #os.path.join(master_directory,'Lungs/RENAMEDUNIQUE') #/FailedRound2/NewFiles')  #"/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/RELEVANTFILES/" #os.path.join(master_directory,'FromPorche/Lungs')  #'../LUNG/DATA/Prone_study' #####'/home/atul/Documents/LUNG/DATA'
# subdirectories=glob.glob(os.path.join(directory_name,'/*')) #"/path/to/directory/*/")
print(directory_name)

output_directory=sys.argv[2] #os.path.join(directory_name,'vessel_output_directory') ###'filter_output_directory')
# if os.path.exists(output_directory):
#     command="rm -r " + output_directory
#     subprocess.call(command,shell=True)

command="mkdir -p " + output_directory
subprocess.call(command,shell=True)
#'/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/FromPorche/filter_output_directory' #os.path.join(master_directory,'FromPorche/filter_output_directory')
output_file_csv=os.path.join(output_directory,'CT_ID_and_ateleactasis_volume.csv')
# print(subdirectories)
# print(files_name)
file_counter=0
# cuda.select_device(0)
## cuda.close()
atelectasis_percentage_list=[]
#atelectasis_percentage_list.append(['atelectasis_percentage','total_lung_voxel','total_atelectasis_voxel'])
# for each_dir in subdirectories:
each_dir=directory_name
files_name=glob.glob(os.path.join(each_dir,"*.nii*"))
files_name_in_output=glob.glob(os.path.join(output_directory,"*.nii*"))
print(files_name)

# # print(files_name)
for INPUT in files_name:
    current_file_noext= os.path.basename(INPUT).split('.nii')[0]
    print('current_file_noext')
    print(current_file_noext)
# #     ## find in output:
# #     analysis_flag=0
# #     for x in files_name_in_output:
# #         print(x)
# #         if current_file_noext in x :
# #             print('Analysis done')
# #             analysis_flag=1
# #             break
# #     # INPUT=I_file
# # #     print(INPUT)
# #     if analysis_flag==0 and "Premonitoring" not in INPUT and "Topogram" not in INPUT :
        
# #         image='' #None 
# #         lung_mask='' #None 
# #         image_mat='' #None 
# #         output_filename='' #None 
# #         hessian_image='' #None 
# #         vesselness_filter='' #None 
    I_file=INPUT #'/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/Lungs/AHB1235/AHB1235_20200228084958_C_A_P_+cm_2.5_B20s.nii.gz'
    print(I_file)
    image = itk.imread(I_file,itk.ctype("float"))
# #     #     I_mask_file=os.path.join(output_directory,os.path.basename(INPUT).split(".nii.gz")[0] + '_lung_gray_seg_LTRCLobes_R231_bw.nii.gz') #'/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/output_directory/AHB1235_20200228084958_C_A_P_+cm_2.5_B20s_lung_gray_seg_LTRCLobes_R231_bw.nii.gz'
# #     #     I_seg_file=os.path.join(output_directory,os.path.basename(INPUT).split(".nii.gz")[0] + '_lung_gray_seg_gt_neg500LTRCLobes_R231.nii.gz') #'/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/output_directory/AHB1235_20200228084958_C_A_P_+cm_2.5_B20s_lung_gray_seg_gt_neg500LTRCLobes_R231.nii.gz'
# #         if  file_counter<1: #'1657_' in INPUT and  ("LUNG_WINDOW" not in INPUT) and ("MRI" not in INPUT) and 
# #     #        file_counter=file_counter+1
# #             print(INPUT)
# #     # #         try:
#     for sigma in range(1,4):
#         image = itk.imread(I_file,itk.ctype("float"))
#     #             lung_mask = itk.imread(I_mask_file,itk.ctype("float"))
#     #             image_mat=itk.GetArrayFromImage(image)
#     #             lung_mask_mat=itk.GetArrayFromImage(lung_mask)
#     #             image_mat[lung_mask_mat<1]=np.min(image_mat)
#     #             image=itk.GetImageFromArray(image_mat)

# #         hessian_image = itk.hessian_recursive_gaussian_image_filter(image, sigma=sigma)
# #         vesselness_filter = itk.Hessian3DToVesselnessMeasureImageFilter[itk.ctype("float")].New()
# #         vesselness_filter.SetInput(hessian_image)
# #         for alpha1 in range(5,11,5):
# #             vesselness_filter.SetAlpha1(alpha1/10)
# #             for alpha2 in range(15,31,5):
# #                 vesselness_filter.SetAlpha2(alpha2/10)

# #     #                     vesselness_filter_array=itk.GetArrayFromImage(vesselness_filter)
# #     #                     vesselness_filter_array[vesselness_filter_array>0]=255
# #     # #                     # image=sitk.GetImageFromArray((sitk.GetArrayFromImage(image)*sitk.GetArrayFromImage(lung_mask))*)
# #     #                     vesselness_filter=itk.GetImageFromArray(vesselness_filter_array)
# #                 output_filename=os.path.join(output_directory,os.path.basename(INPUT).split(".nii")[0] + "_" +str(sigma) +"_" +str(alpha1) +"_" + str(alpha2) +'_vessels.nii.gz')
# #                 print(output_filename)
# #                 itk.imwrite(vesselness_filter, output_filename)

# #     # #         except :
# #     # #             print("Exception")

# #     #     del image 
# #     # #     del lung_mask 
# #     # #     del image_mat 
# #     #     del output_filename
# #     #     del hessian_image 
# #     #     del vesselness_filter

# #     # In[ ]:




