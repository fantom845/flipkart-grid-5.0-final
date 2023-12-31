import streamlit as st
import pandas as pd
import random
from sklearn.metrics.pairwise import euclidean_distances



data = pd.read_csv("fashion_products.csv")

# Create interaction matrix and find similarity
interaction_matrix = data.pivot_table(index='User ID', columns='Product ID', values='Rating', fill_value=0)
product_similarity = euclidean_distances(interaction_matrix.T)

# Function to get product recommendations based on product name and category
def get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity, num_recommendations=50):
    user_interactions = interaction_matrix.loc[user_id].values
    similar_scores = product_similarity.dot(user_interactions)
    recommended_indices = similar_scores.argsort()[-num_recommendations:][::-1]
    recommended_products = interaction_matrix.columns[recommended_indices]
    
    # Filter recommended products by product name and category
    filtered_products = filter_by_product_name_and_category(recommended_products, product_name, category)
    
    return filtered_products

# Function to filter recommended products by product name and category
def filter_by_product_name_and_category(products, product_name, category):
    
    filtered_products=[]
    if product_name in ['T-shirt', 'Jeans']:
         tshirt_recommendations = data[
             (data['Product Name'] == 'T-shirt') &
             (data['Category'] == category)
         ].head(num_recommendations/2)
        
         jeans_recommendations = data[
             (data['Product Name'] == 'Jeans') &
             (data['Category'] == category)  
         ].head(num_recommendations/2)
        
         filtered_products = pd.concat([tshirt_recommendations, jeans_recommendations])
  
    else:
         filtered_products = data[
             (data['Product Name'] == product_name) &
             (data['Category'] == category)
            
         ]
    
    return filtered_products



# Function to generate the UI
def generate_ui():
    
    st.set_page_config(
        page_title="Fashion Product Recommender",
        page_icon="⚙️",
        layout="wide",
        menu_items={
             'Get Help': 'https://www.extremelycoolapp.com/help',
             'Report a bug': "https://www.extremelycoolapp.com/bug",
             'About': "# This is the *Best* reccomender system out there!"
        }
        
        
    )
    
    
    st.title("Fashion Product Recommender")
    st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cGljfGVufDB8fDB8fHww&w=1000&q=80");
    }
   </style>
    """,
    unsafe_allow_html=True
    )
    [theme]
    backgroundColor = "#F0F0F0"
    st.markdown("Discover personalized fashion product recommendations.")

    # User input
    user_id = st.number_input("Enter User ID", min_value=1, max_value=1000, value=1, help="Enter your user ID.")
    product_name = st.selectbox("Select Product Name", data['Product Name'].unique(), help="Select a product name.")
    category = st.selectbox("Select Category", data['Category'].unique(), help="Select a category.")
   
    # Recommendation button
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(user_id, product_name, category, interaction_matrix, product_similarity)
        
        if len(recommendations) > 10:
            random_recommendations = random.sample(list(recommendations['Product ID']), 10)
        else:
            random_recommendations = list(recommendations['Product ID'])
        
        # Display recommended products
        st.subheader("Recommended Products:")
        recommended_products_info = data[data['Product ID'].isin(random_recommendations)][['Product ID', 'Product Name', 'Category', 'Brand', 'Color']]
        st.table(recommended_products_info)
        
        # Display user's history
        st.subheader("User History:")
        user_products_info = data[data['User ID'] == user_id][['Product Name', 'Category', 'Brand', 'Color']].drop_duplicates()
        st.table(user_products_info)



# Main function
if __name__ == "__main__":
    generate_ui()
