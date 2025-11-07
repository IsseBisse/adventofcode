import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

from JurrasicJigsaw import JigsawPiece

a = np.zeros((100, 200))
x = 35
y = 127

sea_monster_pattern = JigsawPiece.string_to_matrix(open("seaMonster.txt").read().split("\n"))

a[x-1:x+2, y-10:y+10] = sea_monster_pattern
match = sig.correlate2d(a, sea_monster_pattern, mode="same")

plt.subplot(221)
plt.imshow(a)

plt.subplot(222)
plt.imshow(match)

print(match.max())
index = np.where(match == np.sum(sea_monster_pattern))
print(index)

plt.show()