<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
<!--   <a href="">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

  <h3 align="center">Lego Project</h3>

  <p align="center">
    Using machine learning to categorize images of lego pieces
  </p>
</div>

## Overview
This project contains several components:
1. A data collection script that downloads 3D models of lego pieces from the MecaBricks website
2. A synthetic image generation script that creates images of the 3D models from different angles and lighting conditions
3. A machine learning model that categorizes the images into different lego piece types

### Example Images
<!-- Grid of images where row is a sub_directory of output, and col is an index -->
| Part | Image 1 | Image 2 | Image 3 | Image 4 | Image 5 |
|------|---------|---------|---------|---------|---------|
| 1x1 Plate | ![1x1 Plate 1](<output/Plate 1x1 (3024)/[0].png>) | ![1x1 Plate 2](<output/Plate 1x1 (3024)/[1].png>) | ![1x1 Plate 3](<output/Plate 1x1 (3024)/[2].png>) | ![1x1 Plate 4](<output/Plate 1x1 (3024)/[3].png>) | ![1x1 Plate 5](<output/Plate 1x1 (3024)/[4].png>) |
| 1x2 Plate | ![1x2 Plate 1](<output/Plate 1x2 (3023)/[0].png>) | ![1x2 Plate 2](<output/Plate 1x2 (3023)/[1].png>) | ![1x2 Plate 3](<output/Plate 1x2 (3023)/[2].png>) | ![1x2 Plate 4](<output/Plate 1x2 (3023)/[3].png>) | ![1x2 Plate 5](<output/Plate 1x2 (3023)/[4].png>) |
| 2x2 Plate | ![2x2 Plate 1](<output/Plate 2 x 2 (3022)/[0].png>) | ![2x2 Plate 2](<output/Plate 2 x 2 (3022)/[1].png>) | ![2x2 Plate 3](<output/Plate 2 x 2 (3022)/[2].png>) | ![2x2 Plate 4](<output/Plate 2 x 2 (3022)/[3].png>) | ![2x2 Plate 5](<output/Plate 2 x 2 (3022)/[4].png>) |
| 2x4 Plate | ![2x4 Plate 1](<output/Plate 2 x 4 (3020)/[0].png>) | ![2x4 Plate 2](<output/Plate 2 x 4 (3020)/[1].png>) | ![2x4 Plate 3](<output/Plate 2 x 4 (3020)/[2].png>) | ![2x4 Plate 4](<output/Plate 2 x 4 (3020)/[3].png>) | ![2x4 Plate 5](<output/Plate 2 x 4 (3020)/[4].png>) |


## Prerequisites
* Python 3.6+
* Blender 2.8+
* Jupyter Notebook
* Dependencies: `pip install -r requirements.txt`

## Data Collection
To collect the data, simply run the `create_objs.ipynb` notebook. This will download the 3D models of the lego pieces from the MecaBricks website as json, convert them to obj files, and save them in the `parts_obj` directory.

## Synthetic Image Generation
To generate synthetic images, open Blender and run the `RandomView.py` script. This will load the obj files from the `parts_obj` directory, render images of the 3D models from different angles and lighting conditions, and save them in the `output` directory.

## Training
TODO

## Acknowledgments
* [MecaBricks](https://www.mecabricks.com/en)
* [Blender](https://www.blender.org/)
* Background images from random public domain sources and gen AI

