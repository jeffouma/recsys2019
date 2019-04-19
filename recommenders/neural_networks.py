import data
import pandas as pd
from tqdm.auto import tqdm

tqdm.pandas()
import numpy as np
from functools import reduce
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import class_weight

pd.options.display.max_columns = None
from keras.callbacks import EarlyStopping
from recommenders.recommender_base import RecommenderBase

import utils.check_folder as check_folder
from keras import metrics
import keras.optimizers
from keras import Sequential
from keras import regularizers
from keras.layers import Dense, Dropout
import out
from sklearn.model_selection import train_test_split


class NeuralNetworks(RecommenderBase):

    def __init__(self, mode, cluster, nn_dict_params):
        name = 'NeuralNetwork_2'
        super(NeuralNetworks, self).__init__(mode=mode, cluster=cluster, name=name)

        self.nn_dict_params = nn_dict_params
        self.dataset_name = nn_dict_params['dataset_name']
        base_path_dataset = f'dataset/preprocessed/neural_network_dataset/{cluster}/{mode}/{self.dataset_name}'

        self.X_train = np.load(f'{base_path_dataset}/X_train.npy')
        self.Y_train = np.load(f'{base_path_dataset}/Y_train.npy')

        self.X_val = np.load(f'{base_path_dataset}/X_val.npy')
        self.Y_val = np.load(f'{base_path_dataset}/Y_val.npy')

        self.class_weights_dict = None
        self._compute_class_weights()
        self._create_model()

    def _compute_class_weights(self):
        temp = np.concatenate((self.Y_train, self.Y_val))
        #class_weights = class_weight.compute_class_weight('balanced', np.unique(temp), temp)

        class_weights_dict = {
            0: 1,
            1: (len(temp)-np.sum(temp))/np.sum(temp),
        }
        self.class_weights_dict=class_weights_dict


    def fit(self):
        callback = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=0, mode='auto', baseline=None,
                                 restore_best_weights=True)
        self.model.fit(self.X_train, self.Y_train, validation_data=(self.X_val, self.Y_val),
                       epochs=self.nn_dict_params['epochs'],
                       batch_size=self.nn_dict_params['batch_size'],
                       shuffle=True,
                       class_weight=self.class_weights_dict)

    def recommend_batch(self):
        base_path = f'dataset/preprocessed/neural_network_dataset/{self.cluster}/{self.mode}/{self.dataset_name}'
        X = np.load(f'{base_path}/X_test.npy')
        target_indeces = np.load(f'{base_path}/target_indeces.npy')
        print(target_indeces)

        predictions = self.model.predict(X)

        final_predictions = []

        count = 0
        accumulator = 0
        for index in tqdm(target_indeces):
            impr = list(map(int, data.full_df().loc[index]['impressions'].split('|')))
            pred = predictions[accumulator:accumulator + len(impr)]
            accumulator += len(impr)
            couples = list(zip(pred, impr))
            couples.sort(key=lambda x: x[0], reverse=True)
            _, sorted_impr = zip(*couples)
            final_predictions.append((index, list(sorted_impr)))
            count += 1

        return final_predictions

    def get_scores_batch(self):
        pass

    def _create_model(self):
        model = Sequential()
        model.add(Dense(self.nn_dict_params['neurons_per_layer'], input_dim=self.X_train.shape[1],
                        activation=self.nn_dict_params['activation_function_internal_layers']))
        model.add(Dense(self.nn_dict_params['neurons_per_layer'],
                        activation=self.nn_dict_params['activation_function_internal_layers']))
        model.add(Dense(1, activation='sigmoid'))

        # compile the model
        model.compile(loss=self.nn_dict_params['loss'], optimizer=self.nn_dict_params['optimizer'],
                      metrics=['accuracy'])
        self.model = model
        print('model created')


def is_target(df, tgt_usersession):
    if tuple(df.head(1)[['user_id', 'session_id']].values[0]) in tgt_usersession:
        return True
    else:
        return False


def create_dataset_for_neural_networks(mode, cluster, features_array, dataset_name):
    # path in which the computed dataset will be stored
    SAVE_PATH = f'dataset/preprocessed/neural_network_dataset/{cluster}/{mode}/{dataset_name}'
    check_folder.check_folder(SAVE_PATH)

    READ_FEATURE_PATH = f'dataset/preprocessed/{cluster}/{mode}/feature'

    """
    RETRIEVE THE FEATURES
    """
    ################################################

    # list of pandas dataframe each element represent a feature
    pandas_dataframe_features_session_list = []
    for f in features_array['session']:
        pandas_dataframe_features_session_list.append(pd.read_csv(f'{READ_FEATURE_PATH}/{f}/features.csv'))

    # merge all the dataframes
    df_merged_session = reduce(lambda left, right: pd.merge(left, right, on=['user_id', 'session_id'],
                                                    how='inner'), pandas_dataframe_features_session_list)

    pandas_dataframe_features_item_list = []
    for f in features_array['item_id']:
        pandas_dataframe_features_item_list.append(pd.read_csv(f'{READ_FEATURE_PATH}/{f}/features.csv'))

    # merge all the dataframes
    df_merged_item = reduce(lambda left, right: pd.merge(left, right, on=['user_id', 'session_id', 'item_id'],
                                                            how='inner'), pandas_dataframe_features_item_list)

    df_merged = pd.merge(df_merged_item, df_merged_session, on=['user_id', 'session_id'])
    ################################################


    # load the target indeces of the mode
    target_indeces = data.target_indices(mode, cluster)

    # load the full df
    full_df = data.full_df()

    # dict that has as keys the couples (user_id, session_id) that are target
    tgt_usersession = {}
    for index in target_indeces:
        tgt_usersession[tuple(full_df.iloc[index][['user_id', 'session_id']].values)] = index

    is_target_ = df_merged.groupby(['user_id', 'session_id']).progress_apply(is_target, tgt_usersession=tgt_usersession)
    df_merged = pd.merge(df_merged, is_target_.reset_index(), on=['user_id', 'session_id'])

    test_df = df_merged[df_merged[0]==True]
    train_df = df_merged[df_merged[0]==False]

    train_df.drop(columns=[0], inplace=True)
    test_df.drop(columns=[0], inplace=True)

    # retrieve the target indeces in the right order
    couples_dict = {}
    couples_arr = test_df[['user_id', 'session_id']].values
    for c in couples_arr:
        if tuple(c) not in couples_dict:
            couples_dict[tuple(c)] = 1

    target_us_reordered = list(couples_dict.keys())

    target_indeces_reordered = []
    for k in target_us_reordered:
        target_indeces_reordered.append(tgt_usersession[k])

    target_indeces_reordered = np.array(target_indeces_reordered)

    """
    CREATE DATA FOR TRAIN

    """
    # the 5 column is the label
    X, Y = train_df.iloc[:, 4:], train_df['label']
    scaler = MinMaxScaler()
    # normalize the values
    X_norm = scaler.fit_transform(X)
    Y_norm = Y.values

    X_train, X_val, Y_train, Y_val = train_test_split(X_norm, Y_norm, test_size=0.2, shuffle=True)

    X_test = test_df.iloc[:, 4:]
    X_test_norm = scaler.fit_transform(X_test)

    print('saving training data...')
    np.save(f'{SAVE_PATH}/X_train', X_train)
    np.save(f'{SAVE_PATH}/X_val', X_val)
    print('done')

    print('saving labels...')
    np.save(f'{SAVE_PATH}/Y_train', Y_train)
    np.save(f'{SAVE_PATH}/Y_val', Y_val)
    print('done')

    print('saving test data...')
    np.save(f'{SAVE_PATH}/X_test', X_test_norm)
    np.save(f'{SAVE_PATH}/target_indeces', target_indeces_reordered)
    print('done')


if __name__ == '__main__':
    features = {
        'item_id': ['impression label', 'impression_position_session', 'impression_price_info_session'],
        'session': ['session_length'],
    }
    dataset_name = 'prova'
    create_dataset_for_neural_networks('small', 'no_cluster', features, dataset_name)

    nn_dict_params = {
        'dataset_name': 'prova',
        'activation_function_internal_layers': 'relu',
        'neurons_per_layer': 128,
        'loss': 'binary_crossentropy',
        'optimizer': 'adam',
        'validation_split': 0.2,
        'epochs': 10,
        'batch_size': 256,
    }

    model = NeuralNetworks(mode='small', cluster='no_cluster', nn_dict_params=nn_dict_params)
    model.evaluate()

    # out.create_sub(recs, 'prova')







