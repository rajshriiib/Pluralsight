
import argparse
import pandas as pd
import sqlite3 as sq
import numpy as np


class create_user_tags_table():
    def __init__(self, dbpath):
        self.conn = sq.connect(dbpath)
        self.user_interest = pd.read_sql_query("SELECT * FROM user_interest", self.conn)
        self.user_assessment = pd.read_sql_query("SELECT * FROM user_assessment", self.conn)
        self.course_views = pd.read_sql_query("SELECT * FROM course_views", self.conn)
        self.course_tags = pd.read_sql_query("SELECT * FROM course_tags", self.conn)

    def dedup(self, x):
        if type(x) is list:
            return set(x)
        return set()

    def get_df(self):
        user_interest_byuser = self.user_interest.groupby("user_handle")["interest_tag"].apply(list).reset_index()
        user_assessment_byuser = self.user_assessment.groupby("user_handle")["assessment_tag"].apply(list).reset_index()
        grp_course_tags = self.course_tags.groupby("course_id")["course_tags"].apply(list).reset_index()

        user_course_tags = self.course_views.merge(grp_course_tags, how="left", on="course_id")
        user_course_tags_byuser = user_course_tags.groupby("user_handle")["course_tags"].apply(list).reset_index()
        user_course_tags_byuser["course_tags"] = [[x for sub_list in l for x in sub_list] for l in
                                                  user_course_tags_byuser["course_tags"]]

        user_interest_assess = user_interest_byuser.merge(user_assessment_byuser, how="left", on="user_handle")
        user_interest_assess_tags = user_interest_assess.merge(user_course_tags_byuser, how="left", on="user_handle")

        user_interest_assess_tags["interest_tag"] = [self.dedup(x) for x in user_interest_assess_tags["interest_tag"]]
        user_interest_assess_tags["assessment_tag"] = [self.dedup(x) for x in user_interest_assess_tags["assessment_tag"]]
        user_interest_assess_tags["course_tags"] = [self.dedup(x) for x in user_interest_assess_tags["course_tags"]]

        user_interest_assess_tags['all_tags'] = user_interest_assess_tags.apply(
            lambda x: (x['interest_tag'] | x['assessment_tag'] | x['course_tags']), axis=1)
        user_interest_assess_tags['all_tags'] = [str(t) for t in user_interest_assess_tags['all_tags']]
        user_interest_assess_tags[["user_handle", "all_tags"]].to_sql("user_tags", self.conn, if_exists='replace',
                                                                      index=False)

        cur = self.conn.cursor()
        cur.execute("SELECT max(rowid) from user_tags")

        if cur.fetchone()[0] > 0:
            return "Refreshed user_tags"

        return "Not Created"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-db", "--dbpath", required=True, help="Sqlite DB File path")
    args = vars(ap.parse_args())
    ct = create_user_tags_table(args["dbpath"])
    print(ct.get_df())

if __name__ == "__main__":
    main()

