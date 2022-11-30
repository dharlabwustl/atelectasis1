#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob ,os,subprocess,sys
import pandas  as pd
import numpy   as np
import nibabel as nib
import matplotlib.pyplot as plt
from lungmask import mask
import SimpleITK as sitk
from skimage import exposure
from lungmask import mask
import SimpleITK as sitk
from numba import cuda


# In[2]:


def read_nii(filepath):
    '''
    Reads .nii file and returns pixel array
    '''
    ct_scan = nib.load(filepath)
    array   = ct_scan.get_fdata()
    array   = np.rot90(np.array(array))
    return(array)
def plot_sample(array_list, color_map = 'gray'):
    '''
    Plots and a slice with all available annotations
    '''
    fig = plt.figure(figsize=(18,15))
    plt.subplot(1,1,1)
    plt.imshow(array_list[0], cmap='gray')
    plt.title('Original Image')
def segment_lesion_area(filename_nifti,algorithm_name='',output_directory='./'):
    input_image = sitk.ReadImage(filename_nifti)
    # model = mask.get_model('unet','LTRCLobes_R231') #LTRCLobes')
    segmentation = mask.apply_fused(input_image)  # default model is U-net(R231)

    if len(algorithm_name)>0:
        if algorithm_name=='LTRCLobes':
            model = mask.get_model('unet','LTRCLobes')
            segmentation = mask.apply(input_image, model)
            
        elif algorithm_name=='LTRCLobes_R231':
            segmentation = mask.apply_fused(input_image)  # default model is U-net(R231)
    elif  algorithm_name=='R231' or len(algorithm_name)==0:
            segmentation = mask.apply(input_image)
    print(np.max(segmentation))
    print(np.min(segmentation))
    segmentation[segmentation>0]=1      
    segmentation_gray=sitk.GetArrayFromImage(input_image) #()
    segmentation_gray_gt_neg500=np.copy(segmentation_gray)
    ## all lung area in gray scale:
    segmentation_gray[segmentation<1]=np.min(segmentation_gray)
    ## 
    # segmentation_gray[segmentation_gray<0]=np.min(segmentation_gray)
    # segmentation_gray[segmentation_gray>200]=np.min(segmentation_gray)
    # segmentation_gray=exposure.rescale_intensity(segmentation_gray , in_range=(-500, 200))*255
    segmentation_mask =np.copy(segmentation)
    segmentation_mask_gt_neg500=np.copy(segmentation)

    
# def write_nifti_from_itk(segmentation_gray,filename_nifti):
    input_image = sitk.ReadImage(filename_nifti)
    segmentation_mask_itk=sitk.GetImageFromArray(segmentation_gray)
        #     complete lung mask:
    segmentation_mask_bw_itk=sitk.GetImageFromArray(segmentation_mask)
    segmentation_mask_bw_itk.CopyInformation(input_image)
    
    ## mask_file_binary
    file_mask_lung_bw=filename_nifti.split(".nii")[0]+'_lung_gray_seg_' + algorithm_name+ '_bw.nii.gz' #NECT_filename.split(".nii")[0]+'_BET_TEST.nii.gz'
    print('file_mask_lung_bw is {}'.format(file_mask_lung_bw))
    sitk.WriteImage(segmentation_mask_bw_itk,os.path.join(output_directory,os.path.basename(file_mask_lung_bw)),True)
    total_lung_voxel=np.sum(segmentation)
 
    # mask_file_nii gray
    segmentation_mask_itk.CopyInformation(input_image)   
    file_mask_lung=filename_nifti.split(".nii")[0]+'_lung_gray_seg_' + algorithm_name+ '.nii.gz' #NECT_filename.split(".nii")[0]+'_BET_TEST.nii.gz'
    print('file_mask_lung is {}'.format(file_mask_lung))
    sitk.WriteImage(segmentation_mask_itk,os.path.join(output_directory,os.path.basename(file_mask_lung)),True)
    
    ## grayscale image above -500 HU
    segmentation_mask_gt_neg500[segmentation_gray_gt_neg500<-500]=np.min(segmentation_mask_gt_neg500)
    segmentation_gray_gt_neg500[segmentation_gray_gt_neg500<-500]=np.min(segmentation_gray_gt_neg500)
    segmentation_gray_gt_neg500[segmentation<1]=np.min(segmentation_gray_gt_neg500)
    segmentation_gray_gt_neg500_itk=sitk.GetImageFromArray(segmentation_gray_gt_neg500)
    segmentation_gray_gt_neg500_itk.CopyInformation(input_image)
    file_segmentation_gray_gt_neg500_itk=filename_nifti.split(".nii")[0]+'_lung_gray_seg_gt_neg500' + algorithm_name+ '.nii.gz' #NECT_filename.split(".nii")[0]+'_BET_TEST.nii.gz'
    print('file_segmentation_gray_gt_neg500_itk is {}'.format(file_segmentation_gray_gt_neg500_itk))
    sitk.WriteImage(segmentation_gray_gt_neg500_itk,os.path.join(output_directory,os.path.basename(file_segmentation_gray_gt_neg500_itk)),True)
    
    ## binary mask image above -500 HU

    
    segmentation_mask_gt_neg500_itk=sitk.GetImageFromArray(segmentation_mask_gt_neg500)
    segmentation_mask_gt_neg500_itk.CopyInformation(input_image)
    file_segmentation_mask_gt_neg500_itk=filename_nifti.split(".nii")[0]+'_lung_mask_seg_gt_neg500' + algorithm_name+ '.nii.gz' #NECT_filename.split(".nii")[0]+'_BET_TEST.nii.gz'
    print('file_segmentation_mask_gt_neg500_itk is {}'.format(file_segmentation_mask_gt_neg500_itk))
    sitk.WriteImage(segmentation_mask_gt_neg500_itk,os.path.join(output_directory,os.path.basename(file_segmentation_mask_gt_neg500_itk)),True)
    

    total_atelectasis_voxel=np.sum(segmentation_mask_gt_neg500)
    atelectasis_percentage=(total_atelectasis_voxel/total_lung_voxel) * 100
    print("Filename{}".format(filename_nifti.split(".nii")[0]))
    print('atelectatis volume : {}'.format(total_atelectasis_voxel))
    print('total_lung volume : {}'.format(total_lung_voxel))
    print("Atelectasis percentage : {}".format(atelectasis_percentage))

#     device = cuda.get_current_device()
#     device.reset()
    
    
    
    
    
    
#     ## 
#     cuda.select_device(0)
# #     cuda.close()
#     while cuda.cudadrv.driver.Context(0,handle).get_memory_info()[0] < 7000000000:    #886471168
#         cuda.close()
#     else:
#         print('Memory freed')
    
    return atelectasis_percentage,total_lung_voxel,total_atelectasis_voxel
    


# In[ ]:


# master_directory='/storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA'
# /storage1/fs1/dharr/Active/ATUL/PROJECTS/LUNGS/DATA/Lungs/RENAMEDUNIQUE/FailedRound1/NewFiles directory_name='/home/atul/Documents/KAGGLE/datasets/NBI_DATASET/manifest-1586193031612/NSCLC-Radiomics/niigzfiles'
directory_name=sys.argv[1] #os.path.join(master_directory,'Lungs/RENAMEDUNIQUE') #/FailedRound2/NewFiles') #'/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/Lungs' #'../LUNG/DATA/Prone_study' #####'/home/atul/Documents/LUNG/DATA'
# subdirectories=glob.glob(os.path.join(directory_name,'*/')) #"/path/to/directory/*/")


output_directory=sys.argv[2] ##os.path.join(directory_name,'lungmask') #'output_directory1') 
command="rm  -r  " + output_directory + "/*" 
subprocess.call(command,shell=True)
# command="mkdir -p  " + output_directory  
# subprocess.call(command,shell=True)
#'/media/atul/AC0095E80095BA32/WASHU_WORK/PROJECTS/LUNGS/DATA/FromPorche/output_directory'
output_file_csv=os.path.join(output_directory,'CT_ID_and_ateleactasis_volume.csv')
# print(subdirectories)
# print(files_name)
file_counter=0
# cuda.select_device(0)
## cuda.close()
atelectasis_percentage_list=[]
#atelectasis_percentage_list.append(['atelectasis_percentage','total_lung_voxel','total_atelectasis_voxel'])
# for each_dir in subdirectories:
files_name=reversed(glob.glob(os.path.join(directory_name,"*.nii*")))

# print(each_dir)
counter=0
for INPUT in files_name:
    print(INPUT)
    if counter == 0: 
#         counter=counter+1
    #     if  ("LUNG_WINDOW" not in INPUT) and ("MRI" not in INPUT) and ("Volume" not in INPUT) and file_counter<3: #'1657_' in INPUT and 
    # #             file_counter=file_counter+1
    #         print(INPUT)
        try:
            atelectasis_percentage,total_lung_voxel,total_atelectasis_voxel=segment_lesion_area(INPUT,'LTRCLobes_R231',output_directory)
            atelectasis_percentage_list.append([os.path.basename(INPUT),atelectasis_percentage,total_lung_voxel,total_atelectasis_voxel])
    #                 atelectasis_percentage_list.append(['atelectasis_percentage','total_lung_voxel','total_atelectasis_voxel'])
        except :
            print("Exception")
            continue 
    #             device = cuda.get_current_device()
    #             device.reset()
    #         device = cuda.get_current_device()
    #         device.reset()
    #        cuda.select_device(0)
    #        cuda.close()
    #        cuda.select_device(0)


    #     INPUT="/home/atul/Documents/LUNG/DATA/SAH_90_02182015_PE_1.0_B20f_20150218212130_4.nii"
    # input_image = sitk.ReadImage(INPUT)
    # segmentation = mask.apply(input_image)  # default model is U-net(R231)
atelectasis_percentage_df=pd.DataFrame(atelectasis_percentage_list)
atelectasis_percentage_df.columns =['Filename','atelectasis_percentage','total_lung_voxel','total_atelectasis_voxel']
atelectasis_percentage_df.to_csv(output_file_csv,index=False)

# In[ ]:


# np.sum(segmentation)
# cuda.select_device(0)
# handle=''

# cuda.cudadrv.driver.Context(0,handle).get_memory_info()[0]
# 261441/1650672  * 100


# In[ ]:


# for x in range(segmentation.shape[2]):
# plot_sample([segmentation[20,:,:]*255])


# In[ ]:


# percentage_atel={'AFF2485_20180630_0132':0.12,

