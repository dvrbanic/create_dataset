import re
import matplotlib.pyplot as plt

iterations = 0
iters_list = []


def show_plot(iteration, loss, path='loss.png'):
    plt.plot(iteration, loss)
    plt.savefig(path)


with open('loss.txt', 'r') as infile:
    file_reader = infile.read()
    list_losses = re.findall(f'Current loss 0.\d+', file_reader)
    list_losses = [float(loss.split()[-1]) for loss in list_losses]
    for i in range(len(list_losses)):
        iterations += 10
        iters_list.append(iterations)


show_plot(iters_list, list_losses, path='loss_.png')
