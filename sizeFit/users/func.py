from .models import UsersInput, NormTable, Brand, Size_by_brand, StdTable
from .models import FemalePants, FemaleShirts, MalePants, MaleShirts
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances
from .scrapping import *


#my_dict = {"S": [90,95], "M": [95,100], "L": [100,105], "XL": [105,110]}
#my_dict = {'XXS': [72, 80], 'XS': [80, 88], 'S': [88, 96], 'M': [96, 104], 'L': [104, 112], 'XL': [112, 124], 'XXL': [124, 136], 'XXXL': [136, 148]}
SIZE_LABELS = {'XXS': 0, 'XS': 1, 'S': 2, 'M': 3, 'L': 4, 'XL': 5, 'XXL': 6, 'XXXL': 7}
FIT_LABELS = {'Tight': 0, 'Slightly Tight': 1, 'Average': 2, 'Slightly Loose': 3, 'Loose': 4}
TUMMY_LABELS = {'Flatter': 0, 'Average': 1, 'Curvier': 2}

def one_hot(df):
    df = pd.concat([df,pd.get_dummies(df["brand"], prefix='brand')], axis=1)
    df.drop('brand', axis=1, inplace=True)
    return df

def label_encoding(df):
    df['size_labels'] = df['size'].map(SIZE_LABELS)
    df['fit_labels'] = df['fit_preference'].map(FIT_LABELS)
    df['tummy_labels'] = df['tummy_shape'].map(TUMMY_LABELS)
    df.drop(columns=['size','gender','tummy_shape','fit_preference'], inplace=True)
    return df

def min_max_norm(df, user = None):
    scaler = MinMaxScaler()
    features = df.columns.tolist()
    if not isinstance(user, pd.DataFrame):
        scaled_values = scaler.fit_transform(df.values.tolist())
        return pd.DataFrame(scaled_values,columns = features).astype(np.float64)
    else:
        scaler.fit(df.values.tolist())
        user_norm = scaler.transform(user.values.tolist())
        return user_norm, scaler

def reverse_norm(scaler, vector):
    reverse = scaler.inverse_transform(np.reshape(vector, (1, -1)))
    return reverse


def k_means(df, gender, item, clusters= 8):
  cluster_centroids = {}
  cluster_std = {}
  kmeans = KMeans(n_clusters = clusters)
  pred = kmeans.fit_predict(df.astype(np.float64))
  df['cluster'] = pred

  if gender == "male":
      if item == "t-shirt":
          data = list(MaleShirts.objects.all().values())
      else:
          data = list(MalePants.objects.all().values())
  elif gender == "female":
        if item == "t-shirt":
            data = list(FemaleShirts.objects.all().values())
        else:
            data = list(FemalePants.objects.all().values())
  table = pd.DataFrame(data)
  table.set_index('id', inplace = True)

  for cluster in range(clusters):
    inx = df[df['cluster'] == cluster].index
    users = table.loc[inx]
    weight, age, height = users.std(axis=0)[0:3]
    cluster_std[cluster] = {'weight': weight, 'age': age, 'height': height}

  for cluster,vector in enumerate(kmeans.cluster_centers_):
    #cluster_centroids[cluster] = np.around(vector.tolist(), decimals = 3)
    cluster_centroids[cluster] = list(np.around(np.array(vector.tolist()),4))
  return cluster_centroids, cluster_std



def insert_into_norm(table, gender, item):
    data = list(table.objects.all().values())
    df = pd.DataFrame(data)

    df.set_index('id', inplace = True)
    user_indx = df.index.to_numpy()

    norm_data = one_hot(df)
    norm_data = label_encoding(norm_data)
    norm_data = min_max_norm(norm_data)

    norm_data.set_index(user_indx, inplace = True)
    norm_data, cluster_std = k_means(norm_data, gender, item)
    #print(norm_data)

    for center, fields in norm_data.items():
        #print(fields)
        norm_table = NormTable(
           gender = "F" if gender == "female" else "M",
           item = "T-shirt" if item == "t-shirt" else "Pants",
           cluster = center,
           weight = fields[0],
           age = fields[1],
           height = fields[2],
           chest_lower = fields[3] if item == "t-shirt" else 0,
           chest_top = fields[4] if item == "t-shirt" else 0,
           waist_lower = fields[3] if item == "pants" else 0,
           waist_top = fields[4] if item == "pants" else 0,
           brand_ASOS = fields[5],
           brand_HM = fields[6],
           brand_PULL_BEAR = fields[7],
           brand_ZARA = fields[8],
           size_labels = fields[9],
           fit_labels = fields[10],
           tummy_labels = fields[11],
           )
        norm_table.save()

    for center, fields in cluster_std.items():
        #print(fields)
        std_table = StdTable(
           gender = "F" if gender == "female" else "M",
           item = "T-shirt" if item == "t-shirt" else "Pants",
           cluster = center,
           weight = fields['weight'],
           age = fields['age'],
           height = fields['height'],
           )
        std_table.save()

def Find_Table(user):
    if user.loc[0, 'gender'] == 'M':
        if user.loc[0, "item"] == "T-shirt":
            table = list(MaleShirts.objects.all().values())
        else:
            table = list(MalePants.objects.all().values())
    else:
        if user.loc[0, "item"] == "T-shirt":
            table = list(FemaleShirts.objects.all().values())
        else:
            table = list(FemalePants.objects.all().values())
    return table

def Manual_One_Hot(df):
    brands = list(Brand.objects.all().values())
    for i in brands:
        brand = " ".join(i.values())
        if df.loc[0, "brand"] == brand:
            df["brand_"+brand] = 1
        else:
            df["brand_"+brand] = 0

    df.drop('brand', axis=1, inplace=True)
    return df

def get_size(df):
    query = Size_by_brand.objects.filter(brand_name = df.loc[0, "brand"], item_name = df.loc[0, "item"], size_name = df.loc[0, "size"])
    if df.loc[0, "item"] == "T-shirt":
        df[["chest_lower", "chest_top"]] = query.values()[0]['chest'].split("-")
    else:
        df[["waist_lower", "waist_top"]] = query.values()[0]['waist'].split("-")
    df.drop("item", axis = 1, inplace = True)
    return df

def Group_Divide(u_gender, u_item):
    groups = list(NormTable.objects.filter(gender = u_gender, item = u_item ).values())
    new_groups = list()
    if u_item == "T-shirt":
        for group in groups:
            group.pop("waist_lower")
            group.pop("waist_top")
            new_groups.append({list(group.values())[1]: list(group.values())[4::]})
    else:
        for group in groups:
            group.pop("chest_lower")
            group.pop("chest_top")
            new_groups.append({list(group.values())[1]: list(group.values())[4::]})
    return new_groups


def reresentive_vector(group_vec, user_vec, item):
    vec = np.concatenate((group_vec,user_vec), axis= 0)
    #print(vec)
    if item == "T-shirt":
        #print(np.mean(vec, axis= 0))
        chest_lower, chest_top = np.mean(vec, axis= 0)[3:5]
        return np.round([chest_lower, chest_top],2)
    else:
        waist_lower, waist_top = np.mean(vec, axis= 0)[3:5]
        return np.round([waist_lower, waist_top],2)


def find_similar_users(user_vector, users_group):
  dist = []
  print(user_vector)
  print(users_group)
  for group in users_group:
    values = [*group.values()][0]
    cluster = [*group.keys()][0]
    dst = distance.euclidean(user_vector, values)
    dist.append([values, dst, cluster])
  #similar_group = min(dist.items(), key=lambda x: x[1])
  dist.sort(key = lambda tup: tup[1])
  print("dist0", dist[0] )
  return dist[0]
#[ 96.18 100.18 180]
#my_dict = {"S": [90,95], "M": [95,100], "L": [100,105], "XL": [105,110]}
# def size_similarity(user_vec, size_dict):
#     similar_size = {}
#     for size, interval in size_dict.items():
#         similar_size[size] = cosine_similarity(np.reshape(user_vec, (1,-1)), np.reshape(interval,(1, -1)))
#     return max(similar_size.items(), key = lambda x: x[1])
#     #return similar_size

def size_similarity(user_vec, size_dict):
    lower_bound, upper_bound = user_vec
    length = upper_bound - lower_bound
    similar_sizes = {}

    for size, rng in size_dict.items():
      # print(size,':',inter[0], inter[1])
      if (lower_bound >= rng[0]) and (upper_bound <= rng[1]):
        return {size:100}
      if (lower_bound < rng[0]) and (upper_bound > rng[1]):
        return {size:100}
      if lower_bound > rng[1]:
        continue
      if upper_bound < rng[0]:
        continue
      if (lower_bound >= rng[0]) and (lower_bound < rng[1]):
          similar_sizes[size] = ((rng[1] - lower_bound) / length) * 100
      else:
         similar_sizes[size] = ((upper_bound - rng[0]) / length) * 100

    return dict(sorted(similar_sizes.items(), key=lambda item: item[1], reverse=True))


def rmse(user_vec, group_vec):
    # y_hat = np.array([54.91,32.96,163.71,92.56,97.56,1,0,0,0,2.31, 0.95,0.48])
    # y_true = np.array([50,27,220,71,76, 1,0,0,0,1,4,2])
    differences = abs(user_vec - group_vec)
    differences_squared = differences ** 2
    mean_of_differences_squared = differences.mean()
    rmse_val = np.sqrt(mean_of_differences_squared)
    return rmse_val
#print("d is: " + str(["%.4f" % elem for elem in y_hat]))
#print("p is: " + str(["%.4f" % elem for elem in y_true]))
def get_std_cluster(u_gender, u_item, num_cluster):
    std_cluster = list(StdTable.objects.filter(gender = u_gender, item = u_item, cluster = num_cluster).values())[0]
    return std_cluster

def check_std(user_vector, group_vector, std):
    #group_norm = list(StdTable.objects.filter(gender = u_gender, item = u_item, cluster = int(num_cluster)).values())[0]
    #group = reverse_norm(scaler, group_norm)
    # if u_item == "T-shirt":
    #         group_norm.pop("waist_lower")
    #         group_norm.pop("waist_top")
    # else:
    #         group_norm.pop("chest_lower")
    #         group_norm.pop("chest_top")
    std_weigt = int(np.round(std['weight']))
    std_height = int(np.round(std['height']))
    user_weight = int(user_vector[0][0])
    user_height = int(user_vector[0][2])
    group_weight = int(np.round(group_vector[0][0]))
    group_height = int(np.round(group_vector[0][2]))
    print("weight:", group_weight - 2 * std_weigt, group_weight + 2 * std_weigt)
    print("height:", group_height - 2 * std_height, group_height + 2 * std_height)
    if user_weight not in range(group_weight - 2 * std_weigt, group_weight + 2 * std_weigt):
        return False
    if user_height not in range(group_height - 2 * std_height, group_height + 2 * std_height):
        return False
    return True

    # print(std_weigt, group_vector, group_height)
    # norm_std_vec = list(group_norm.values())[4::]
    # print(norm_std_vec)
    # std_vec = reverse_norm(scaler, norm_std_vec)
    # return std_vec


def Find_My_Size(user_in_process, url):
    df_user = pd.DataFrame(user_in_process, index = [0])
    table = Find_Table(df_user)
    df_users = pd.DataFrame(table)
    #df_users.drop('id', axis = 1, inplace = True)
    df_users.set_index('id', inplace = True)


    user_gender = df_user.loc[0, "gender"]
    user_item = df_user.loc[0, "item"]

    df_user = get_size(df_user)


    df_users = one_hot(df_users)
    df_user = Manual_One_Hot(df_user)


    df_users = label_encoding(df_users)
    df_user = label_encoding(df_user)


    user_norm, scaler = min_max_norm(df_users, df_user)
    user_groups = Group_Divide(user_gender, user_item)
    similar_users, dist, cluster = find_similar_users(user_norm, user_groups)
    print("similar_group", similar_users)
    print("cluster", cluster)
    #print("---------------------")
    group_vector = reverse_norm(scaler, similar_users)
    user_vector = reverse_norm(scaler, user_norm)
    print("group_vector:", group_vector)
    print("user_vector:", user_vector)


    #rmse_val = rmse(group_vector, user_vector)
    std = get_std_cluster(user_gender, user_item, cluster)
    check_std(user_vector, group_vector, std)
    if check_std(user_vector, group_vector, std):
            rep_vector = reresentive_vector(group_vector, user_vector, user_item)
            print("in range")
    else:
            rep_vector = reresentive_vector(user_vector, user_vector, user_item)
            print("not in range")
    print("---------------------")
    print("rep vector:", rep_vector)
    scraping_size_dict = scraping(url)
    print("------")
    print("scrapping:", scraping_size_dict)
    # if not scraping_size_dict():
    #     retuen False
    return size_similarity(rep_vector, scraping_size_dict)
