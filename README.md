# similarity-service-application
# Step 1: Data Cleaning
The dataset given for this take home assignment initially contained several columns that were not required to calculate similarity between products. The features that I needed to used to calculate similarity were (brand, sales_price, weight, rating). Initially, there were 2890, 8143 and 23746 null values in the sales_price, brand and weight columns respectively. Since one of the assumptions was that a given unique_id would exist in the dataset, I couldn't just drop the nul values from the dataset. I did a couple of different thing in order to handle the null values and populate the dataset in the best possible manner from what I was given. First, for the brand column I populated the null values by using the product_name and product_url columns in order to find brands names for each null value. I did this by recognizing a pattern between both the columns where the first couple of words in the product_name and product_url columns were always the brand name. I was able to get the brand name from this pattern by first creating a dictionary where the key was the first word common between product_name and product_url and the value for each key was a list of all the product names for that specific key since some brands have multiple items. After doing that I then ran a longest common substring algorithm between every item of the list for each specific key where the first word in the lcs has to be equal to the key value. That way I was able to get all the brand names than had multiple words in their name and I stored this in another dictionary where the key was the key from the previous dictionary and the value was the lcs. Once I was able to extract the brand names correctly I updated the null values in the rand column with the subsequest right value by comparing the unique_id.

Next, I had to find a way to handle null values in sales_price and the weight column. I could not just fill in the null values with the mean or median of the column since that would compromise the integrity of my dataset and the corresponding similarity score that would be created would be completely wrong. So in order to handle null values in these columns better I went with the approach of KMeans clustering where I created clusters based on the rating and product_name column since both the columns were completely populated and both the columns are reasonable parameters to use for clustering. To create the clustering using the product_name column I had to first convert the words in each of the rows into vectors using TfidfVectorizer. After doing that I created clusters using k = 5 as my parameter. I got this value of k by plotting an elbow plot for value of k VS WCSS where 5 was my elbow point. After creating the clusters I filled in the null values in the sales_price and weight column by taking the mean of whichever cluster the null values fell in and assigning the respective null values accordingly.

After doing this my dataset was now completely cleaned up for all the features I was going to use to calculate the similarity score on and now all I had to do was save this cleaned dataset into another csv file.

# Step 2: Model Building
Now, for the actual model building part it was fairly straightforward. All I had to do before feeding in the values into the cosine similarity function to calculate the score was scale the data using Standard Scaler and one hot encode all the unique values in the brand column. After that I got the similarity score I stored all the scores for each of the products compared to the given unique_id in a new similarity_score data frame which contained 'unique_id', 'similarity_score' and 'rating' as its columns. Next, to get only get num_similar number of items from the top of the data frame was also fairld straightforward and I stored all these unique_ids in my output list which would in turn be returned. In case of a tie between similarity scores, I used rating as my tie-breaker metric which is why I stroed rating as well in my similarity_score data frame.

# Step 3: APIs
After cleaning my dataset and making my model I now needed to create an API that would make a GET request to my model and get the list of similar product ids. I used FAST API for that as per the requirements and I also implemented error handling for various different HTTP error codes that the application could potentially run into.

# Step 4: Dockerization
After completeing all the requirements of the project so far the next step was to create a docker image that can be deployable on kubernetes. The process for this consisted of creating the Docker file with the right specifications, creating a requirements.txt file of the libraries used in the appliaction and finally using the Docker client to create an image of the application. After creating the docker image I tested it by running the image locally on my device and it worked as intended. After making the image, I went ahead and deployed the image to Docker hub in order for it to be accessible to anyone that wished to access it. The url for the docker image on Docker Hub is https://hub.docker.com/r/arvindveerelli/similarity-service-application/tags.

# Step 5: Deploying using K8s
The next step was deployment using minikube to my local K8 cluster. This required creating a deployment.yaml and service.yaml files that were required for the pod in order to access the docker image correctly. I was able to successfully deploy my docker image to my local pod on my local minikube cluster with the pod running normally.

# Step 6: Optimisation and what can be improved
