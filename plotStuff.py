import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, meanScores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training")
    plt.xlabel("Games")
    plt.ylabel("Scores")
    plt.plot(scores)
    plt.plot(meanScores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(meanScores)-1, meanScores[-1], str(meanScores[-1]))