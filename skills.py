import re

SKILLS=[
    "python","java","c++","machine learning","deep learning",
    "nlp","data science","tensorflow","pytorch","sql",
    "excel","communication","flask","streamlit"
]

def extract_skills(text):
    text=text.lower()
    found=[]
    
    for skill in SKILLS:
        if re.search(rf"\b{skill}\b",text):
            found.append(skill)
            
    return list(set(found))
        