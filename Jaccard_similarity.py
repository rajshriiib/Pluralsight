#compute similarity

class jaccard_similarity():

    def __init__(self, dbpath):
        conn = sq.connect(dbpath)
        self.user_tags = pd.read_sql_query("SELECT * FROM user_tags", conn)
        self.user_tags["all_tags"] = [eval(t) for t in self.user_tags['all_tags']]

    def get_interest_list(self, user_handle):
        user_interest = self.user_tags[self.user_tags["user_handle"] == user_handle]["all_tags"][0]
        return user_interest

    def compute_jaccard_similarity(self, user_handle, threshold):
        similar_users = []
        self.user_interest = get_interest_list(user_handle)
        # jaccard_similarity
        for i, user in self.user_tags.iterrows():
            intersection = len(list(self.user_interest.intersection(user["all_tags"])))
            union = (len(self.user_interest) + len(user["all_tags"])) - intersection
            jaccard_score = float(intersection / union)
            if jaccard_score >= threshold:
                similar_users.append((user["user_handle"], round(jaccard_score * 100, 2)))
        similar_users.remove((user_handle, 100.0))
        return similar_users

