#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音乐歌单数据分析脚本
用法: python analyze_playlist.py <playlist_data.json> <output_analysis.json>
"""
import json
import sys
from datetime import datetime
from collections import Counter, defaultdict
import re


def detect_language(name, artists):
    """基于歌名和歌手名推测语言"""
    text = name + ' ' + artists
    has_cjk = bool(re.search(r'[\u4e00-\u9fff]', text))
    has_jp = bool(re.search(r'[\u3040-\u309f\u30a0-\u30ff]', text))
    has_kr = bool(re.search(r'[\uac00-\ud7af]', text))
    has_latin = bool(re.search(r'[a-zA-Z]{3,}', text))

    if has_jp:
        return '日语'
    elif has_kr:
        return '韩语'
    elif has_cjk and not has_latin:
        return '中文'
    elif has_cjk and has_latin:
        return '中文(含英文)'
    elif has_latin and not has_cjk:
        return '英文/欧美'
    else:
        return '其他'


def analyze(input_path, output_path):
    """对歌单数据进行全面分析"""
    with open(input_path, 'r', encoding='utf-8') as f:
        songs = json.load(f)

    print(f"加载歌曲数: {len(songs)}")

    # === 时间维度分析 ===
    year_counts = defaultdict(int)
    year_month_counts = defaultdict(int)
    year_songs = defaultdict(list)

    for song in songs:
        at = song['added_at']
        if at and at > 0:
            dt = datetime.fromtimestamp(at / 1000)
            year = dt.year
            month = dt.month
            year_counts[year] += 1
            year_month_counts[f"{year}-{month:02d}"] += 1
            year_songs[year].append(song)

    # === 歌手分析 ===
    artist_counter = Counter()
    for song in songs:
        for artist in song['artists'].split(' / '):
            artist = artist.strip()
            if artist:
                artist_counter[artist] += 1

    # === 各年份最爱歌手 ===
    year_top_artists = {}
    for year in sorted(year_songs.keys()):
        if year_counts[year] >= 5:
            year_artist_counter = Counter()
            for song in year_songs[year]:
                for artist in song['artists'].split(' / '):
                    artist = artist.strip()
                    if artist:
                        year_artist_counter[artist] += 1
            year_top_artists[str(year)] = year_artist_counter.most_common(10)

    # === 时长分析 ===
    durations = [s['duration_ms'] for s in songs if s['duration_ms'] > 0]
    avg_dur = sum(durations) / len(durations) / 1000 / 60 if durations else 0
    total_dur = sum(durations) / 1000 / 3600 if durations else 0

    dur_ranges = {'<2min': 0, '2-3min': 0, '3-4min': 0, '4-5min': 0, '5-7min': 0, '7-10min': 0, '>10min': 0}
    for d in durations:
        mins = d / 1000 / 60
        if mins < 2: dur_ranges['<2min'] += 1
        elif mins < 3: dur_ranges['2-3min'] += 1
        elif mins < 4: dur_ranges['3-4min'] += 1
        elif mins < 5: dur_ranges['4-5min'] += 1
        elif mins < 7: dur_ranges['5-7min'] += 1
        elif mins < 10: dur_ranges['7-10min'] += 1
        else: dur_ranges['>10min'] += 1

    # === 语言分析 ===
    lang_counter = Counter()
    lang_by_year = defaultdict(lambda: Counter())

    for song in songs:
        lang = detect_language(song['name'], song['artists'])
        lang_counter[lang] += 1
        at = song['added_at']
        if at and at > 0:
            year = datetime.fromtimestamp(at / 1000).year
            lang_by_year[year][lang] += 1

    # === 专辑分析 ===
    album_counter = Counter()
    for song in songs:
        if song['album']:
            album_counter[song['album']] += 1

    # === 收藏频率 ===
    sorted_months = sorted(year_month_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    # === 音乐时代分析 ===
    pub_year_counter = Counter()
    for song in songs:
        pt = song.get('publish_time', 0)
        if pt and pt > 0:
            try:
                pub_year = datetime.fromtimestamp(pt / 1000).year
                if 1950 <= pub_year <= 2030:
                    pub_year_counter[pub_year] += 1
            except Exception:
                pass

    decade_counter = Counter()
    for year, count in pub_year_counter.items():
        decade = f"{(year // 10) * 10}s"
        decade_counter[decade] += count

    # === 深夜收藏分析 ===
    late_night_songs = []
    for song in songs:
        at = song['added_at']
        if at and at > 0:
            dt = datetime.fromtimestamp(at / 1000)
            if 0 <= dt.hour < 4:
                late_night_songs.append(song)

    # === 长歌分析 ===
    long_songs = [s for s in songs if s['duration_ms'] > 7 * 60 * 1000]
    very_long_songs = [s for s in songs if s['duration_ms'] > 10 * 60 * 1000]

    # === 高频收藏日 ===
    day_counts = defaultdict(int)
    day_songs = defaultdict(list)
    for song in songs:
        at = song['added_at']
        if at and at > 0:
            dt = datetime.fromtimestamp(at / 1000)
            day_key = dt.strftime('%Y-%m-%d')
            day_counts[day_key] += 1
            day_songs[day_key].append(song)

    peak_days = sorted(day_counts.items(), key=lambda x: x[1], reverse=True)[:30]

    # === 首尾歌曲 ===
    songs_with_time = [(s, s['added_at']) for s in songs if s['added_at'] and s['added_at'] > 0]
    songs_with_time.sort(key=lambda x: x[1])
    earliest_songs = [(s['name'], s['artists'], datetime.fromtimestamp(s['added_at']/1000).strftime('%Y-%m-%d'))
                      for s, _ in songs_with_time[:10]] if songs_with_time else []
    latest_songs = [(s['name'], s['artists'], datetime.fromtimestamp(s['added_at']/1000).strftime('%Y-%m-%d'))
                    for s, _ in songs_with_time[-10:]] if songs_with_time else []

    # 构建分析结果
    analysis = {
        'total_songs': len(songs),
        'year_counts': dict(year_counts),
        'top_artists': artist_counter.most_common(100),
        'lang_distribution': dict(lang_counter),
        'lang_by_year': {str(k): dict(v) for k, v in lang_by_year.items()},
        'duration_stats': {
            'avg_minutes': round(avg_dur, 1),
            'total_hours': round(total_dur, 1),
            'distribution': dur_ranges,
            'long_songs_count': len(long_songs),
            'very_long_songs_count': len(very_long_songs),
        },
        'top_albums': album_counter.most_common(50),
        'year_top_artists': year_top_artists,
        'decade_distribution': dict(decade_counter),
        'peak_months': sorted_months,
        'peak_days': peak_days,
        'late_night_count': len(late_night_songs),
        'earliest_songs': earliest_songs,
        'latest_songs': latest_songs,
        'time_span': {
            'first_year': min(year_counts.keys()) if year_counts else None,
            'last_year': max(year_counts.keys()) if year_counts else None,
        }
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)

    print(f"✅ 分析完成，结果保存到 {output_path}")

    # 打印摘要
    print(f"\n{'='*60}")
    print(f"📊 分析摘要")
    print(f"{'='*60}")
    print(f"  总歌曲数: {len(songs)}")
    print(f"  时间跨度: {analysis['time_span']['first_year']} - {analysis['time_span']['last_year']}")
    print(f"  总时长: {total_dur:.0f} 小时")
    print(f"  平均时长: {avg_dur:.1f} 分钟")
    print(f"  长歌(>7min): {len(long_songs)} 首")
    print(f"  深夜收藏(0-4点): {len(late_night_songs)} 首")
    print(f"  最爱歌手: {', '.join(a[0] for a in artist_counter.most_common(5))}")
    print(f"  语言分布: {dict(lang_counter.most_common(5))}")

    return analysis


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python analyze_playlist.py <playlist_data.json> <output_analysis.json>")
        sys.exit(1)

    analyze(sys.argv[1], sys.argv[2])
