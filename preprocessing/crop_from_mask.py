from .Display_mask import load_coco, load_annotation, find_image

import numpy as np
import cv2 as cv
from skimage.draw import polygon
import os

def crop_from_mask(dataset,annotation_numb,cropped_im):
    """Crops the region of interest in the cropped_im image
    
    Parameters
    ----------
    annotation_numb : list, [x,y,width,height]
        The annotation number from the COCO dataset.
    cropped_im : Array-like image<
        The image from fill_mask, where the background is removed and only
        region of intereset is shown, rest is black.

    Returns
    -------
    cropped : Array-like image
        Returns the cropped image with only the region of interest of dimension
        x*y

    """
    start_x = min(dataset['annotations'][annotation_numb]['segmentation'][0][0::2])
    start_y = min(dataset['annotations'][annotation_numb]['segmentation'][0][1::2])
    end_x = max(dataset['annotations'][annotation_numb]['segmentation'][0][0::2])-start_x
    end_y = max(dataset['annotations'][annotation_numb]['segmentation'][0][1::2])-start_y

    cropped = cropped_im[start_y:start_y+end_y,start_x:start_x+end_x]

    return cropped

def fill_mask(dataset,image_id,annotation,image_name,image_path):
    """ Takes the segmentations from COCO dataset and discards the background 
    (ie. the region that is not withing interest)

    Parameters
    ----------
    image_id : int
        The image_id from the COCO dataset
    annotation : list, [x,y,x,y...x,y]
        The segmentation mask obtained from the COCO dataset
    image_name : str
        The name of the image where the mask orignates from

    Returns
    -------
    cropped_im : Returns the cropped image, where the area of interest has
    been cropped out and put on a black background

    """
    for i in range(len(dataset['images'])):
        if (dataset['images'][i]['id']==image_id):
            height = dataset['images'][i]['height']
            width = dataset['images'][i]['width']
    mini_img = np.zeros((height,width),dtype=bool)
    x, y = (annotation[0][0::2]),(annotation[0][1::2])
    for x_x,y_y in zip(x,y):
        x_x, y_y = int(x_x), int(y_y)
        mini_img[y_y,x_x]=True
    img=mini_img.astype(int)

    row, col = polygon(y, x, img.shape)
    img[row,col] = 1
    PATH = os.path.join(image_path, image_name)
    orig_im = cv.imread(PATH)
    orig_im = cv.cvtColor(orig_im, cv.COLOR_BGR2RGB)
    orig_im = np.uint8(orig_im)
    cropped_im = cv.bitwise_and(orig_im, orig_im, mask=np.uint8(img))
    return cropped_im

def overlay_on_larger_image(larger_image,smaller_image,x=None,y=None):
    """ Place an object from a mask upon an image that is larger or same size as the object image
    Parameters
    ----------
    larger_image : array-like
        The background image to be overlayed upon
    smaller_image : array-like
        The object to be placed on the larger_image
    x : int. Optional
        Where to place the object in respect to origo on the x-axis
        Optional. The default is None.
    y : int. Optional
        Where to place the object in respect to origo on the y-axis
        The default is None.

    Returns
    -------
    Displays the resulting image.

    """
    if x == None:
        x = np.random.randint(0,(larger_image.shape[1]-smaller_image.shape[1]))
    if y == None:
        y = np.random.randint(0,(larger_image.shape[0]-smaller_image.shape[0]))
    temp = larger_image[y:y+smaller_image.shape[0], x:x+smaller_image.shape[1]] # Selecting a window of the image to edit
    temp[smaller_image>0] = 0 # All the places where the object is, is set to 0. Where the mask is 0, does remains unchanged from the larger_image
    temp += smaller_image * (smaller_image > 0) #the object is added to the blackened image
    larger_image[y:y+smaller_image.shape[0], x:x+smaller_image.shape[1]] = temp # The window is put back into larger_image
    return larger_image

imported = True
if not imported:  
    annotation_path = r'C:\Users\Cornelius\Documents\GitHub\Bscproject\Bsc_Thesis_Instance_segmentation\preprocessing\COCO_Test.json'
    image_dir = 'C:/Users/Cornelius/Documents/GitHub/Bscproject/Bsc_Thesis_Instance_segmentation/preprocessing/'
    image_numb = 1
    dataset = load_coco(annotation_path)
    background = cv.imread("sunset.jfif")
    background = cv.cvtColor(background, cv.COLOR_BGR2RGB)
    image_name,image_id = find_image(dataset, image_numb)
    #image_name = "Test_Rye_Midsummer_Dense_series1_20_08_20_10_33_01.jpg"
    
    annote_ids = []
    for i in range(len(dataset['annotations'])):
        if dataset['annotations'][i]['image_id']==image_numb:
            annote_ids.append(i)
    for idx in annote_ids:
        bbox, annotation = load_annotation(dataset, idx,image_numb)
        cropped_im = fill_mask(image_id,annotation,image_name)
        cropped = crop_from_mask(dataset,idx,cropped_im)
        overlay_on_larger_image(background,cropped)
        #plt.imshow(cropped)
        #plt.show()
    
