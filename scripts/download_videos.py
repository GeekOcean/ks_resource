import os
import requests
import time
import json


def get_url(url):
    """TODO: Docstring for function.

    :function: TODO
    :returns: TODO

    """
    urllist = []
    while True:
        try:
            data = requests.get(url)
            data = data.json()
            urllist = []
            i = 0
            while (i < len(data)):
                urllist.append([data[i]['mp4Url']])
                i = i + 1
            return urllist
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 3 seconds')
            time.sleep(3)
        except:
            print(
                'Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds'
            )
            time.sleep(3)


def get_link_sum(url_txt_folder, cdn_txt_path, link_sum):
    """TODO: Docstring for get_link_sum.

    :function: TODO
    :returns: TODO

    """
    link_dict = {}
    if (not os.path.exists(url_txt_folder)):
        os.mkdir(url_txt_folder)
    else:
        with open(cdn_txt_path, 'r') as f:
            link_dict = json.load(f)
            # print(type(link_dict))
            link_dict = json.loads(link_dict)
            # print(type(link_dict))
            f.close()
        link_sum = len(link_dict)
    return link_sum


def write_to_file(urllist, url_txt_folder, url_txt_path):
    """TODO: Docstring for write_to_file.

    :function: TODO
    :returns: TODO

    """
    # print("Current folder: ", os.getcwd())
    if (not os.path.exists(url_txt_folder)):
        os.mkdir(url_txt_folder)
    with open(url_txt_path, 'w+') as f:
        for url in urllist:
            f.write(url[0])
            f.write('\n')
        f.close()


def download_videos(videos_path, videos_download_every):
    """TODO: Docstring for download_videos.

    :function: TODO
    :returns: TODO

    """
    # print(os.getcwd())
    # create videos folder
    if (not os.path.exists(videos_path)):
        os.mkdir(videos_path)
    os.chdir(videos_path)
    link_dict = {}
    res = 0
    count = 0
    dir_num = len([
        lists for lists in os.listdir(videos_path)
        if os.path.isdir(os.path.join(videos_path, lists))
    ])
    link_addr = 'https://cdn.jsdelivr.net/gh/liuyaanng/douyin_resource@master/txt/ks.json'
    link_res = requests.get(link_addr)
    link_dict = json.loads(json.loads(link_res.text))
    # with open(url_txt_path, 'r') as f:
    #     link_dict = json.load(f)
    #     link_dict = json.loads(link_dict)
    while (count < videos_download_every):
        print('start download')
        count += 1
        try:
            link = link_dict[dir_num + count]['url']
            res = requests.get(link)
            if (res.status_code == 200):
                dir_num += 1
                videopath_name = 'v' + str(dir_num)
                videoname = 'ks' + str(dir_num) + '.mp4'
                if (not os.path.exists(videopath_name)):
                    os.mkdir(videopath_name)
                os.chdir(videopath_name)
                os.system("ffmpeg -y -i %s %s" % (link, videoname))
                print('download %s videos' % dir_num)
                os.chdir('../')
        except requests.exceptions.ConnectionError:
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            print('ChunkedEncodingError -- please wait 3 seconds')
            time.sleep(3)
        except:
            print(
                'Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds'
            )
            time.sleep(3)


def to_m3u8(videos_path):
    """TODO: Docstring for to_m3u8.

    :function: TODO
    :returns: TODO

    """
    name_after = '.mp4'
    os.chdir(videos_path)
    g = os.walk(videos_path)
    for path, dir_list, filenames in g:
        for filename in filenames:
            if (os.path.splitext(filename)[1] == name_after):
                os.chdir(path)
                filename_pre = os.path.splitext(filename)[0]
                tsname_pre = filename_pre + '_'
                # print('deal with %s' % filename_pre)
                os.system(
                    'ffmpeg -y -i %s.mp4 -profile:v baseline -level 3.0  -start_number 0 -hls_time 5 -hls_list_size 0 -f hls %s.m3u8'
                    % (filename_pre, tsname_pre))
                os.system('trash %s' % filename)
                os.chdir('../')
        # print("del %s" % filename)
    print("to m3u8 success!")


def generate_cdn_link(url_txt_folder, cdn_txt_name, videos_path, cdn_link_pre):
    """TODO: Docstring for generate_cdn_link.

    :function: TODO
    :returns: TODO

    """
    u3m8_names = []
    name_after = '.m3u8'
    link_sum = 0
    videos_dir = []
    for root, dirs, files in os.walk(videos_path):
        for dir in dirs:
            videos_dir.append(dir)
        for file in files:
            if (os.path.splitext(file)[1] == name_after):
                name_dict = {}
                link_sum += 1
                name_dict['id'] = link_sum
                name_dict['url'] = cdn_link_pre + root.split(
                    '/')[-1:][0] + '/' + file
                u3m8_names.append(name_dict)
    cdn_link_path = url_txt_folder + cdn_txt_name
    json_u3m8_names = json.dumps(u3m8_names)
    # print(json_u3m8_names)
    # print(type(json_u3m8_names))
    if (not os.path.exists(url_txt_folder)):
        os.mkdir(url_txt_folder)
    with open(cdn_link_path, 'w+') as f:
        json.dump(json_u3m8_names, f)
        f.close()
    # with open(cdn_link_path, 'a+') as f:
    # for u3m8_name in u3m8_names:
    # f.write(u3m8_name)
    # f.write('\n')
    # f.close
    print("generate cdn link success!")
    return link_sum


def push_to_github(root, videos_sum):
    """TODO: Docstring for push_to_github.

    :function: TODO
    :returns: TODO

    """
    os.chdir(root)
    os.system("git add .")
    os.system("git commit -m \'add videos\'")
    os.system("git push")
    print("Push success, there are %d videos!" % videos_sum)
