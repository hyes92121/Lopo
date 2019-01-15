from weather_util import WeatherManager
import numpy as np
from sys import argv
from collections import defaultdict
import random
import torch.utils.data as Data
torch.manual_seed(1)
    

def readSeries(datadir, cities, attr):
    wm = WeatherManager(datadir)
    wm.loadSeries(cities, attr) #, date_range=("2017-10-12","2017-11-01"))
    wm.interpolate()
    wm.averaged(base = 24)
    series = wm.getSeries()
    return series

def sliceSeries(two_d_array, length):
    tmp = []
    for i in range(0, two_d_array.shape[1], length):
        sliced = two_d_array[:, i:i+length]
        if sliced.shape[1] == length:
            tmp.append(sliced)
    return tmp 

def readData(datadir):
    cities = ["Philadelphia", "New York", "Montreal", "Boston", "Eilat", "Haifa", "Nahariyya", "Jerusalem"]
    temp = readSeries(datadir, cities, "temperature")
    press = readSeries(datadir, cities, "pressure")
    humid = readSeries(datadir, cities, "humidity")
    speed = readSeries(datadir, cities, "wind_speed")
    direc = readSeries(datadir, cities, "wind_direction")

    data = defaultdict(np.array)
    for idx, city in enumerate(cities):
        data[city] = sliceSeries(np.stack([temp[idx], press[idx], humid[idx], speed[idx], direc[idx]]), 365)

    samples = []
    for city in data:
        for series in data[city]:
            samples.append(series)
    random.shuffle(samples)
    train_samples, eval_samples = samples[:int(len(samples)*0.8)], samples[int(len(samples)*0.8):]
    train_samples, eval_samples = torch.from_numpy(np.stack(train_samples)), torch.from_numpy(np.stack(eval_samples))
    return train_samples, eval_samples 


def trainIters(train_pairs, eval_pairs, encoder, decoder, n_iters, print_every=1000, learning_rate=0.01):
    start = time.time()
    plot_losses = []
    print_loss_total = 0  # Reset every print_every
    plot_loss_total = 0  # Reset every plot_every

    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    training_pairs = [tensorsFromPair(p) for p in train_pairs]
    criterion = nn.NLLLoss()

    for iter in range(len(training_pairs) + 1):
        train_input_tensor, train_target_tensor = training_pairs[iter - 1][0], training_pairs[iter - 1][1]

        loss = train(train_input_tensor, train_target_tensor, encoder,
                     decoder, encoder_optimizer, decoder_optimizer, criterion)
        print_loss_total += loss
        plot_loss_total += loss

        if iter % print_every == 0:
            print_loss_avg = print_loss_total / print_every
            print_loss_total = 0
            print('%s (%d %d%%) %.4f' % (timeSince(start, iter / n_iters),
                                         iter, iter / n_iters * 100, print_loss_avg))


            

if __name__ == "__main__":
    datadir = argv[1]
    train_samples, eval_samples = readData(datadir)
    train_dataset = Data.TensorDataset(data_tensor=train_samples, target_tensor=train_samples)
    loader = Data.Dataloader(dataset=train_dataset, batch_size=32, shuffle=True, num_workers=2)
    for epoch in range(10):
        for step, (batch_x, batch_y) in enumerate(loader):



    

