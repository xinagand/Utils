from matplotlib import pyplot as plt
#data_path = {'normal_train_loss_log.txt','negative_train_loss_log.txt','gray_train_loss_log.txt'}#,'negative_train2000/loss_log.txt'}
import seaborn as sns

def main():
    data_path = './data/test_1'
    show_ocgan_acc(data_path)



def show_ocgan_acc(data_path):
    print(data_path + " reading")
    acc = []
    count = 5
    with open(data_path, 'r') as f:
        for i in range(6):
            line = f.readline()
        # print(line)
        while True:
            if count == 500:
                break
            for i in range(3):
                line = f.readline()
                if not line:
                    break
            line = f.readline()
            if not line:
                break
            # print(line)
            acc.append(float(line.split('=')[1]))
            f.readline()
            count += 1
    print("best: {0} at iter {1}".format(max(acc), acc.index(max(acc))))
    plt.figure("{}".format(data_path))
    plt.plot(acc,'r-', label=data_path) # row , col
    # plt.axis((0,30,0,0.01))
    plt.legend(loc='lower right', frameon=False)

    plt.savefig('auc.png')
    plt.show()


def show_ognet_loss(data_path):
    # read data
    print(data_path + " reading")
    bepoch = []
    bdloss = []
    bgloss = []

    with open(data_path, 'r') as f:
        while True:
            epoch = f.readline()
            if not epoch:
                break
            d_loss = f.readline()
            print(d_loss)
            g_loss = f.readline()

            bepoch.append(epoch)
            bdloss.append(float(d_loss.split(' ')[1].replace('.\n', '')))
            bgloss.append(float(g_loss.split(' ')[1].replace('.\n', '')))

    for i in range(len(bepoch)):
        print(bdloss[i])

    #TODO: 정확도 찍어주기
    plt.plot(bdloss,'b-', label='d_loss') # row , col
    plt.plot(bgloss,'r-', label='g_loss') # row , col
    # plt.axis((0,30,0,0.01))
    plt.legend(loc='center right', frameon=False)

    plt.savefig('auc.png')
    plt.show()


def read_smix_log(data_path):
    epoch = []
    top1 = []
    top5 = []
    loss = []

    with open(data_path, 'r') as f:
        while True:
            line = f.readline().split(' ')
            print(line)
            if not line:
                break
            if line[0] in ['Best', '']:
                break
            epoch.append(line[2].replace('\t', ''))
            top1.append(float(line[5]))
            top5.append(float(line[9].replace('\t', '')))
            loss.append(float(line[12].replace('\n', '')))
    return epoch, top1, top5, loss


def show_smix(title, path, path2=None, path3=None):
    result = []

    data_path = path
    print(data_path + " reading")
    result.append(read_smix_log(data_path))

    if not path2:
        data_path2 = path2
        print(data_path + " reading")
        result.append(read_smix_log(data_path2))

    if not path3:
        data_path3 = path3
        print(data_path + " reading")
        result.append(read_smix_log(data_path3))

    plt.figure("{}".format(title))
    plt.plot(result[0][2],'r-', label='1') # row , col
    if not path2:
        plt.plot(result[1][2],'b-', label='2') # row , col
    if not path3:
        plt.plot(result[2][2],'g-', label='3') # row , col
    # plt.axis((0,30,0,0.01))
    plt.legend(loc='center right', frameon=False)

    plt.savefig('auc.png')
    plt.show()


def show_dist():
    #############################
    # This file it to print figures for the scores.csv file from aae_anomaly only.

    # check
    # 1. data_path : path to data
    # 2. num_data : number of input file
    # 3. title_name : title for the plt figure

    # optional
    # 1) bins : for the plot

    #############################

    data_path = ['scores.csv']
    num_data = 1
    title_name = "pohang_new"

    data = [[0] for i in range(len(data_path) * 2)]
    i = 0
    # read data
    for i in range(num_data):
        print(data_path[i] + " reading")
        count = 0
        with open(data_path[i], 'r') as f:
            for k in f:
                if count == 0:
                    count += 1
                    continue
                k = k.replace('\n', '')
                k = k.split(',')
                # k = ''.join(k)
                if "a" == k[0][0]:  # anomaly
                    # if k[0] in anomaly:  # anomaly
                    data[i + num_data].append(float(k[1]))
                else:
                    # elif k[0] in normal:
                    data[i].append(float(k[1]))
        data[i] = data[i][1:]  # cut first line.
        data[i + num_data] = data[i + num_data][1:]  # cut first line.
        i += 1

    # # threshold cut
    # databox = [[0] for i in range(4)]
    # threshold = 0.1039
    #
    # for i in range(len(data_path)):
    #     for j in data[i]:
    #         if j > threshold:
    #             databox[i].append(j)
    #     for k in data[i+2]:
    #         if k < threshold:
    #             databox[i+2].append(k)
    # plt.show()

    # Full Data Distribution
    bins = 100  # bin for histogram
    plt.figure(figsize=(15, 10))
    for i in range(num_data):
        sub = str(num_data) + '1' + str(i + 1)
        plt.subplot(sub)
        if i == 0:
            plt.title(title_name)
        sns.distplot(data[i], hist=True, kde=True,
                     bins=bins, color='blue',
                     hist_kws={'edgecolor': 'black'},
                     kde_kws={'linewidth': 2},
                     label="Normal")
        sns.distplot(data[i + num_data], hist=True, kde=True,
                     bins=bins, color='red',
                     hist_kws={'edgecolor': 'black'},
                     kde_kws={'linewidth': 2},
                     label="Abnormal")
        plt.xlabel('score')
        plt.ylabel('density')
        plt.legend(loc='upper right')
    plt.savefig(title_name + '.png')
    plt.show()


def show_graph():
    data_path = ['loss_log.txt']
    num_data = 1

    dataset = ['Simulation Map']
    title_name = ''
    for i, data in enumerate(dataset):
        title_name += data
        if i + 1 < len(dataset):
            title_name += ' vs '

    data = []
    i = 0
    # read data
    for i in range(num_data):
        print(data_path[i] + " reading")
        data.append([])
        with open(data_path[i], 'r') as f:
            for k in range(1000):
                tmp = f.readline()
                tmp = tmp.replace('Avg Run Time (ms/batch): ', 'Avg_Run_Time_(ms/batch): ')
                tmp = tmp.replace('max AUC: ', 'max_AUC: ')
                tmp = tmp.replace(':', '')
                tmp = tmp.replace('\n', '')
                tmp = tmp.split(' ')
                tmp = tmp[3:]
                print(tmp)
                data[i].append(tmp)
        data[i] = data[i][1:]
        i += 1

    # for q in data:
    #     print('\n')
    #     for w in q:
    #         print(w)

    EER = []
    AUC = []
    max_AUC = []
    for count in range(num_data):
        # print(count)
        EER.append([])
        AUC.append([])
        max_AUC.append([])
        for i in data[count]:
            # print(i)
            EER[count].append(float(i[3]))
            AUC[count].append(float(i[5]))
            max_AUC[count].append(float(i[7]))

    plt.figure(figsize=(15, 10))
    plt.subplot(311)
    plt.plot(AUC[0], 'b-', label=dataset[0])  # row , col
    # plt.plot(AUC[1] ,'r-', label=dataset[1]) # row , col
    plt.xlabel('epoch')
    plt.ylabel('AUC')
    plt.yscale('linear')
    plt.legend(loc='lower right', frameon=False)

    plt.subplot(312)
    plt.plot(max_AUC[0], 'b-', label=dataset[0])  # row , col
    # plt.plot(max_AUC[1] ,'r-', label=dataset[1]) # row , col
    # plt.plot(AUC[2],'g-') # row , col
    plt.xlabel('epoch')
    plt.ylabel('max_AUC')
    plt.yscale('linear')
    plt.legend(loc='lower right', frameon=False)

    plt.subplot(313)
    plt.plot(EER[0], 'b-', label=dataset[0])  # row , col
    # plt.plot(EER[1] ,'r-', label=dataset[1]) # row , col
    # plt.plot(AUC[2],'g-') # row , col
    plt.xlabel('epoch')
    plt.ylabel('EER')
    plt.yscale('linear')
    plt.legend(loc='upper right', frameon=False)

    plt.savefig('training auc.png')
    plt.show()


if __name__ == '__main__':
    main()
