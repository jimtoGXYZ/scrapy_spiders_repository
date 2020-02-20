import pandas as pd

s = pd.Series(['lama', 'cow', 'lama', 'beetle', 'lama', 'hippo'],
              name='animal')

print(s)
print(s.drop_duplicates())
