# Movie Recommendation System
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# --------------------------
# Step 1: Movie ratings data
# --------------------------
data = {
    'User': ['Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
    'Movie': ['Inception', 'Titanic', 'Avatar', 'Inception', 'Titanic', 'Avengers', 'Avatar', 'Avengers', 'Titanic'],
    'Rating': [5, 3, 4, 4, 5, 5, 2, 5, 3]
}

df = pd.DataFrame(data)

# --------------------------
# Step 2: Collaborative Filtering (User-User)
# --------------------------
# Create a user-item matrix
user_item_matrix = df.pivot_table(index='User', columns='Movie', values='Rating').fillna(0)

# Compute cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# Function to recommend movies using collaborative filtering
def recommend_movies(user, n_recommendations=2):
    similar_users = user_similarity_df[user].sort_values(ascending=False)[1:]
    recommendations = {}
    
    for other_user, similarity in similar_users.items():
        for movie, rating in user_item_matrix.loc[other_user].items():
            if rating > 0 and user_item_matrix.loc[user, movie] == 0:
                if movie not in recommendations:
                    recommendations[movie] = 0
                recommendations[movie] += similarity * rating
    
    recommended_movies = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
    return [movie for movie, score in recommended_movies]

# --------------------------
# Step 3: Content-Based Filtering
# --------------------------
# Sample movie features
movies = pd.DataFrame({
    'Movie': ['Inception', 'Titanic', 'Avatar', 'Avengers'],
    'Genre': ['Action Sci-Fi', 'Romance Drama', 'Action Sci-Fi', 'Action Adventure']
})

# Convert genres to TF-IDF vectors
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(movies['Genre'])

# Compute similarity between movies
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=movies['Movie'], columns=movies['Movie'])

# Function to recommend movies using content-based filtering
def recommend_similar_movies(movie, n_recommendations=2):
    similar_movies = cosine_sim_df[movie].sort_values(ascending=False)[1:n_recommendations+1]
    return similar_movies.index.tolist()

# --------------------------
# Step 4: Testing the System
# --------------------------
# Collaborative Filtering
print("Collaborative Filtering Recommendations:")
print("For Alice:", recommend_movies('Alice'))
print("For Bob:", recommend_movies('Bob'))
print("For Charlie:", recommend_movies('Charlie'))

# Content-Based Filtering
print("\nContent-Based Filtering Recommendations:")
print("Movies similar to Inception:", recommend_similar_movies('Inception'))
print("Movies similar to Titanic:", recommend_similar_movies('Titanic'))
print("Movies similar to Avatar:", recommend_similar_movies('Avatar'))
