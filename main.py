from weather_util import WeatherManager
import numpy as np
from sys import argv
from collections import defaultdict
import random
import torch
import torch.utils.data as Data
from torch import optim, nn
from rnn import EncoderRNN, DecoderRNN, train, evaluate
torch.manual_seed(1)


def readSeries(datadir, cities, attr):
    wm = WeatherManager(datadir)
    wm.loadSeries(cities, attr)  # , date_range=("2017-10-12","2017-11-01"))
    wm.interpolate()
    wm.averaged(base=24)
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


if __name__ == "__main__":
    datadir = argv[1]
    train_samples, eval_samples = readData(datadir)
    train_dataset = Data.TensorDataset(data_tensor=train_samples, target_tensor=train_samples)
    train_loader = Data.Dataloader(dataset=train_dataset, batch_size=32, shuffle=True, num_workers=2)
    eval_dataset = Data.TensorDataset(data_tensor=eval_samples, target_tensor=eval_samples)
    eval_loader = Data.Dataloader(dataset=eval_dataset, batch_size=32, shuffle=False, num_workers=2)

    input_size = output_size = hidden_size = train_samples.shape[1]
    encoder = EncoderRNN(input_size=input_size, hidden_size=hidden_size)
    decoder = DecoderRNN(hidden_size=hidden_size, output_size=output_size)

    train_loss_total = 0
    eval_loss_total = 0
    learning_rate = 0.01
    encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
    criterion = nn.NLLLoss()
 
    for epoch in range(10):
        for step, (batch_x, batch_y) in enumerate(train_loader):
            train_num = batch_x.shape[0]
            train_loss = train(batch_x, batch_y, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion)
            train_loss_total += train_loss

        for step, (batch_x, batch_y) in enumerate(eval_loader):
            eval_num = batch_x.shape[0]
            eval_loss = evaluate(batch_x, batch_y, encoder, decoder, criterion)
            eval_loss_total += eval_loss

        print("Epoch: ", epoch, "|Train loss: ", train_loss_total / train_num, "|Eval loss: ", eval_loss_total / eval_num)
