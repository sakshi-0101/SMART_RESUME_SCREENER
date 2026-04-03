import re

import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

bert_model=SentenceTransformer("all-MiniLM-L6-v2")

def clean_text(text):
    text=text.lower()
    text=re.sub(r'[^a-zA-Z]',' ',text)
    return text

def extract_text(file):
    pdf_reader=PyPDF2.PdfReader(file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text() or ""
    return text

def tfidf_similarity(job_desc,resumes):
    docs=[job_desc]+resumes
    tfidf=TfidfVectorizer(stop_words='english')
    matrix=tfidf.fit_transform(docs)
    scores=cosine_similarity(matrix[0:1],matrix[1:]).flatten()
    return scores

def bert_similarity(job_desc,resumes):
    job_emb=bert_model.encode([job_desc])
    resume_emb=bert_model.encode(resumes)
    
    scores=cosine_similarity(job_emb,resume_emb).flatten()
    return scores

def get_final_scores(job_desc,resumes):
    tfidf_scores=tfidf_similarity(job_desc,resumes)
    bert_scores=bert_similarity(job_desc,resumes)
    
    final_scores=(0.4*tfidf_scores)+(0.6*bert_scores)
    
    return [round(score*100,2) for score in final_scores]

def get_all_scores(job_desc, resumes):
    tfidf_scores = tfidf_similarity(job_desc, resumes)
    bert_scores = bert_similarity(job_desc, resumes)

    final_scores = (0.4 * tfidf_scores) + (0.6 * bert_scores)

    return tfidf_scores, bert_scores, final_scores