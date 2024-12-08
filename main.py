from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

# Mapping of category_id to category names
cat_to_id = {
    "2": "Vible",
    "4": "E/ACC",
    "3": "The Igloo",
    "20": "OvaDrive",
    "22": "SolTok",
    "25": "Super Feed",
    "5": "Gratitube",
    "8": "Bloom Scroll",
    "18": "Startup College",
    "21": "Pumptok",
    "6": "InstaRama",
    "13": "Flic",
}

# Function to recommend posts

def Recommend(username, category_id=None, moods=None):
    # Load data
    final_df = pd.read_csv("./CONTENT_based_filtering.csv")
    final_df=final_df.drop(columns=['Unnamed: 0'],axis=1)
    similarity = np.load("./similarity_matrix.npy")
    # Preprocess the `category` column to remove brackets and quotes
    final_df['category'] = final_df['category'].str.strip("[]").str.replace("'", "")
    
    # Map category_id to category name (assuming you have a mapping function for this)
    category_name = cat_to_id.get(category_id)

    # Fetch the posts viewed by the user
    user_views = final_df[final_df["username"] == username]

    if user_views.empty:
        return []  # Return empty list if the user has no viewed posts
    
    recommended_posts = []  # Initialize an empty list to store recommendations

    # Iterate through the titles the user has viewed
    for title in user_views["title"]:
        # Get the index of the title in final_df
        title_index = final_df[final_df["title"] == title].index[0]

        # Get similarity distances for the current title
        distances = similarity[title_index]
        
        # Find the top 5 most similar posts (excluding the current post itself)
        title_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

        for idx, _ in title_list:
            recommended_post = final_df.iloc[idx]
            recommended_posts.append(recommended_post)

    # Convert to DataFrame for further filtering
    recommended_df = pd.DataFrame(recommended_posts).drop_duplicates()

    # Filter by category if `category_id` is provided
    if category_name:
        recommended_df = recommended_df[recommended_df['category'] == category_name]

    # Filter by moods if provided
    if moods:
        if isinstance(moods, str):
            moods = [moods]  # Ensure moods is a list
        
        # Filter the recommended posts where any mood in the 'mood' column matches the provided moods
        recommended_df = recommended_df[recommended_df['moods'].apply(lambda x: any(mood in x for mood in moods))]

    # Optionally, sort by 'rating_percent' if available
    if 'rating_percent' in recommended_df.columns:
        recommended_df = recommended_df.sort_values(ascending=False, by='rating_percent')

    # Remove duplicates based on 'title' column to avoid recommending the same post multiple times
    recommended_df = recommended_df.drop_duplicates(subset='title')

    # Return top 10 recommendations
    return recommended_df.head(10).to_dict('records')

# Route for username and category_id filtering
@app.route("/feed", methods=["GET"])
def feed():
    username = request.args.get("username")
    category_id = request.args.get("category_id")
    
    if not username:
        return jsonify({"error": "username is required"}), 400

    # Trim whitespace from username
    username = username.strip()
    
    # Fetch recommendations
    try:
        posts = Recommend(username=username, category_id=category_id)
        return jsonify({"username": username, "recommended_posts": posts})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)