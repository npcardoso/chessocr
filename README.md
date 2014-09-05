# chessocr

A OCR application for chess boards

The goal of this application is to read an image, detect the chess boards in it and
export them using the FEN notation (https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation).

## Setting stuff up

```
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python src/main.py <filename>
```

## Roadmap

### Done

#### Board Detection
- Read Image from file

![Original Image](./images/orig.png)

- Convert image to grayscale.

![Grayscale Image](./images/gray.png)

- Convert to black and white taking into account average image brightness.

![BW Image](./images/bw.png)

- Find contours using cv2.findContours

![Contours Image](./images/contours.png)

- Filter irrelevant contours:
  - Area either too small or too large.
  - Ratio height/width not close to 1.

![Contours Image](./images/contours_filtered.png)

#### Board Extraction/Perspective Correction
- Draw each contour in an individual black buffer.

![Contours bw Image](./images/contour_individual_bw.png)

- Find lines by using the standard Hough transform. This is done,
  iteratively, progressively decreasing the accumulator threshold
  parameter until there exactly 2 horizontal lines and 2 vertical
  lines (with some degree of freedom).
  - Lines that are too close to each other are ignored

![Contour Lines](./images/contour_lines_bw.png)
![Contour Lines](./images/contour_lines_orig.png)

- Calculate the perspective correction transformation using the 4 points of intersection.

![Perspective Points](./images/perspective.png)

- Apply the transformation to a copy of the original image and crop it to size.

![Extracted Board](./images/extracted.png)

### Doing

#### Grid Detection/Tile extraction
  - Using OpenCV to detect grids

  - Using Canny algorithm for edge detection
    ![Canny Edge Image](./images/canny.png)

  - Find lines by using the standard Hough transform. This is done, iteratively, progressively decreasing the accumulator threshold parameter until there are at least 8 horizontal lines and 8 vertical lines. Lines that are too close to each other are ignored

    ![Hough Lines Image 1](./images/hough1.png)

    ![Hough Lines Image 2](./images/hough2.png)

  - Calculate the line intersections

    ![Detected Grid](./images/grid.png)

### To Do

#### Piece Detection

#### Rule-based Board Validation/Self-Correction
