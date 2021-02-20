import download_videos as dv


def ks():
    """TODO: Docstring for ks.

    :function: TODO
    :returns: TODO

    """
    root = "/root/GeekOcean/ks_resource/"
    url_txt_folder = root + 'txt/'
    url_txt_name = 'ks.txt'
    cdn_txt_name = 'ks.json'
    url_txt_path = url_txt_folder + url_txt_name
    cdn_txt_path = url_txt_folder + cdn_txt_name
    videos_path = root + 'videos'
    cdn_link_pre = 'https://cdn.jsdelivr.net/gh/GeekOcean/ks_resource@master/videos/'
    videos_download_every = 20
    dv.download_videos(videos_path, videos_download_every)
    dv.to_m3u8(videos_path)
    videos_sum = dv.generate_cdn_link(url_txt_folder, cdn_txt_name,
                                      videos_path, cdn_link_pre)
    print(videos_sum)
    dv.push_to_github(root, videos_sum)


if __name__ == "__main__":
    while True:
        ks()
        print("Sleep...")
        dv.time.sleep(300)
