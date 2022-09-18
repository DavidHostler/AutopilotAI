# AutopilotAI
A revisited edition of my original self-driving AI portfolio project from early 2021. It is meant to provide a temporary autopilot for PC gamers who need to go AFK for brief periods of time. 

#Description and Theory 


Currently the model relies on a basic recurrent LSTM network in Keras to make predictions on time-series data related to a user's keypresses.
Given a blindly driving model and relatively consistent yet random road conditions (presumes no sudden unexpected turns), the AI should be able to 
predict to a high degree of success what buttons on your keyboard to push in order to keep driving, should the driver suddenly go AFK.

Significant improvements were made over the 2021 model. Whereas before, I trained the model on recurrent past datapoints, this time I employed techniques 
from stochastic calculus to introduce very significant regularization to the model.
If the time series data is assumed to undergo something approximating Geometric Brownian Motion (GBM), then it stands to reason that in the limit as the size of each timestep becomes infinitesimal and the model is allowed to run on increasingly large timescales, then the data related to user keypress decisions now approximates a continuous martingale.

A common technique in some areas of machine learning, such as Variational Autoencoders, Generative Adversarial Networks, and even in some deep reinforcement learning algorithms, is to introduce Gaussian noise data. It seems that if you do this, such that every successive predicted value lies within a Gaussian distribution centred around the previous value in the sequence of training data, then the expectation value of the joint probability of the latter event given the first simply is the value of the latter-which is precisely the definition of a martingale!

Training the model recurrently on a multiple sequences of normally distributed random  variables (i.e. noisy data), in the limit as the number of noisy data curves becomes very large, becomes a Gaussian process by the Central Limit Theorem. 
Additionally, it seems that if the Gaussians have a moderate variance (less narrow around the mean, mu), predictions in time become more accurate. I hypothesize that this is likely related to the derivative of a Gaussian having ~ 1/sigma^2 dependence, and its effects on backpropagation through the network.


#Improvements

The model drives blind for now. A huge reason for this is that I haven't been able to implement a CNN in real time that could be pre-trained and then run, for the simple reason that most gaming PC's already running a game begin to struggle under the computational load. 
Hopefully I get contributions in the form of help from some friends that own an RTX 3000 series or higher! :)

Once the model is no longer "driving blind", it'll be interesting to model its behaviour against other similar self-driving related projects.

I may even open a branch making direct use of a Transformer for time-series forecasting- given its infinite attention window and versatility.
The one advantage that LSTM has over Transformers is that it neither takes much data nor very long to train the LSTM- at the cost of a limited 
window of memory, as the architecture of LSTM layers incorporates deliberate "forgetfulness" for older learned features.


