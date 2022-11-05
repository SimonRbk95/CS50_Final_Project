import csv
import gzip
import shutil
import os
import googleapiclient.discovery
import googleapiclient.errors

from os.path import exists


# input txt file name without extension
def read_txt(file):
    if not exists(f'static/{file}.txt'):
        with gzip.open(f'static/{file}.txt.gz', 'rb') as f_in:
            with open(f'static/{file}.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            f_out.close()
    contents = []
    with open(f'static/{file}.txt', newline="") as f_out:
        reader = csv.DictReader(f_out, delimiter="\t")
        for row in reader:
            contents.append(dict(row))
        return contents


# input csv file name without extension
def read_csv(file):
    contents = []
    with open(f"static/{file}.csv") as f_out:
        reader = csv.DictReader(f_out)
        for row in reader:
            contents.append(row)
        return contents


def append_dict_cdb(dict, courses):
    courses.append({
        "Course Name": dict["Product Name"],
        "URL": dict["Product URL"],
        "Partner": dict["Manufacturer"],
        "Image URL": dict["Image URL"],
        "Current Price": dict["Current Price"],
        "Product Description": dict["Product Description"],
        # hard code the product type for courses that are not in cdb100 as they are most likely of type "course"
        "Product Type": "Standalone Course",
    })
    return courses


def append_dict_cdb100(dict, courses, cdb):
    courses.append({
        "Course Name": dict["Product Name"],
        "URL": dict["URL"],
        "Partner": dict["Partner"],
        "Product Type": dict["Product Type"],
    })
    # get further data for chosen courses from cdb
    for dict in cdb:
        # keep track of at which index the list element, the dictionary called 'course', is
        i = 0
        for course in courses:
            if dict["Product Name"] == course["Course Name"]:
                # courses[i]["URL"] = dict["Short Link"]
                courses[i]["Image URL"] = dict["Image URL"]
                courses[i]["Current Price"] = dict["Current Price"]
                courses[i]["Product Description"] = dict["Product Description"]
                # courses[i]["SKU"] = dict["Unique Merchant SKU"]
            i += 1
    return courses


def check_duplicates(courses, dict):
    return any(course["Course Name"] == dict["Product Name"] for course in courses)


def condition_coursera(dict, courses, keywords_q3, index, max_courses, cdb100=None):
    # look for a match in cdb100
    if cdb100:
        if any(n in dict["Product Name"] or n in dict["Primary Domain"] or n in dict["Primary Subdomain"] for n in keywords_q3[int(index)]) and not check_duplicates(courses, dict) and len(courses) < max_courses:
            return True
    # look for a match in cdb
    else:
        if any(n in dict["Product Name"] for n in keywords_q3[int(index)]) and not check_duplicates(courses, dict) and len(courses) < max_courses:
            return True


# requires cdb100 or cdb database as a list of dictionaries
def check_all_courses(courses, index, keywords_q3, max_courses, List_q4=None, cdb100=None, cdb=None):
    # append professional certificates first if get a new job is the goal
    # check if we are searching the cdb100 to use appropriate searches
    if cdb100:
        if "0" in List_q4:
            for dict in cdb100:
                if condition_coursera(dict, courses, keywords_q3, index, max_courses, True) and dict["Product Type"] == "Professional Certificate":
                    courses = append_dict_cdb100(dict, courses, cdb)
        for dict in cdb100:
            if condition_coursera(dict, courses, keywords_q3, index, max_courses, True):
                courses = append_dict_cdb100(dict, courses, cdb)
    # in big data base search only for matches in product name
    # match is checked in app.py
    else:
        for dict in cdb:
            if condition_coursera(dict, courses, keywords_q3, index, max_courses):
                courses = append_dict_cdb(dict, courses)
    return courses


def YT_lookup(course, maxResults):
    """Look up quote for symbol."""
    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get("API_KEY")
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)
    request = youtube.search().list(
        part="id,snippet",
        type='video',
        q=course,
        videoDuration='medium',
        videoDefinition='high',
        maxResults=maxResults,
        relevanceLanguage="en",
        # videoEmbeddable="true",
        # ~order="viewCount",
        # fields="items(id(videoId),snippet(title,description,thumbnails))"
        fields="items(id(videoId))"
    )

    # contact api
    try:
        response = request.execute()
    except googleapiclient.errors.HttpError:
        return None

    # parse response
    YT_data = []
    for i in range(maxResults):
        YT_data.append({
            "videoId": response["items"][i]["id"]["videoId"],
            # "title": response["items"][i]["snippet"]["title"],
            # "thumbnail": response["items"][i]["snippet"]["thumbnails"]["medium"]["url"],
            # "description": response["items"][i]["snippet"]["description"],
        })
    return YT_data

