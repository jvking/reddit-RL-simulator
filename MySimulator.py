#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created by Ji He, Jan. 21st, 2016
# last modified by Ji He, Sep. 5th, 2016

# This program provides a simulation environment for the task of predicting and tracking popular discussion threads, on Reddit.
# You may refer to our paper for more information: https://arxiv.org/abs/1606.03667

import argparse
from itertools import izip
import numpy as np
import pandas as pd
import sqlite3
import time

class RedditNavigationSimulator:
    def __init__(self, dataFile = "data/askscience.db", mode = 1, dict_config = {"doShuffle": True, "K": 3, "N": 10, "T": 7200, "M": None, "trainRatio": 0.9}):
        # load a 5k Reddit vocabulary
        self.vocabulary = dict([(line.rstrip().split(" ")[0], int(line.rstrip().split(" ")[1])) for line in open("reddit_vocab_5k.txt", "r")])
        # mode = 0: tracking based on tree structures, not time stamps, immediate children (direct responses) are returned
        # mode = 1: tracking based on time stamps (more real-time scenario), first N children (in subtrees) are returned
        # mode = 2: tracking based on time stamps, first N children (direct responses) are returned
        # mode = 3: tracking based on time stamps, after T timeStep, tracked children (in subtrees) are returned
        # mode = 4: tracking based on time stamps, after T timeStep, tracked children (direct responses) are returned
        # K: every time pick K comments to follow, N: every time at most N new comments can be shown (in mode 1/2), T: timeStep in mode 3/4, M: if not None, only the most M comments will be in the state
        conn = sqlite3.connect(dataFile)
        if "askmen" in dataFile or "askwomen" in dataFile or "askscience" in dataFile or "atheism" in dataFile or "changemyview" in dataFile or "fitness" in dataFile or "politics" in dataFile or "worldnews" in dataFile:
            df_post = pd.read_sql_query("SELECT id,subreddit,title,score,num_comments,created FROM posts", conn)
        else:
            df_post = pd.read_sql_query("SELECT id,subreddit,title,score,num_comments,created_utc FROM posts", conn)
            df_post.columns = [u'id', u'subreddit', u'title', u'score', u'num_comments', u'created']
        df_comment = pd.read_sql_query("SELECT id,body,score,parent_id,link_id,timestamp FROM comments", conn)
        conn.close()
        self.mode = mode # this is important for configuration
        self.dict_config = dict_config
        # construct a id-index dictionary for the whole database
        self.dict_id_idx = dict(izip(("t1_" + df_comment['id']).tolist(), df_comment.index.tolist()))
        # split train/test
        indices_post = range(len(df_post))
        # np.random.shuffle(indices_post)
        self.indices_train = indices_post[: int(self.dict_config["trainRatio"] * len(df_post))]
        self.indices_test = indices_post[int(self.dict_config["trainRatio"] * len(df_post)): ]
        self.data_set = []
        for post_index in range(len(df_post)):
            self.data_set.append((df_post.ix[post_index], df_comment[df_comment['link_id'] == ("t3_" + df_post.ix[post_index]['id'])]))
        self.Restart()
        
    def Restart(self, dataset = "train"):
        while True: # pick a non-empty discussion tree
            self.post_index = np.random.choice(self.indices_train) if dataset == "train" else np.random.choice(self.indices_test)
            # extract discussion tree associated with self.post_index
            self.post, self.df_tree = self.data_set[self.post_index]
            if len(self.df_tree):
                break
        # store the root node (post) as initially tracked comment
        self.state = [self.post['title']]
        self.tracked_ids = ["t3_" + self.post['id']]
        self.reward = 0
        if self.mode <> 0: # construct a list of indices with timeStamps from old to new
            self.current_time = int(float(self.post['created'])) - 3600 # due to different time representation when collecting data
            self.comments_time = [temp['timestamp'] for _, temp in self.df_tree.iterrows()]
            self.idx_checked_comment = 0 # this marks the index of the checked comment
        return

    def Read(self):
        if self.mode == 0:
            mask = [temp in self.tracked_ids for temp in self.df_tree['parent_id']]
        elif self.mode == 1:
            mask = [False] * len(self.df_tree)
            while self.idx_checked_comment < len(self.df_tree) and sum(mask) < self.dict_config["N"]:
                # check the idx_checked_comment-th comment, and see if it is in subtree
                temp = self.df_tree.iloc[self.idx_checked_comment]
                flag = True
                while temp['parent_id'] not in self.tracked_ids:
                    if temp['parent_id'] not in self.dict_id_idx: # not in subtree, including when parent_id starts with "t3_"
                        flag = False
                        break
                    temp = self.df_tree.ix[self.dict_id_idx[temp['parent_id']]] # go to parent comment
                if flag: # idx_checked_comment-th comment is in subtree
                    mask[self.idx_checked_comment] = True
                self.idx_checked_comment += 1
        elif self.mode == 2:
            mask = [False] * len(self.df_tree)
            while self.idx_checked_comment < len(self.df_tree) and sum(mask) < self.dict_config["N"]:
                # check the idx_checked_comment-th comment, and see if it is immediate child
                if self.df_tree.iloc[self.idx_checked_comment]['parent_id'] in self.tracked_ids:
                    mask[self.idx_checked_comment] = True
                self.idx_checked_comment += 1
        elif self.mode == 3:
            mask = [temp['timestamp'] > self.current_time and temp['timestamp'] <= self.current_time + self.dict_config["T"] for _, temp in self.df_tree.iterrows()]
            for self.idx_checked_comment in np.where(mask)[0]:
                temp = self.df_tree.iloc[self.idx_checked_comment]
                flag = True
                while temp['parent_id'] not in self.tracked_ids:
                    if temp['parent_id'] not in self.dict_id_idx: # not in subtree, including when parent_id starts with "t3_"
                        flag = False
                        break
                    temp = self.df_tree.ix[self.dict_id_idx[temp['parent_id']]] # go to parent comment
                if not flag: # idx_checked_comment-th comment is not in subtree
                    mask[self.idx_checked_comment] = False
        elif self.mode == 4:
            mask = [temp['timestamp'] > self.current_time and temp['timestamp'] <= self.current_time + self.dict_config["T"] for _, temp in self.df_tree.iterrows()]
            for self.idx_checked_comment in np.where(mask)[0]:
                if not self.df_tree.iloc[self.idx_checked_comment]['parent_id'] in self.tracked_ids:
                    mask[self.idx_checked_comment] = False
        # get new comments in a data frame
        self.df_new_comments = self.df_tree[mask]
        actions = [temp for temp in self.df_new_comments['body']]

        if self.dict_config["doShuffle"]:
            self.idxShuffle = range(len(actions))
            np.random.shuffle(self.idxShuffle)
            actions = [actions[i] for i in self.idxShuffle]
        return self.state, actions, self.reward # we are not providing terminal variable, and assume if len(actions) == 0 then terminal = True

    def Act(self, playerInputs):
        # playerInputs is a list of selected comments, the order does not matter, although it might affect the state a little bit
        if self.dict_config["doShuffle"]:
            playerInputs = [self.idxShuffle[i] for i in playerInputs]
        # update state/tracked_ids/reward
        self.state += [self.df_new_comments.iloc[i]['body'] for i in playerInputs]
        self.tracked_ids = ["t1_" + self.df_new_comments.iloc[i]['id'] for i in playerInputs]
        self.reward = sum([self.df_new_comments.iloc[i]['score'] for i in playerInputs])
        # if state is set to a fixed memory M
        if self.dict_config["M"] <> None and len(self.state) > self.dict_config["M"]:
            self.state[: len(self.state) - self.dict_config["M"]] = []

        if self.mode == 3 or self.mode == 4:
            # advance the current_time by self.dict_config["T"]
            self.current_time += self.dict_config["T"]
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Reddit navigation simulator", epilog = "E.g. ./MySimulator.py --mode 1 --K 3 --N 10 --dataFile data/askscience.db")
    parser.add_argument('--mode', type = int, required = False, default = 1)
    parser.add_argument('--K', type = int, required = True) # we choose 3 mostly in our paper
    parser.add_argument('--N', type = int, required = True) # we choose 10 in our paper
    parser.add_argument('--T', type = int, required = False, default = 7200)
    parser.add_argument('--M', type = int, required = False, default = None)
    parser.add_argument('--dataFile', type = str, required = True)
    args = parser.parse_args()
    dict_config = {"doShuffle": True, "K": args.K, "N": args.N, "T": args.T, "M": args.M, "trainRatio": 0.9}

    np.random.seed(seed = 1234)
    mySimulator = RedditNavigationSimulator(dataFile = args.dataFile, mode = args.mode, dict_config = dict_config)

    startTime = time.time()
    numEpisode = 0
    while numEpisode < 10000:
        state, actions, reward = mySimulator.Read()
        print("state: " + str(state))
        print("actions: " + str(actions))
        print("reward: " + str(reward))
        if len(actions) == 0:
            mySimulator.Restart()
            numEpisode += 1
        else:
            playerInputs = map(int, raw_input().split())
            mySimulator.Act(playerInputs)

    endTime = time.time()
    print("Duration: " + str(endTime - startTime))
