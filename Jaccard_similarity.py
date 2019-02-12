#compute similarity

from __future__ import division
import argparse
import sqlite3 as sq
import pandas as pd

class jaccard_similarity():

    def __init__(self, dbpath):
        self.dbpath=dbpath
        conn = sq.connect(self.dbpath)
        self.user_tags = pd.read_sql_query("SELECT * FROM user_tags", conn)
        self.user_tags["all_tags"] = [eval(t) for t in self.user_tags['all_tags']]

    def get_interest_list(self, user_handle):
        self.user_handle=user_handle
        user_interest = self.user_tags[self.user_tags["user_handle"]==self.user_handle]["all_tags"][0]
        return user_interest

    def compute_jaccard_similarity(self, user_handle, threshold):
        self.user_handle=int(user_handle)
        self.threshold=float(threshold)
        self.similar_users = []
        user_interest = self.get_interest_list(self.user_handle)
        for i, user in self.user_tags.iterrows():
            intersection = len(list(user_interest.intersection(user["all_tags"])))
            union = (len(user_interest) + len(user["all_tags"])) - intersection
            jaccard_score = intersection / union
            if jaccard_score >= self.threshold:
                self.similar_users.append((user["user_handle"], round(jaccard_score * 100, 2)))
        self.similar_users.remove((self.user_handle, 100.0))
        return self.similar_users


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-db", "--dbpath", required=True, help="Sqlite DB File path")
    ap.add_argument("-uh", "--user_handle", required=True, help="User Handle")
    ap.add_argument("-thrsh", "--threshold", required=True, help="0 to 1 Ex: 0.5 would give atleast 50% matching users")
    args = vars(ap.parse_args())
    js=jaccard_similarity(args["dbpath"])
    user_summary=js.compute_jaccard_similarity(args["user_handle"], args["threshold"])
    print("Listing User handles and percent matching for User-{}".format(args["user_handle"]))
    for t in user_summary:
        print("User {} matches {} percent".format(t[0],t[1]))

if __name__ == "__main__":
    main()


