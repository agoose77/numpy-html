# numpy-html
A simple table renderer for numpy arrays. Provides a rich display hook for use with Jupyter Lab / Notebook. Inspired by [xtensor](https://github.com/QuantStack/xtensor).

## Installation
`pip install numpy-html`

## Example inside Jupyter
```python
import numpy_html
import numpy as np

np.set_printoptions(threshold=5, edgeitems=2)
np.arange(49).reshape(7, 7)
```
|  0 	|  1 	| ⋯ 	|  5 	|  6 	|
|:--:	|:--:	|:-:	|:--:	|:--:	|
|  7 	|  8 	| ⋯ 	| 12 	| 13 	|
|  ⋮ 	|  ⋮ 	| ⋱ 	|  ⋮ 	|  ⋮ 	|
| 35 	| 36 	| ⋯ 	| 40 	| 41 	|
| 42 	| 43 	| ⋯ 	| 47 	| 48 	|
