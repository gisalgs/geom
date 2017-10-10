# Code for geometric algorithms

This is no formal installation for this package (or any packages in `gisalgs`). However, installing the code is not complicated. It is important to organize everything in a directory and each package such as `geom` is a subdirectory. Now suppose we use the directory at the root called `/lib` to store everything and we create a subfolder called `gisalgs` there. Under the `/lib/gisalgs` directory, create a subdirectory called `geom` and save all the files in this repository in geom. It will be essential to have the `__init__.py` in geom (this is just an empty file with the specific file name). Lastly, make sure to copy `__init__.py` to the parent directory (in this case, `/lib/gisalgs`).

The following is an example of using modules in this repository:

```python
import sys
sys.path.append('/lib/gisalgs')

from geom.point import *

p, p1, p2 = Point(10,0), Point(0,100), Point(0,1)
print(p.distance(p1))
print(p1)
```
