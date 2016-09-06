# Reddit-RL-simulator
This repository provides simulator codes for predicting and tracking popular discussion threads on Reddit.

### Data
[Google drive link](https://drive.google.com/open?id=0B1E_psSh6yvQQ0FJRWJBTDFQQ1U)

Please copy the .db database files and put them under reddit-RL-simulator/data/

### Usage (dependencies: Python 2.7)
```
python MySimulator.py --K 3 --N 10 --dataFile data/askscience.db
```
After typing the above command, you will see the following print-outs (state, list of sub-actions, reward). The sub-action order may differ:
>state: [u'Is the heat I feel when I face a bonfire transmitted to me mostly by infrared radiation or by heated air?']


### Reference
1. Ji He, Mari Ostendorf, Xiaodong He, Jianshu Chen, Jianfeng Gao, Lihong Li and Li Deng. [_Deep Reinforcement Learning with a Combinatorial Action Space for Predicting and Tracking Popular Discussion Threads._](http://arxiv.org/abs/1606.03667) Conference on Empirical Methods in Natural Language Processing (EMNLP). 2016.
