import praw
import spacy
import pandas as pd
import numpy as np
from scipy import spatial
from tqdm import trange, tqdm

nlp = spacy.load('en_core_web_lg')

client_id = "your client id"
client_secret = "your client secret"
user_agent = "your user agent"

def setup():

    '''
    function that sets up the top reddit submissions in a catalog (pandas dataframe).
    returns DataFrame catalog.
    '''

    reddit = praw.Reddit(client_id=client_id,
                        client_secret=client_secret,
                        user_agent=user_agent)

    submission_list = [submission for submission in reddit.subreddit('RoomPorn').hot(limit=1000) if submission.num_comments > 20]
    submission_list.extend([submission for submission in reddit.subreddit('AmateurRoomPorn').hot(limit=1000) if submission.num_comments > 20])
    submission_list.extend([submission for submission in reddit.subreddit('malelivingspace').hot(limit=1000) if submission.num_comments > 20])
    submission_list.extend([submission for submission in reddit.subreddit('CozyPlaces').hot(limit=1000) if submission.num_comments > 20])

    with tqdm(total=len(submission_list), desc="comment") as pbar:
        for submission in submission_list:
            submission.comments.replace_more(limit=0)
            pbar.update(1)
            
    def get_hotwords(words):
        
        doc = nlp(words)

        return [token for token in doc if token.pos_ in ["PROPN", "NOUN", "ADJ"]]

    catalog = pd.DataFrame(columns=["image","title","comments","vector"])

    def calculate_vector(title, comments):
        
        title_vectors = []
        comment_vectors = []
        mean_title_vector = np.zeros(300,)
        mean_comment_vector = np.zeros(300,)
        comments_len = 0

        for comment in comments:
            for word in comment:
                comments_len += 1

        for hotword in title:
            title_vectors.append(hotword.vector)

        for comment in comments:
            for hotword in comment:
                comment_vectors.append(hotword.vector)

        for vector in title_vectors:
            mean_title_vector += vector
        
        mean_title_vector = mean_title_vector / len(title_vectors)

        for vector in comment_vectors:
            mean_comment_vector += vector
        
        mean_comment_vector = mean_comment_vector / comments_len


        return (2*mean_title_vector + mean_comment_vector) / 3

    # Function that appends a new row to the catalog from a submission

    def append_row(catalog, submission):
        image = submission.url
        title = get_hotwords(submission.title)
        comments = [comment.body for comment in submission.comments.list()]
        comments = [get_hotwords(comment) for comment in comments]
        vector = calculate_vector(title, comments)

        catalog = catalog.append({"image":image, "title":title, "comments":comments, "vector":vector}, ignore_index=True)

        return catalog

    with tqdm(total=len(submission_list), desc="comment") as pbar:
        for i in range(len(submission_list)):
            catalog = append_row(catalog, submission_list[i])
            pbar.update(1)

    return catalog

def get_url_list(catalog, hotwords):

    def get_cosine_similarity(sentvec_1, sentvec_2):
        
        '''
        Takes two vectors
        Returns the cosine similarity of two given vectors normalized into a number between 0 and 1
        '''
        
        return  round((2 - spatial.distance.cosine(sentvec_1, sentvec_2)) / 2, 4)
        
    search_vector = nlp(hotwords).vector

    similarity = []

    for i in range(len(catalog)):
        similarity.append(get_cosine_similarity(search_vector, catalog["vector"][i]))

    catalog["similarity"] = similarity
    catalog = catalog[catalog.image.str.contains(".jpg") | catalog.image.str.contains(".png")]
    catalog = catalog.sort_values(by=['similarity'], ascending=False).reset_index(drop=True)

    url_list = catalog.head(10)["image"].to_list()
    
    return url_list