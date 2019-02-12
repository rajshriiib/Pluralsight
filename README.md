# Pluralsight
Technical challenge
Please download db file from the drive - https://drive.google.com/file/d/1Fup4hxsYjV0B6a7wTeHWx3aPgX1x_TI8/view?usp=sharing

Sample run codes:

#to refresh user_tags table(created from 4 base tables - user_interest,user_assessment,course_views,course_tags)

python User_table_creation.py -db "user_similarity.db" 

#to get similar users - provide a user_handle and threshold(0 to 1)

python Jaccard_similarity.py -db "user_similarity.db" -uh 1 -thrsh 0.5

