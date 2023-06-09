#!/bin/sh
#BSUB -J torch_gpu
#BSUB -o test_bin_rgb_%J.out
#BSUB -e test_bin_rgb_%J.err
#BSUB -n 2
#BSUB -q gpuv100
#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -R "rusage[mem=32G]"
#BSUB -R "span[hosts=1]"
#BSUB -W 10
# end of BSUB options

# load a scipy module
# replace VERSION and uncomment
module load matplotlib/3.4.2-numpy-1.21.1-python-3.9.6
module load scipy/1.6.3-python-3.9.6
module load pandas/1.3.1-python-3.9.6
# load CUDA (for GPU support)
module load cuda/11.0

# activate the virtual environment
# NOTE: needs to have been built with the same SciPy version above!
source /work3/coer/Bachelor/yolov5/instance-segm-yolo/bin/activate

python segment/val.py --weights /work3/coer/Bachelor/yolov5/runs/train-seg/exp150/weights/best.pt --data grainSpectral.yaml --img 256 --task "test"

#python segment/val.py --weights /work3/coer/Bachelor/yolov5/runs/train-seg/exp141/weights/best.pt --data grain256_april_binary.yaml --img 256 --task "test" # validate

#python segment/val.py --weights yolov5s-seg.pt --data grain.yaml --img 640 --name coco


