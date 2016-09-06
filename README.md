# Reddit-RL-simulator
This repository provides simulator codes for predicting and tracking popular discussion threads on Reddit.

### Data
[Google drive link](https://drive.google.com/open?id=0B1E_psSh6yvQQ0FJRWJBTDFQQ1U)

Please copy the .db database files and put them under reddit-RL-simulator/data/

### Basic Usage (dependencies: Python 2.7)
To run the simulation, simply type:
```
python MySimulator.py --K 3 --N 10 --dataFile data/askscience.db
```
After typing the above command, you will see the following three print-outs (state, list of sub-actions, reward). The sub-action order may differ.

State is a list of comments being tracked (the length of list depends on _M_ argument):
>state: [u'Is the heat I feel when I face a bonfire transmitted to me mostly by infrared radiation or by heated air?']

The second print-out is a list of sub-actions (in our combinatorial setting, an action is selecting _K_ sub-actions from _N_ sub-action candidates. In this demo, _N_=10):
>actions: [u"Thanks! Follow up question, if it's not too complicated to answer: Similar to what henrebotha asked, how come visible light doesn't heat me up while infrared wavelengths do? Do other wavelengths warm humans similarly to infrared, or is that a property unique to that range of the spectrum?", u'[deleted]', u'[deleted]', u"&gt; visible light\n\nBut then (and please forgive the extremely ignorant question) why doesn't it feel hot when I shine a flashlight at my face? \n\nEDIT: Thanks, I've gotten plenty of half explanations now. ", u'Yes, you are right. \n\nThe thermal radiation created by the bonfire travels away in all directions. Heat that is transferred via convection mostly travels upwards as the heated air billows up. If you are to the side of the fire, the heat you receive is transferred via thermal radiation. If you are standing directly above the fire, you receive heat from both thermal radiation *and* convection. For this reason, directly above the fire is the hottest place to be. I don\'t recommend it. \n\nNote that thermal radiation can include many different wavelengths of electromagnetic radiation and not just infrared, although infrared is the dominant type near room temperature. For a bonfire, the thermal radiation is composed of both infrared radiation *and* visible light in significant amounts.\n\nUPDATE: In loose usage, the term "thermal radiation" means "radiation that is able to heat an object upon being absorbed by the object". In this usage, all electromagnetic radiation is thermal radiation, from radio waves to gamma rays. In the more strict usage of the term, "thermal radiation" means "radiation that is produced in a broad spectrum that depends on the temperature of the source". In this stricter usage, the visible light from LED flashlights is not thermal radiation, since LED flashlights do not operate that way. Each photon from the LED flashlight is not different from a photon of the same frequency from a campfire - they can both heat something they strike. But the spectral frequency distribution of the photons from an LED bulb is not thermal.', u"But read the post above mine:\n\n&gt; the **thermal** radiation is composed of both infrared radiation and visible light **in significant amounts**.\n\nIt's saying there's a significant amount of visible thermal radiation. What's the difference between visible thermal radiation and light? ", u'[deleted]', u'It is simply because of power. A good old fashioned flashlight with a tungsten bulb will probably emit 90% infra red and 10% visible, but there will only be 20 watts in total. A bonfire on the other hand will be emitting around 5,000 to 50,000 watts or more, mostly in the infra red spectrum.\n\nStand next to a 1000 watt light bulb, you will feel the heat.\n\nEDIT: Reading some of the replies below, there is one example everybody can relate to. If you set up a 1000 watt green laser beam (that would be a powerful cutting laser) it can be entirely visible light on one wavelength, but it will heat up and vaporise a piece of steel some distance away. But to confuse things, a lot of cutting lasers use infra red light simply because it is more efficient to produce.', u"&gt;Stand next to a 1000 watt light bulb, you will feel the heat.\n\nBut aren't you still just feeling the heat from IR given off by the bulb, not the visible light? I sounds /u/henrebotha was thinking that by /u/chrisbaird's description, /uchrisbaird is saying that you feel the heat from the visible light given off by the bonfire.", u'Flashlights are designed to primarily output visible light, IR output is minimized. ']

The reward is summing up Karma scores in the action at the last time step. Since we just start tracking this discussion tree (the state is the post itself), this time step our reward is 0:
>reward: 0

You can continue the simulation of tracking threads by typing your choice of action (a list of integers). For example, typing "0 3 4" (choosing "Thanks! Follow up question ...", "&gt; visible light\n\nBut then ...", and "Yes, you are right. \n\nThe thermal radiation ...") at the above state will transition to the next tuple:

State:
>state: [u'Is the heat I feel when I face a bonfire transmitted to me mostly by infrared radiation or by heated air?', u"Thanks! Follow up question, if it's not too complicated to answer: Similar to what henrebotha asked, how come visible light doesn't heat me up while infrared wavelengths do? Do other wavelengths warm humans similarly to infrared, or is that a property unique to that range of the spectrum?", u"&gt; visible light\n\nBut then (and please forgive the extremely ignorant question) why doesn't it feel hot when I shine a flashlight at my face? \n\nEDIT: Thanks, I've gotten plenty of half explanations now. ", u'Yes, you are right. \n\nThe thermal radiation created by the bonfire travels away in all directions. Heat that is transferred via convection mostly travels upwards as the heated air billows up. If you are to the side of the fire, the heat you receive is transferred via thermal radiation. If you are standing directly above the fire, you receive heat from both thermal radiation *and* convection. For this reason, directly above the fire is the hottest place to be. I don\'t recommend it. \n\nNote that thermal radiation can include many different wavelengths of electromagnetic radiation and not just infrared, although infrared is the dominant type near room temperature. For a bonfire, the thermal radiation is composed of both infrared radiation *and* visible light in significant amounts.\n\nUPDATE: In loose usage, the term "thermal radiation" means "radiation that is able to heat an object upon being absorbed by the object". In this usage, all electromagnetic radiation is thermal radiation, from radio waves to gamma rays. In the more strict usage of the term, "thermal radiation" means "radiation that is produced in a broad spectrum that depends on the temperature of the source". In this stricter usage, the visible light from LED flashlights is not thermal radiation, since LED flashlights do not operate that way. Each photon from the LED flashlight is not different from a photon of the same frequency from a campfire - they can both heat something they strike. But the spectral frequency distribution of the photons from an LED bulb is not thermal.']

List of sub-actions:
>actions: [u"If I'm not mistaken, it also depends on your skin tone. If you have a rather pasty complexion, you reflect most visible light (that's why the skin appears 'white') but if you have a darker skin tone, you are absorbing all wavelengths except those that you can see.", u'Thanks for the clarification.', u'I think what he meant is that if you had a hypothetical bulb that emitted 1000 watts *of visible light* but nothing in IR, it would feel very warm.\n\nNothing like that currently exists-- even the most efficient red LEDs are still putting out half or more of their output as waste heat rather than visible light.  But you could approximate the effect with a couple of pieces of IR-filter glass, so that only light shone on you.\n\nTo get the same amount of "feeling of heat" from just visible light to compare to a campfire would be stupendously bright.  Since we can\'t see IR, there isn\'t a good intuitive understanding of how "bright" a campfire would be.  ', u'[deleted]', u'Do you mean "INvisible thermal radiation"? \n\nTechnically, there is no difference between thermal radiation and light. They are both examples of electromagnetic radiation (i.e. conducted by photons). However, what we commonly refer to when we say "light" is the visible spectrum, approximately 390 - 700 nm (violet to deep red).\n\nEdit: Just wanted to add that how efficient the flashlight is depends on how the light is generated. If they use the old tungsten type bulbs, which basically relies on heating a thin piece of wire until it glows, then most of the light generated is infrared rather than visible. Newer flashlights use LEDs, which generate light by using the movement of electrons, and therefore generate more light in the visible spectrum.', u'[deleted]', u'We had a handheld floodlight at my old workplace that was so powerful you could feel it burning after 10-20 seconds, even when you were a few yards from it. ', u'A significant amount of the visible light is still being absorbed by your skin, and results in heating. ', u'[deleted]', u"One can feel heat from both infrared and visible light. There's just more infrared present so that does the majority of heating. \n\nEdit: I'd like to mention that some saunas use IR light as a heat source for the occupants. IIRC some airplanes use it for de-icing their wings as well. "]

Reward:
>reward: 1772

You can edit the main function in MySimulator.py to hook up with your own agent and RL framework. The interface of all three text games are designed so that they share the same interface:
```
(state, actions, reward) = mySimulator.Read() # state is a list of string (state-text), actions is a list of strings (sub-actions), reward is a float
mySimulator.Act(playerInput)                  # playerInput is a list of integers
mySimulator.Restart(dataset = "train")        # after the episode ends, restart the game.
```
Note that in mySimulator.Restart() function, user can choose to restart with a discussion tree in either train/test (by setting dataset to "train" or "test"). This way we make sure the models are trained and tested with different discussion trees to show how well the models generalize.

### More Details
reddit-RL-simulator/reddit_vocab_5k.txt stores the most frequent 5K vocabulary of Reddit data set.

There are more arguments with MySimulator.py:

**--mode**:

There are 5 modes in our simulator. In [1] we always chose mode=1 to ensure we are learning in a "real-time" threads tracking scenario.

  mode = 0: tracking based on tree structures, not time stamps, immediate children (direct responses) are returned  
  mode = 1: tracking based on time stamps (more real-time scenario), first N children (in subtrees) are returned  
  mode = 2: tracking based on time stamps, first N children (direct responses) are returned  
  mode = 3: tracking based on time stamps, after T timeStep, tracked children (in subtrees) are returned  
  mode = 4: tracking based on time stamps, after T timeStep, tracked children (direct responses) are returned

--K:

--N:

--T:

--M:

--dataFile:



### Reference
1. Ji He, Mari Ostendorf, Xiaodong He, Jianshu Chen, Jianfeng Gao, Lihong Li and Li Deng. [_Deep Reinforcement Learning with a Combinatorial Action Space for Predicting and Tracking Popular Discussion Threads._](http://arxiv.org/abs/1606.03667) Conference on Empirical Methods in Natural Language Processing (EMNLP). 2016.
