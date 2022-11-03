import os
import numpy as np
import pandas as pd


# file_dirs = ['2021_03_10', '2021_03_11',
#              '2021_03_12', '2021_05_15',
#              '2021_05_17', '2021_06_04',
#              '2021_06_14', '2021_06_17']
file_dirs = ['today', 'today']
# file_dirs = ['2021_03_10', '2021_03_11',
#              '2021_03_12', '2021_05_15',
#              '2021_05_17']

def trial_info():
    n_trials_R = 0
    n_trials_R_tot = 0
    n_trials_L = 0
    n_trials_L_tot = 0
    n_trials_Z = 0
    n_trials_Z_tot = 0

    other = 0

    for i in range(len(file_dirs)):
        directory = os.getcwd() + '/' + file_dirs[i]
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                if filename.startswith("R"):
                    # print(os.path.join(directory, filename))
                    n_trials_R += 1
                elif filename.startswith("L"):
                    # print(os.path.join(directory, filename))
                    n_trials_L += 1
                elif filename.startswith("Z"):
                    n_trials_Z += 1
                else:
                    other += 1
            else:
                continue

        print('---------------------------------------------------')
        print('Folder ' + str(i+1) + ' results')
        print('---------------------------------------------------')
        print('Right hand trials: ' + str(n_trials_R))
        print('Left hand trials: ' + str(n_trials_L))
        print('Rest trials: ' + str(n_trials_Z))
        print('Total folder trials: ' + str((n_trials_R + n_trials_L + n_trials_Z)))
        print('Total folder samples: ' + str((n_trials_R + n_trials_L + n_trials_Z)*4))

        n_trials_R_tot += n_trials_R
        n_trials_L_tot += n_trials_L
        n_trials_Z_tot += n_trials_Z
        n_trials_R = 0
        n_trials_L = 0
        n_trials_Z = 0


    print('---------------------------------------------------')
    print('Total right hand trials: ' + str(n_trials_R_tot))
    print('Total left hand trials: ' + str(n_trials_L_tot))
    print('Total rest trials: ' + str(n_trials_Z_tot))
    print('Total trials: ' + str((n_trials_R_tot + n_trials_L_tot + n_trials_Z_tot)))
    print('Total samples: ' + str((n_trials_R_tot + n_trials_L_tot + n_trials_Z_tot)*4))
    print('Total fuck ups: ' + str(other))
    print('---------------------------------------------------')
trial_info()


def epoch_data(data, between_boo):
    epoched_data = np.zeros((8, 1))

    if between_boo:
        inc = 125
    else:
        inc = 250

    start = 0
    end = 250
    while (end <= data.shape[1]):
        window = data[:, start:end]
        epoched_data = np.hstack((epoched_data, window))
        # print(epoched_data)

        start += inc
        end += inc

    return epoched_data[:, 1:]


def get_data():
    R_stack = np.zeros((8, 1))
    L_stack = np.zeros((8, 1))
    Z_stack = np.zeros((8, 1))

    for i in range(len(file_dirs)):
        directory = os.getcwd() + '/' + file_dirs[i]
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                if filename.startswith("R"):
                    df = pd.read_csv(str(os.path.join(directory, filename)), index_col=0)
                    df = df.to_numpy()
                    R_stack = np.hstack((R_stack, epoch_data(df, True)))
                if filename.startswith("L"):
                    df = pd.read_csv(str(os.path.join(directory, filename)), index_col=0)
                    df = df.to_numpy()
                    L_stack = np.hstack((L_stack, epoch_data(df, True)))
                if filename.startswith("Z"):
                    df = pd.read_csv(str(os.path.join(directory, filename)), index_col=0)
                    df = df.to_numpy()
                    Z_stack = np.hstack((Z_stack, epoch_data(df, True)))
            else:
                continue

    return R_stack[:, 1:], L_stack[:, 1:], Z_stack[:, 1:]


R_stack, L_stack, Z_stack = get_data()
print(R_stack.shape)
print("Trials: ", R_stack.shape[1]/250)
pd.DataFrame(R_stack).to_csv("data_R.csv")
print(L_stack.shape)
print("Trials: ", L_stack.shape[1]/250)
pd.DataFrame(L_stack).to_csv("data_L.csv")
print(Z_stack.shape)
print("Trials: ", Z_stack.shape[1]/250)
pd.DataFrame(Z_stack).to_csv("data_Z.csv")
