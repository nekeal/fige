# Fige



# Generating test data

```python
from fige.generators import *
size = np.array([100, 100])
square_gen = SquareGenerator(size)
circle_gen = CircleGenerator(size)
triangle_gen = TriangleGenerator(size)

square_gen.run(1000)
circle_gen.run(1000)
triangle_gen.run(1000)
```
