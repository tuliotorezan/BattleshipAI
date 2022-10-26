from re import S
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        flatsize = input_size[0]*input_size[1]
        #self.flatten = nn.Flatten()
        #self.linear1 = nn.Linear(flatsize, hidden_size)
        self.linear1 = nn.Conv2d(1,hidden_size, 3)
        self.flatten = nn.Flatten()
        self.linear2 = nn.Linear(8*8, hidden_size) #since the map is size 10x10 and kernel is 3, the resulting map after convolution is 8x8
        self.linear3 = nn.Linear(hidden_size, output_size)
        
    def forward(self,x):
        x = F.relu(self.linear1(x))
        x = self.flatten(x)
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x
    
    def save(self, fileName="model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        fileName = os.path.join(model_folder_path, fileName)
        torch.save(self.state_dict(), fileName)
        
        
class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)
        self.criteria = nn.MSELoss()
        
    def trainStep(self, state, action, reward, nextState, done):
        #state = torch.cat(state,0).half()
        #nextState = torch.cat(nextState,0).half()
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.float)
        reward = torch.tensor(reward, dtype=torch.float)
        
        if len(reward.shape) == 0: #then we only have a single exemple, but we want format (1,x)
            #if this is false, then the data is already in the format (n, x)
            #state = torch.unsqueeze(state, 0)
            #nextState = torch.unsqueeze(nextState, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
            
        #get predicted Q values with current state
        pred = self.model(state)
        
        target = pred.clone()
        
        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(nextState))#[i]
                # newQ = reward+gamma * max(next_predicted Q value)
                target[i][torch.argmax(action).item()] = Q_new
                
        self.optimizer.zero_grad() #clearing the gradient
        loss = self.criteria(target, pred)
        loss.backward()
        self.optimizer.step()
            
            
            
            
            