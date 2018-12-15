# numpy-html
A simple table renderer for numpy arrays. Provides a rich display hook for use with Jupyter Lab / Notebok.

## Installation
`pip install git+https://github.com/agoose77/numpy-html.git#egg=numpy-html`

## Example inside Jupyter
```python
import numpy as np
np.set_printoptions(threshold=5, edgeitems=2)
np.arange(49).reshape(7, 7)
```
<table style='border-style:solid;border-width:1px;'>
<tr>
<td style='font-family:monospace;white-space: pre;' title='(0, 0)'>0 </td>
<td style='font-family:monospace;white-space: pre;' title='(0, 1)'>1 </td>
<td><center>⋯</center></td>
<td style='font-family:monospace;white-space: pre;' title='(0, 5)'>5 </td>
<td style='font-family:monospace;white-space: pre;' title='(0, 6)'>6 </td>
</tr>
<tr>
<td style='font-family:monospace;white-space: pre;' title='(1, 0)'>7 </td>
<td style='font-family:monospace;white-space: pre;' title='(1, 1)'>8 </td>
<td><center>⋯</center></td>
<td style='font-family:monospace;white-space: pre;' title='(1, 5)'>12</td>
<td style='font-family:monospace;white-space: pre;' title='(1, 6)'>13</td>
</tr>
<tr>
<td><center>⋮</center></td>
<td><center>⋮</center></td>
<td><center>⋱</center></td>
<td><center>⋮</center></td>
<td><center>⋮</center></td>
</tr>
<tr>
<td style='font-family:monospace;white-space: pre;' title='(5, 0)'>35</td>
<td style='font-family:monospace;white-space: pre;' title='(5, 1)'>36</td>
<td><center>⋯</center></td>
<td style='font-family:monospace;white-space: pre;' title='(5, 5)'>40</td>
<td style='font-family:monospace;white-space: pre;' title='(5, 6)'>41</td>
</tr>
<tr>
<td style='font-family:monospace;white-space: pre;' title='(6, 0)'>42</td>
<td style='font-family:monospace;white-space: pre;' title='(6, 1)'>43</td>
<td><center>⋯</center></td>
<td style='font-family:monospace;white-space: pre;' title='(6, 5)'>47</td>
<td style='font-family:monospace;white-space: pre;' title='(6, 6)'>48</td>
</tr>
</table>
