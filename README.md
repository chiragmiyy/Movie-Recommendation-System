# 🎬 Movie Recommendation System

This is a **Content-Based Movie Recommendation System** built using Python. It recommends similar movies based on user input by analyzing features such as genres, keywords, cast, and crew. 

## 🚀 Features

- Recommends top 10 similar movies based on content
- Utilizes **TMDB 5000 Movie Dataset**
- Fetches **movie posters** via **TMDB API**
- Feature engineering using **text data (overview, genres, keywords, etc.)**
- Natural Language Processing (NLP) with **Text Vectorization** and **Cosine Similarity**

---

## 📁 Dataset

The project uses the **TMDB 5000 Movie Dataset** which consists of:
- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- NLTK (optional, for stemming)
- Jupyter Notebook (for development and demo)

---

## 📊 How It Works

1. **Data Cleaning**: Merge `movies` and `credits` datasets, remove duplicates/nulls.
2. **Feature Extraction**: Extract `genres`, `keywords`, `cast`, `crew`, `overview`.
3. **Preprocessing**: Tokenize, lowercase, remove spaces, and apply stemming.
4. **Vectorization**: Convert text to numeric using **CountVectorizer**.
5. **Similarity Calculation**: Compute **cosine similarity** between movie vectors.
6. **Recommendation**: Return top 5 movies closest to the input movie.

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Install dependencies

pip install -r requirements.txt

### 3. Run the Jupyter Notebook

jupyter notebook

Open movie_recommender.ipynb and run the cells step-by-step.

## 📂 Folder Structure

<pre> ``` movie-recommendation-system/ 
├── tmdb_5000_movies.csv 
├── tmdb_5000_credits.csv 
├── movie_recommender.ipynb 
├── README.md 
└── requirements.txt ``` </pre>