import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from typing import List

df = pd.read_csv('/app/Final_cleaned_dataset.csv')

df2 = pd.get_dummies(df, columns = ['brand'])
#df3 = df2.copy()

def calculate_similarity(product_attributes, all_attributes):
    scaler = StandardScaler()
    all_attributes_scaled = scaler.fit_transform(all_attributes)
    product_attributes_scaled = scaler.transform(product_attributes.reshape(1, -1))
    similarity_scores = cosine_similarity(product_attributes_scaled, all_attributes_scaled).flatten()
    return similarity_scores


def find_similar_products(product_id: str, num_similar: int) -> List[str]:
    product = df2[df2['uniq_id'] == product_id].iloc[0]
    product_attributes = product.drop(labels = ['uniq_id']).values
    all_attributes = df2.drop(columns = ['uniq_id']).values
    similarity_score = calculate_similarity(product_attributes, all_attributes)
    similarity_df = pd.DataFrame({
        'uniq_id': df2['uniq_id'],
        'similarity_score': similarity_score,
        'rating': df2['rating']
    })
    similarity_df = similarity_df.sort_values(by=['similarity_score', 'rating'], ascending=[False, False])
    similarity_df = similarity_df[similarity_df['uniq_id'] != product_id]
    similar_product_ids = similarity_df.head(num_similar)['uniq_id'].tolist()
    
    return similar_product_ids


#df2[df2['uniq_id'] == '36c9db800b40d1e00df701009a685d3d']


#prod_id = '1b8a7af720c99e818ef8dd9e33be44de'
#num_similar = 7
#similar_prods = find_similar_products(prod_id, num_similar)
#print(similar_prods)