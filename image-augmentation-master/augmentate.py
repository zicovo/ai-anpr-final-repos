import os
import matplotlib.image as mpimg
from skimage import exposure
from cv2 import flip
import sys

def create_folder(name):
  if not os.path.exists(name):
    os.makedirs(name)

base_path = 'images_v2'

# Path to original images that we need to augmentate
original_cropped_images = f'./{base_path}/cropped_images'

# Path where all augmented images will be stored
augmented_path = f'./{base_path}/augmented_images'
create_folder(augmented_path)

categories = os.listdir(original_cropped_images)

for category in categories:
  category_path = f'{original_cropped_images}/{category}'
  print(category_path)
  print(category)
  images = os.listdir(category_path)
  # print(images)

  for image in images:
    image_path = f'{category_path}/{image}'

    # 0.5 default
    low_exp_cutoff = 0.55 # before 0.5 (was not dark enough)
    high_exp_cutoff = 0.38 # before 0.4 (sometimes to light)

    # 1 default, greater than 1 darker
    low_exp_gamma = 1
    high_exp_gamma = 0.8

    # Read image from path
    img = mpimg.imread(image_path)

    lower_exp = exposure.adjust_sigmoid(img, cutoff=low_exp_cutoff)
    # higher_exp = exposure.adjust_sigmoid(img, cutoff=high_exp_cutoff)
    higher_exp = exposure.adjust_gamma(img, gamma=high_exp_gamma)


    flip_y = flip(img, 1)

    flipped_lower_exp = exposure.adjust_sigmoid(flip_y, cutoff=low_exp_cutoff)
    # flipped_higher_exp = exposure.adjust_sigmoid(flip_y, cutoff=high_exp_cutoff)
    flipped_higher_exp = exposure.adjust_gamma(flip_y, gamma=high_exp_gamma)

    
    # Create folder for each version
    create_folder(f'{augmented_path}/{category}')

    # Path for each image
    normal_exp_path = f'{augmented_path}/{category}/normal-exposure-{image}'
    lower_exp_path = f'{augmented_path}/{category}/lower-exposure-{image}'
    higher_exp_path = f'{augmented_path}/{category}/higher-exposure-{image}'


    # Put flipped image into correct folder
    if (category == 'left_ear'):
      print('this is a left ear flipped so put in right ear')
      create_folder(f'{augmented_path}/right_ear')
      flip_y_path = f'{augmented_path}/right_ear/flip-y-{image}'
      flipped_lower_exp_path = f'{augmented_path}/right_ear/flip-y-lower-exposure-{image}'
      flipped_higer_exp_path = f'{augmented_path}/right_ear/flip-y-higer-exposure-{image}'

    elif (category == 'right_ear'):
      print('this is a right ear flipped so put in left ear')
      create_folder(f'{augmented_path}/left_ear')
      flip_y_path = f'{augmented_path}/left_ear/flip-y-{image}'
      flipped_lower_exp_path = f'{augmented_path}/left_ear/flip-y-lower-exposure-{image}'
      flipped_higer_exp_path = f'{augmented_path}/left_ear/flip-y-higer-exposure-{image}'

    elif (category == 'left_hand'):
      print('this is a left hand flipped so put in right hand')
      create_folder(f'{augmented_path}/right_hand')
      flip_y_path = f'{augmented_path}/right_hand/flip-y-{image}'
      flipped_lower_exp_path = f'{augmented_path}/right_hand/flip-y-lower-exposure-{image}'
      flipped_higer_exp_path = f'{augmented_path}/right_hand/flip-y-higer-exposure-{image}'

    elif (category == 'right_hand'):
      print('this is a right hand flipped so put in left hand')
      create_folder(f'{augmented_path}/left_hand')
      flip_y_path = f'{augmented_path}/left_hand/flip-y-{image}'
      flipped_lower_exp_path = f'{augmented_path}/left_hand/flip-y-lower-exposure-{image}'
      flipped_higer_exp_path = f'{augmented_path}/left_hand/flip-y-higer-exposure-{image}'

    else:
      print('no need to move it to another folder')
      flip_y_path = f'{augmented_path}/{category}/flip-y-{image}'
      flipped_lower_exp_path = f'{augmented_path}/{category}/flip-y-lower-exposure-{image}'
      flipped_higer_exp_path = f'{augmented_path}/{category}/flip-y-higer-exposure-{image}'

    mpimg.imsave(normal_exp_path, img)
    mpimg.imsave(lower_exp_path, lower_exp)
    mpimg.imsave(higher_exp_path, higher_exp)
    mpimg.imsave(flip_y_path, flip_y)
    mpimg.imsave(flipped_lower_exp_path, flipped_lower_exp)
    mpimg.imsave(flipped_higer_exp_path, flipped_higher_exp)
    break;


sys.exit("END")