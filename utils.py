import requests
import time
import os.path
import subprocess
import numpy as np
import pandas as pd
import pylab as plt
import seaborn as sns
from lxml import html
from pyspark.sql import functions as F


DATA_DIR = "data/"
DATA_ARCHIVE = DATA_DIR + "yelp_dataset_challenge_academic_dataset.tgz"


def download_yelp_dataset(skip_when_exists=True):
    if skip_when_exists and os.path.exists(DATA_ARCHIVE):
        return

    url = "https://www.yelp.de/dataset_challenge/dataset"
    s = requests.Session()
    r = s.get(url)

    # exctract hidden csrf token using lxml
    doc = html.fromstring(r.text)
    form = doc.cssselect("form[name='challenge_dataset_form']")[0]
    inputs = form.cssselect("input")
    csrf_token = inputs[0].value

    # submit form
    post_data = {"csrftok": csrf_token,
                 "name": "Neo York",
                 "email": "neo.york@gmx.net",
                 "school": "",
                 "resume": "",
                 "filename": "",
                 "recruiter_contact": "nothanks",
                 "user_agreement": "True",
                 "initials": "NY"
                 }
    time.sleep(2)
    r = s.post("https://www.yelp.de/dataset_challenge/dataset", post_data)

    # find download button using lxml
    doc = html.fromstring(r.text)
    download_link = None
    for link in doc.cssselect("a"):
        if link.text == 'Download Data':
            download_link = link.get("href")

    # download data archive and write to disc
    time.sleep(3)
    r = s.get(download_link, stream=True)
    with open(DATA_ARCHIVE, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


JSON_FILES = ["yelp_academic_dataset_{}.json".format(x) for x in ["business", "checkin", "review", "tip", "user"]]


def extract_yelp_dataset(skip_when_exists=True):
    json_files_exist = all(os.path.exists(DATA_DIR + f) for f in JSON_FILES)
    if skip_when_exists and json_files_exist:
        return

    subprocess.call(["tar", "xzf", DATA_ARCHIVE, "-C", DATA_DIR])


def count_reviews(df, column, show=True, normalize=True, cumulative=False):
    times_rated = df.groupby(column).count()
    times_rated.cache()

    # define logarithmic bins for making a histogram
    max_times_rated = times_rated.agg(F.max("count")).collect()[0][0]
    bins = np.logspace(0, np.log10(max_times_rated), 20)
    bins = np.array(sorted(set(np.round(bins))))  # only integer bins

    # compute histogram
    _, counts = times_rated.rdd.values().histogram(list(bins))

    if normalize:
        counts = np.array(counts, dtype="float32")
        counts /= np.sum(counts)

    if cumulative:
        counts = np.cumsum(counts)

    if show:
        f, axs = plt.subplots(1, 2, figsize=(8, 3))
        plt.sca(axs[0])
        plt.bar(bins[:-1], counts, width=bins[1:] - bins[:-1])
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("# reviews per {}".format(column))
        plt.ylabel("fraction of {}s".format(column))
        plt.sca(axs[1])
        plt.plot(bins[:-1], np.cumsum(counts))
        plt.xscale("log")
        plt.xlabel("# reviews per {}".format(column))
        plt.ylabel("cumulative fraction of {}s".format(column))
        f.tight_layout()

    return bins, counts


def concat_for_seaborn(scores):
    scores1 = scores.drop("rmse_test", axis=1).rename(columns=dict(rmse_train="rmse"))
    scores1["dataset"] = "train"
    scores2 = scores.drop("rmse_train", axis=1).rename(columns=dict(rmse_test="rmse"))
    scores2["dataset"] = "test"
    return pd.concat([scores1, scores2], ignore_index=True)


def plot_histogram(bins, counts, xlabel, ylabel="fraction", seaborn=True,
                   normalize=True, **kwargs):
    if normalize:
        counts = np.array(counts, dtype="float32")
        counts /= np.sum(counts)
    bins = np.array(bins)

    if seaborn:
        sns.barplot(bins[:-1], counts, **kwargs)
    else:
        plt.bar(bins[:-1], counts, width=bins[1:] - bins[:-1], **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel("fraction")


blue, green, red, purple = sns.color_palette("deep", 10)[0:4]
