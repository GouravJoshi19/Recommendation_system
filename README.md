
# Recommendation System for Personalized Post Recommendations

## Project Overview
This project implements a recommendation system to suggest personalized posts to users based on their interactions, preferences (category), and moods. The system uses a combination of content-based filtering, collaborative filtering, and emotion-based cold-start techniques to generate recommendations.

The system is built using the Flask web framework and provides 3 API endpoints for personalized recommendations based on the following parameters:
1. **Username**
2. **Category**
3. **Mood**

The API returns the top 10 posts recommended for the user based on the specified input.

## Approach & Model Architecture

The recommendation system is based on three main approaches:

### 1. **Content-Based Filtering**:
   - **Cosine Similarity**: This approach relies on calculating the similarity between posts based on their content features such as the title, category, and mood. Posts that are similar in content are recommended to the user.
   - **Steps**:
     - Extract features from the dataset such as the `category`, `mood`, and other relevant content information.
     - Calculate the cosine similarity between posts to identify which posts are most similar to a given post.
     - Recommend the top 10 posts based on their similarity to the posts a user has already interacted with.

### 2. **Collaborative Filtering**:
   - This approach generates recommendations based on the interactions of users. It assumes that if two users have similar tastes, they will enjoy similar content.
   - **Steps**:
     - User-item interaction matrix is created to capture the relationship between users and posts.
     - Collaborative filtering is performed to predict which posts a user might like based on the preferences of similar users.

### 3. **Cold-Start Problem (Emotion-based)**:
   - **Problem**: In the cold-start scenario (when a user has no interaction history), traditional recommendation models (content-based or collaborative) cannot generate recommendations.
   - **Solution**: Use the **emotions** extracted from the `post_summary` column to recommend posts based on mood.
     - **Emotion extraction**: Extract the emotions (such as Awe, Reverence, Strength, Benevolence) from the `post_summary` to understand the tone of the post.
     - **Steps**: Use the extracted emotions to match posts that align with the user's current mood, and recommend those posts.

### Key Decisions Made During Development:
- **Cosine Similarity**: Used for content-based filtering as it effectively measures the similarity between text-based data such as post titles and descriptions.
- **Emotion Extraction**: For cold-start problems, I extracted emotions from the `post_summary` column and used them to suggest posts based on the user’s current mood. This is a key feature for users with limited historical interactions.
- **Flask API**: Flask was chosen for implementing the API due to its lightweight nature and ease of integration with machine learning models.
- **Data Preprocessing**: A significant part of the project involved cleaning and understanding real-time data, such as interactions and emotions, which was a challenge for me as a beginner.

## Challenges Faced
- As a beginner, working with real-time data was challenging. Understanding the data, especially the interactions between users and posts, required significant effort. Moreover, learning how to handle large datasets and extract meaningful features (like emotions) from the `post_summary` column was difficult but rewarding.
- The cold-start problem was tricky to address, especially when trying to extract emotion-based features from the dataset, which required a deeper understanding of natural language processing and feature extraction techniques.

## API Endpoints

The system provides the following 3 API endpoints:

### 1. **Get Recommended Posts by Username, Category, and Mood**:
   - **Endpoint**: `/feed?username=your_username&category_id=category_id_user_want_to_see&mood=user_current_mood`
   - **Description**: This endpoint returns 10 posts recommended for the user based on the `username`, `category_id`, and `mood`.
   - **Parameters**:
     - `username`: The unique identifier of the user (e.g., 'user1').
     - `category_id`: The category the user is interested in (e.g., 'Technology').
     - `mood`: The current mood of the user (e.g., 'Awe', 'Reverence').
   
   **Example Request**:
   ```
   GET http://localhost:5000/feed?username=user1&category_id=Technology&mood=Awe
   ```
   
### 2. **Get Recommended Posts by Username and Category**:
   - **Endpoint**: `/feed?username=your_username&category_id=category_id_user_want_to_see`
   - **Description**: This endpoint returns 10 posts recommended for the user based on the `username` and `category_id`. It does not consider the user's mood.
   - **Parameters**:
     - `username`: The unique identifier of the user (e.g., 'user1').
     - `category_id`: The category the user is interested in (e.g., 'Philosophy').
   
   **Example Request**:
   ```
   GET http://localhost:5000/feed?username=user1&category_id=Philosophy
   ```

### 3. **Get Recommended Posts by Username Only**:
   - **Endpoint**: `/feed?username=your_username`
   - **Description**: This endpoint returns 10 posts recommended for the user based on the `username` alone. It will use the user's previous interactions (if available) to recommend posts.
   - **Parameters**:
     - `username`: The unique identifier of the user (e.g., 'user1').
   
   **Example Request**:
   ```
   GET http://localhost:5000/feed?username=user1
   ```

### Response Format:
Each API call will return a JSON response with the following structure:

```json
{
    "recommended_posts": [
        {
            "title": "Post 1",
            "category": "Philosophy",
            "mood": "Awe",
            "rating_percent": 85
        },
        {
            "title": "Post 2",
            "category": "Technology",
            "mood": "Reverence",
            "rating_percent": 90
        },
        ...
    ]
}
```

## Setup and Installation Instructions

### 1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/recommendation-system.git
   cd recommendation-system
   ```

### 2. **Install Dependencies**:
   - Make sure you have Python 3 installed.
   - Install required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Run the Flask API**:
   - To start the Flask API, run the following command:
   ```bash
   python main.py
   ```
   - The server will start on `http://localhost:5000`.

### 4. **Test the API**:
   - Use a tool like **Postman** or **cURL** to send GET requests to the API endpoints.

### 5. **CSV Dataset**:
   - The CSV file (`synthetic_posts.csv`) used for generating recommendations should be placed in the project directory.

## Future Improvements
- **Improved Cold-Start Solutions**: Implement more sophisticated cold-start techniques such as hybrid recommendation models or incorporating external data (e.g., user profiles or item metadata).
- **Scalability**: Enhance the system's scalability to handle larger datasets and more users, possibly by integrating with cloud-based services.
- **User Feedback Loop**: Implement a feedback system where users can rate the recommended posts, and the model can be updated with their preferences.
