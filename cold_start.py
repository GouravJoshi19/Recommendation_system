from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

def Recommend_mood(moods):
    try:
        complete_df = pd.read_csv("./completed_data_for_cold_start.csv")
        
        # Ensure moods is a list
        if isinstance(moods, str):
            moods = moods.split(',')  # If moods are passed as a comma-separated string, split them
        
        # Filter the DataFrame for rows where any mood in the 'moods' column matches one of the provided moods
        filtered_df = complete_df[complete_df['mood'].apply(lambda x: any(mood in x for mood in moods))]

        # Optionally, sort by 'rating_percent' if available
        recommendations = filtered_df.sort_values(ascending=False, by='rating_percent')

        # Remove duplicates based on 'title' column to avoid recommending the same post multiple times
        recommendations = recommendations.drop_duplicates(subset='title')

        return recommendations

    except Exception as e:
        raise Exception(f"Error during recommendation process: {str(e)}")


@app.route("/coldstart", methods=["GET"])
def feed():
    moods = request.args.get('mood')
    if not moods:
        return jsonify({"error": "Mood is required"}), 400
    
    # Fetch recommendations
    try:
        # Fetch recommendations as a DataFrame
        posts = Recommend_mood(moods)

        # Convert the DataFrame to a list of dictionaries for JSON response
        posts_dict = posts.to_dict('records')

        return jsonify({"recommended_posts": posts_dict})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
