import os
os.makedirs("data", exist_ok=True)

import pandas as pd
import random

jobs = [
    "python machine learning nlp data analysis",
    "java backend spring boot api development",
    "data science pandas numpy visualization",
    "deep learning pytorch tensorflow cnn",
    "frontend html css javascript react"
]

resumes = [
    "python pandas numpy machine learning project",
    "java spring boot backend api development",
    "excel data analysis communication skills",
    "deep learning cnn pytorch model training",
    "html css javascript frontend developer"
]

data = []

for _ in range(50):
    jd = random.choice(jobs)
    res = random.choice(resumes)

    label = 1 if any(word in res for word in jd.split()) else 0

    data.append([jd, res, label])

df = pd.DataFrame(data, columns=["job_description", "resume", "label"])
df.to_csv("data/train.csv", index=False)

print("Dataset created")