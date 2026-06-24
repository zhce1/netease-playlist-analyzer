#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网易云音乐歌单数据获取脚本
用法: python fetch_playlist.py <playlist_id> <output_path>
"""
import urllib.request
import urllib.parse
import json
import time
import sys
import re


def extract_playlist_id(url_or_id):
    """从链接或纯ID中提取歌单ID"""
    if url_or_id.isdigit():
        return url_or_id
    match = re.search(r'[?&]id=(\d+)', url_or_id)
    if match:
        return match.group(1)
    match = re.search(r'/playlist/(\d+)', url_or_id)
    if match:
        return match.group(1)
    match = re.search(r'(\d{6,})', url_or_id)
    if match:
        return match.group(1)
    return url_or_id


def fetch_playlist(playlist_id, output_path):
    """获取歌单完整数据"""
    # Step 1: 获取歌单所有歌曲ID
    url = f"https://music.163.com/api/v6/playlist/detail?id={playlist_id}&n=0&s=0"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://music.163.com/'
    })

    print(f"正在获取歌单 {playlist_id} 的歌曲列表...")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

    if data.get('code') != 200:
        print(f"错误: API返回 code={data.get('code')}, msg={data.get('msg','')}")
        sys.exit(1)

    playlist = data['playlist']
    track_ids = [t['id'] for t in playlist['trackIds']]
    add_time_map = {t['id']: t.get('at', 0) for t in playlist['trackIds']}
    playlist_name = playlist.get('name', '未知歌单')
    print(f"歌单名称: {playlist_name}")
    print(f"总歌曲数: {len(track_ids)}")

    # Step 2: 分批获取歌曲详情
    all_songs = []
    batch_size = 200

    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(track_ids) - 1) // batch_size + 1
        print(f"  获取第 {batch_num}/{total_batches} 批 ({len(batch)} 首)...")

        ids_param = '[' + ','.join(str(x) for x in batch) + ']'
        post_data = urllib.parse.urlencode({'ids': ids_param}).encode()

        detail_url = "https://music.163.com/api/song/detail"
        req2 = urllib.request.Request(detail_url, data=post_data, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Referer': 'https://music.163.com/',
            'Content-Type': 'application/x-www-form-urlencoded'
        })

        try:
            with urllib.request.urlopen(req2, timeout=30) as resp:
                raw = resp.read().decode()
                detail_data = json.loads(raw)

            if detail_data.get('code') == 200:
                songs = detail_data.get('songs', [])
                all_songs.extend(songs)
                print(f"    成功获取 {len(songs)} 首 (累计: {len(all_songs)})")
            else:
                print(f"    错误: code={detail_data.get('code')}")
        except json.JSONDecodeError:
            try:
                idx = raw.index('}{')
                first_json = raw[:idx+1]
                detail_data = json.loads(first_json)
                if detail_data.get('code') == 200:
                    songs = detail_data.get('songs', [])
                    all_songs.extend(songs)
                    print(f"    分割后获取 {len(songs)} 首 (累计: {len(all_songs)})")
            except Exception:
                print(f"    JSON解析失败，跳过该批次")
        except Exception as e:
            print(f"    异常: {e}")

        time.sleep(0.8)

    # Step 3: 构建最终数据集
    final_data = []
    for song in all_songs:
        song_id = song.get('id')
        artists_field = song.get('ar', song.get('artists', []))
        artists = [a.get('name', '') for a in artists_field] if artists_field else []
        album_info = song.get('al', song.get('album', {}))

        final_data.append({
            'id': song_id,
            'name': song.get('name', ''),
            'artists': ' / '.join(artists),
            'album': album_info.get('name', '') if album_info else '',
            'duration_ms': song.get('dt', song.get('duration', 0)),
            'added_at': add_time_map.get(song_id, 0),
            'publish_time': song.get('publishTime', 0),
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成! 保存了 {len(final_data)} 首歌曲到 {output_path}")
    print(f"   覆盖率: {len(final_data)}/{len(track_ids)} ({100*len(final_data)//max(len(track_ids),1)}%)")
    return final_data


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python fetch_playlist.py <歌单链接或ID> <输出文件路径>")
        sys.exit(1)

    raw_input = sys.argv[1]
    output = sys.argv[2]
    pid = extract_playlist_id(raw_input)
    fetch_playlist(pid, output)
