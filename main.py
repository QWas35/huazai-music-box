# -*- coding: utf-8 -*-
"""
华仔音乐盒 - Android版本
基于Kivy框架开发
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.metrics import dp

import requests
import json
import threading
import os
import datetime
import random
from urllib.parse import quote

VERSION = "3.5"
APP_NAME = "🎵 华仔音乐盒"

# 天蓝色配色方案
COLORS = {
    'bg_dark': (0.102, 0.322, 0.463, 1),      # #1a5276
    'bg_medium': (0.161, 0.502, 0.725, 1),    # #2980b9
    'bg_light': (0.365, 0.678, 0.886, 1),     # #5dade2
    'accent': (0.204, 0.596, 0.859, 1),       # #3498db
    'text': (1, 1, 1, 1),                      # 白色
    'text_secondary': (0.831, 0.902, 0.945, 1),
    'row_odd': (0.922, 0.961, 0.984, 1),      # 浅蓝
    'row_even': (0.831, 0.902, 0.945, 1),
    'netease': (0.753, 0.224, 0.169, 1),      # 网易红
    'kugou': (0.161, 0.502, 0.725, 1),        # 酷狗蓝
    'qq': (0.153, 0.682, 0.376, 1),           # QQ绿
    'kuwo': (0.557, 0.267, 0.678, 1),         # 酷我紫
    'migu': (0.902, 0.494, 0.133, 1),         # 咪咕橙
    'gold': (0.945, 0.769, 0.059, 1),         # 金色
}

# 音乐源配置
MUSIC_SOURCES = ['全网搜索', '网易云', '酷狗', 'QQ音乐', '酷我', '咪咕']

HOT_TAGS = ['流行', '抖音', '情歌', '经典', '粤语', '民谣', '摇滚', '古风', '电子', '说唱']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}


class MusicAPI:
    """音乐API封装"""
    
    @staticmethod
    def search_netease(keyword, limit=20):
        """网易云音乐搜索"""
        try:
            url = "https://music.163.com/api/search/get/web"
            params = {'s': keyword, 'type': 1, 'offset': 0, 'limit': limit}
            headers = HEADERS.copy()
            headers['Referer'] = 'https://music.163.com/'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            resp = requests.post(url, data=params, headers=headers, timeout=10)
            data = resp.json()
            
            results = []
            if data.get('code') == 200:
                for song in data.get('result', {}).get('songs', []):
                    artists = ', '.join([a['name'] for a in song.get('artists', [])])
                    results.append({
                        'id': str(song['id']),
                        'title': song.get('name', ''),
                        'artist': artists,
                        'album': song.get('album', {}).get('name', ''),
                        'source': '网易云',
                        'duration': song.get('duration', 0) // 1000
                    })
            return results
        except Exception as e:
            print(f"网易云搜索失败: {e}")
            return []
    
    @staticmethod
    def search_kugou(keyword, limit=20):
        """酷狗音乐搜索"""
        try:
            url = "https://complexsearch.kugou.com/v2/search/song"
            params = {
                'keyword': keyword, 'page': 1, 'pagesize': limit,
                'platform': 'WebFilter', 'clientver': 2000
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            results = []
            if data.get('status') == 1:
                for song in data.get('data', {}).get('lists', []):
                    results.append({
                        'id': song.get('FileHash', ''),
                        'title': song.get('SongName', ''),
                        'artist': song.get('SingerName', '').replace('、', ', '),
                        'album': song.get('AlbumName', ''),
                        'source': '酷狗',
                        'duration': song.get('Duration', 0),
                        'hash': song.get('FileHash', '')
                    })
            return results
        except Exception as e:
            print(f"酷狗搜索失败: {e}")
            return []
    
    @staticmethod
    def search_qq(keyword, limit=20):
        """QQ音乐搜索"""
        try:
            url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
            params = {'w': keyword, 'p': 1, 'n': limit, 'format': 'json', 'new_json': 1}
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            results = []
            if data.get('code') == 0:
                for song in data.get('data', {}).get('song', {}).get('list', []):
                    artists = ', '.join([s.get('name', '') for s in song.get('singer', [])])
                    results.append({
                        'id': str(song.get('mid', '')),
                        'title': song.get('name', ''),
                        'artist': artists,
                        'album': song.get('album', {}).get('name', ''),
                        'source': 'QQ音乐',
                        'duration': song.get('interval', 0)
                    })
            return results
        except Exception as e:
            print(f"QQ音乐搜索失败: {e}")
            return []
    
    @staticmethod
    def search_kuwo(keyword, limit=20):
        """酷我音乐搜索"""
        try:
            url = "https://www.kuwo.cn/api/www/search/searchMusicBykeyWord"
            params = {'key': keyword, 'pn': 1, 'rn': limit}
            headers = HEADERS.copy()
            headers['Referer'] = 'https://www.kuwo.cn/'
            
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            
            results = []
            if data.get('code') == 200:
                for song in data.get('data', {}).get('list', []):
                    results.append({
                        'id': str(song.get('rid', '')),
                        'title': song.get('name', ''),
                        'artist': song.get('artist', ''),
                        'album': song.get('album', ''),
                        'source': '酷我',
                        'duration': 0
                    })
            return results
        except Exception as e:
            print(f"酷我搜索失败: {e}")
            return []
    
    @staticmethod
    def search_migu(keyword, limit=20):
        """咪咕音乐搜索"""
        try:
            url = "https://m.music.migu.cn/migu/remoting/scr_search_tag"
            params = {'keyword': keyword, 'pgc': 1, 'rows': limit, 'type': 2}
            headers = HEADERS.copy()
            headers['Referer'] = 'https://m.music.migu.cn/'
            
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            data = resp.json()
            
            results = []
            for song in data.get('musics', []):
                results.append({
                    'id': song.get('id', ''),
                    'title': song.get('songName', ''),
                    'artist': song.get('singerName', ''),
                    'album': song.get('albumName', ''),
                    'source': '咪咕',
                    'duration': 0
                })
            return results
        except Exception as e:
            print(f"咪咕搜索失败: {e}")
            return []
    
    @staticmethod
    def get_play_url(source, song_id, hash_id=None):
        """获取播放链接"""
        try:
            if source == '网易云':
                return f"https://music.163.com/song/media/outer/url?id={song_id}.mp3"
            
            elif source == '酷狗' and hash_id:
                url = "https://wwwapi.kugou.com/yy/index.php"
                params = {
                    'r': 'play/getdata', 'hash': hash_id,
                    'mid': 'd869723361c7194010f1645f4a80f5ca',
                    'platid': 4, '_': int(datetime.datetime.now().timestamp() * 1000)
                }
                resp = requests.get(url, params=params, timeout=10)
                data = resp.json()
                if data.get('status') == 1:
                    return data.get('data', {}).get('play_url', '')
            
            elif source == 'QQ音乐':
                return f"https://y.qq.com/n/ryqq/songDetail/{song_id}"
            
            elif source == '酷我':
                url = f"https://www.kuwo.cn/api/v1/www/music/play?mid={song_id}&type=music"
                resp = requests.get(url, timeout=10)
                data = resp.json()
                return data.get('data', {}).get('url', '')
            
        except Exception as e:
            print(f"获取播放链接失败: {e}")
        return None


class SongItem(BoxLayout):
    """歌曲列表项"""
    
    def __init__(self, song_data, index, on_play_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.song = song_data
        self.on_play = on_play_callback
        
        # 背景色
        bg_color = COLORS['row_odd'] if index % 2 == 0 else COLORS['row_even']
        with self.canvas.before:
            Color(*bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # 序号
        self.add_widget(Label(
            text=str(index + 1),
            size_hint_x=0.1,
            color=COLORS['bg_dark'],
            font_size=dp(14)
        ))
        
        # 歌曲信息
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.6)
        info_layout.add_widget(Label(
            text=song_data['title'][:20],
            size_hint_y=0.6,
            halign='left',
            valign='middle',
            color=COLORS['bg_dark'],
            font_size=dp(15),
            bold=True
        ))
        info_layout.add_widget(Label(
            text=f"{song_data['artist'][:15]} - {song_data.get('source', '')}",
            size_hint_y=0.4,
            halign='left',
            valign='middle',
            color=(0.3, 0.3, 0.3, 1),
            font_size=dp(12)
        ))
        self.add_widget(info_layout)
        
        # 播放按钮
        play_btn = Button(
            text='▶',
            size_hint_x=0.15,
            background_color=COLORS['accent'],
            font_size=dp(18)
        )
        play_btn.bind(on_press=self._on_play_press)
        self.add_widget(play_btn)
        
        # 下载按钮
        download_btn = Button(
            text='⬇',
            size_hint_x=0.15,
            background_color=COLORS['gold'],
            font_size=dp(18)
        )
        download_btn.bind(on_press=self._on_download_press)
        self.add_widget(download_btn)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    
    def _on_play_press(self, instance):
        if self.on_play:
            self.on_play(self.song)
    
    def _on_download_press(self, instance):
        # TODO: 实现下载功能
        popup = Popup(title='提示', content=Label(text='下载功能开发中...'), size_hint=(0.8, 0.3))
        popup.open()


class MusicApp(App):
    """主应用"""
    
    def build(self):
        self.title = f"{APP_NAME} v{VERSION}"
        self.search_results = []
        self.current_song = None
        self.sound = None
        self.is_playing = False
        
        # 主布局
        self.root_layout = BoxLayout(orientation='vertical')
        
        # 设置背景色
        with self.root_layout.canvas.before:
            Color(*COLORS['bg_dark'])
            self.bg_rect = Rectangle(size=self.root_layout.size, pos=self.root_layout.pos)
        self.root_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # === 顶部标题 ===
        header = BoxLayout(size_hint_y=0.08)
        with header.canvas.before:
            Color(*COLORS['bg_dark'])
            Rectangle(size=header.size, pos=header.pos)
        
        title_label = Label(
            text=APP_NAME,
            font_size=dp(22),
            bold=True,
            color=COLORS['text']
        )
        header.add_widget(title_label)
        self.root_layout.add_widget(header)
        
        # === 搜索区域 ===
        search_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=dp(5), padding=dp(10))
        with search_layout.canvas.before:
            Color(*COLORS['bg_medium'])
            Rectangle(size=search_layout.size, pos=search_layout.pos)
        
        # 音乐源选择
        source_layout = BoxLayout(size_hint_y=0.35, spacing=dp(5))
        source_layout.add_widget(Label(text='音乐源:', size_hint_x=0.2, color=COLORS['text'], font_size=dp(14)))
        self.source_spinner = Spinner(
            text='全网搜索',
            values=MUSIC_SOURCES,
            size_hint_x=0.8,
            background_color=COLORS['bg_light'],
            color=COLORS['text'],
            font_size=dp(14)
        )
        source_layout.add_widget(self.source_spinner)
        search_layout.add_widget(source_layout)
        
        # 搜索输入框
        input_layout = BoxLayout(size_hint_y=0.35, spacing=dp(5))
        self.search_input = TextInput(
            hint_text='输入歌曲名、歌手名搜索...',
            multiline=False,
            size_hint_x=0.75,
            font_size=dp(16),
            background_color=COLORS['bg_light'],
            foreground_color=COLORS['text']
        )
        input_layout.add_widget(self.search_input)
        
        search_btn = Button(
            text='🔍 搜索',
            size_hint_x=0.25,
            background_color=COLORS['accent'],
            color=COLORS['text'],
            font_size=dp(14),
            bold=True
        )
        search_btn.bind(on_press=self.do_search)
        input_layout.add_widget(search_btn)
        search_layout.add_widget(input_layout)
        
        # 热门标签
        tags_layout = BoxLayout(size_hint_y=0.3, spacing=dp(3))
        tags_layout.add_widget(Label(text='热门:', size_hint_x=0.15, color=COLORS['text_secondary'], font_size=dp(12)))
        for tag in HOT_TAGS[:6]:
            tag_btn = Button(
                text=tag,
                size_hint_x=None,
                width=dp(50),
                background_color=COLORS['bg_light'],
                color=COLORS['text'],
                font_size=dp(11)
            )
            tag_btn.bind(on_press=lambda instance, t=tag: self.search_by_tag(t))
            tags_layout.add_widget(tag_btn)
        search_layout.add_widget(tags_layout)
        
        self.root_layout.add_widget(search_layout)
        
        # === 歌曲列表 ===
        self.list_container = BoxLayout(orientation='vertical', size_hint_y=0.62)
        
        # 列表标题
        list_header = BoxLayout(size_hint_y=0.06)
        with list_header.canvas.before:
            Color(*COLORS['bg_medium'])
            Rectangle(size=list_header.size, pos=list_header.pos)
        for text, width in [('序号', 0.1), ('歌曲', 0.6), ('播放', 0.15), ('下载', 0.15)]:
            list_header.add_widget(Label(text=text, size_hint_x=width, color=COLORS['text'], font_size=dp(13)))
        self.list_container.add_widget(list_header)
        
        # 滚动列表
        self.scroll_view = ScrollView(size_hint_y=0.94)
        self.song_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(1))
        self.song_list.bind(minimum_height=self.song_list.setter('height'))
        self.scroll_view.add_widget(self.song_list)
        self.list_container.add_widget(self.scroll_view)
        
        self.root_layout.add_widget(self.list_container)
        
        # === 状态栏 ===
        self.status_label = Label(
            text='💡 输入关键词搜索音乐',
            size_hint_y=0.05,
            color=COLORS['text_secondary'],
            font_size=dp(13)
        )
        self.root_layout.add_widget(self.status_label)
        
        # === 底部播放器 ===
        player_layout = BoxLayout(size_hint_y=0.1, spacing=dp(5), padding=dp(5))
        with player_layout.canvas.before:
            Color(*COLORS['bg_medium'])
            Rectangle(size=player_layout.size, pos=player_layout.pos)
        
        # 当前歌曲信息
        self.current_song_label = Label(
            text='未播放',
            size_hint_x=0.6,
            halign='left',
            color=COLORS['text'],
            font_size=dp(14),
            bold=True
        )
        player_layout.add_widget(self.current_song_label)
        
        # 播放/暂停按钮
        self.play_btn = Button(
            text='▶',
            size_hint_x=0.2,
            background_color=COLORS['accent'],
            font_size=dp(24)
        )
        self.play_btn.bind(on_press=self.toggle_play)
        player_layout.add_widget(self.play_btn)
        
        # 停止按钮
        stop_btn = Button(
            text='⏹',
            size_hint_x=0.2,
            background_color=COLORS['netease'],
            font_size=dp(24)
        )
        stop_btn.bind(on_press=self.stop_play)
        player_layout.add_widget(stop_btn)
        
        self.root_layout.add_widget(player_layout)
        
        return self.root_layout
    
    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos
    
    def do_search(self, instance):
        """执行搜索"""
        keyword = self.search_input.text.strip()
        if not keyword:
            return
        
        source = self.source_spinner.text
        self.status_label.text = '🔍 搜索中...'
        
        # 清空列表
        self.song_list.clear_widgets()
        self.search_results = []
        
        # 启动搜索线程
        threading.Thread(target=self._search_thread, args=(keyword, source), daemon=True).start()
    
    def _search_thread(self, keyword, source):
        """搜索线程"""
        results = []
        
        if source == '全网搜索':
            # 并发搜索所有源
            threads = []
            results_list = []
            lock = threading.Lock()
            
            def search_func(api_func):
                try:
                    r = api_func(keyword, 12)
                    with lock:
                        results_list.extend(r)
                except:
                    pass
            
            for api_func in [
                MusicAPI.search_netease,
                MusicAPI.search_kugou,
                MusicAPI.search_qq,
                MusicAPI.search_kuwo,
                MusicAPI.search_migu
            ]:
                t = threading.Thread(target=search_func, args=(api_func,))
                t.daemon = True
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join(timeout=12)
            
            results = results_list
            random.shuffle(results)
        
        elif source == '网易云':
            results = MusicAPI.search_netease(keyword, 30)
        elif source == '酷狗':
            results = MusicAPI.search_kugou(keyword, 30)
        elif source == 'QQ音乐':
            results = MusicAPI.search_qq(keyword, 30)
        elif source == '酷我':
            results = MusicAPI.search_kuwo(keyword, 30)
        elif source == '咪咕':
            results = MusicAPI.search_migu(keyword, 30)
        
        self.search_results = results
        
        # 更新UI
        Clock.schedule_once(lambda dt: self._update_search_results(results), 0)
    
    def _update_search_results(self, results):
        """更新搜索结果"""
        self.song_list.clear_widgets()
        
        if not results:
            self.status_label.text = '❌ 未找到相关歌曲'
            return
        
        for i, song in enumerate(results):
            item = SongItem(song, i, self.play_song)
            self.song_list.add_widget(item)
        
        self.status_label.text = f'✅ 找到 {len(results)} 首歌曲'
    
    def search_by_tag(self, tag):
        """按标签搜索"""
        self.search_input.text = tag
        self.do_search(None)
    
    def play_song(self, song):
        """播放歌曲"""
        self.current_song = song
        self.current_song_label.text = f"{song['title']} - {song['artist']}"
        self.status_label.text = f'🎵 正在播放: {song["title"]}'
        
        # 停止之前的播放
        if self.sound:
            self.sound.stop()
        
        # 获取播放链接并播放
        threading.Thread(target=self._play_thread, args=(song,), daemon=True).start()
    
    def _play_thread(self, song):
        """播放线程"""
        song_id = song.get('id', '')
        hash_id = song.get('hash', '')
        
        play_url = MusicAPI.get_play_url(song['source'], song_id, hash_id)
        
        if play_url:
            Clock.schedule_once(lambda dt: self._load_and_play(play_url), 0)
        else:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', '❌ 无法获取播放链接'), 0)
    
    def _load_and_play(self, url):
        """加载并播放"""
        try:
            self.sound = SoundLoader.load(url)
            if self.sound:
                self.sound.play()
                self.is_playing = True
                self.play_btn.text = '⏸'
            else:
                self.status_label.text = '❌ 无法加载音频'
        except Exception as e:
            self.status_label.text = f'❌ 播放失败: {str(e)[:20]}'
    
    def toggle_play(self, instance):
        """切换播放/暂停"""
        if self.sound:
            if self.is_playing:
                self.sound.stop()
                self.play_btn.text = '▶'
                self.is_playing = False
            else:
                self.sound.play()
                self.play_btn.text = '⏸'
                self.is_playing = True
    
    def stop_play(self, instance):
        """停止播放"""
        if self.sound:
            self.sound.stop()
            self.sound = None
        self.is_playing = False
        self.play_btn.text = '▶'
        self.current_song_label.text = '未播放'
        self.status_label.text = '💡 输入关键词搜索音乐'


if __name__ == '__main__':
    MusicApp().run()
