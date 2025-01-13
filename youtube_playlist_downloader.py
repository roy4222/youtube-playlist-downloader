import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import threading
import yt_dlp
import os
import sys
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class YoutubePlaylistDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube播放清單下載器")
        self.root.geometry("800x600")  # 加大視窗
        
        # 設置主題風格
        style = ttk.Style()
        style.theme_use('clam')
        
        # 創建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL輸入區域
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="播放清單URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # 下載位置選擇
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(path_frame, text="下載位置:").pack(side=tk.LEFT)
        self.path_entry = ttk.Entry(path_frame)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.path_entry.insert(0, os.path.join(os.path.expanduser("~"), "Downloads"))
        
        ttk.Button(path_frame, text="瀏覽", command=self.browse_directory).pack(side=tk.RIGHT)
        
        # 線程數選擇
        thread_frame = ttk.Frame(main_frame)
        thread_frame.pack(fill=tk.X, pady=5)
        ttk.Label(thread_frame, text="同時下載數:").pack(side=tk.LEFT)
        self.thread_var = tk.StringVar(value="5")
        thread_spinbox = ttk.Spinbox(thread_frame, from_=1, to=10, width=5, textvariable=self.thread_var)
        thread_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 添加說明標籤
        ttk.Label(thread_frame, text="(建議: 3-7, 最大: 10)", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # 下載按鈕
        self.download_btn = ttk.Button(main_frame, text="開始下載", command=self.start_download)
        self.download_btn.pack(pady=10)
        
        # 總進度條
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        ttk.Label(progress_frame, text="總進度:").pack(side=tk.LEFT)
        self.total_progress_var = tk.DoubleVar()
        self.total_progress_bar = ttk.Progressbar(progress_frame, variable=self.total_progress_var, maximum=100)
        self.total_progress_bar.pack(fill=tk.X, expand=True, padx=5)
        
        # 當前下載進度條
        current_progress_frame = ttk.Frame(main_frame)
        current_progress_frame.pack(fill=tk.X, pady=5)
        ttk.Label(current_progress_frame, text="當前歌曲:").pack(side=tk.LEFT)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(current_progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, expand=True, padx=5)
        
        # 狀態標籤
        self.status_label = ttk.Label(main_frame, text="準備就緒")
        self.status_label.pack(pady=5)
        
        # 下載列表（使用Treeview替代Text）
        self.download_list = ttk.Treeview(main_frame, columns=("status"), show="headings", height=10)
        self.download_list.heading("status", text="下載狀態")
        self.download_list.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 添加滾動條
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.download_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.download_list.configure(yscrollcommand=scrollbar.set)
        
        self.downloaded_count = 0
        self.total_videos = 0
        
    def update_status(self, status, item_id=None):
        self.status_label.config(text=status)
        if item_id is None:
            self.download_list.insert("", tk.END, values=(status,))
        else:
            self.download_list.item(item_id, values=(status,))
        self.download_list.yview_moveto(1)
        self.root.update_idletasks()
    
    def download_single_video(self, video_info, index):
        try:
            video_url = f"https://www.youtube.com/watch?v={video_info.get('id', '')}"
            title = video_info.get('title', 'Unknown Title')
            item_id = self.download_list.insert("", tk.END, values=(f"等待下載: {title}",))
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(self.path_entry.get(), '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'external_downloader': 'aria2c',
                'external_downloader_args': [
                    '-x', '16',  # 16個連接
                    '-s', '16',  # 16個線程
                    '-k', '2M',  # 每個分片2M
                    '--min-split-size=1M',  # 最小分片1M
                    '--max-connection-per-server=16',  # 每個服務器最大連接數
                    '--max-concurrent-downloads=16',  # 最大並行下載數
                ],
                'progress_hooks': [lambda d: self.download_progress_hook(d, item_id)],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status(f"正在下載: {title}", item_id)
                ydl.download([video_url])
                self.downloaded_count += 1
                self.total_progress_var.set((self.downloaded_count / self.total_videos) * 100)
                self.update_status(f"完成: {title}", item_id)
                
        except Exception as e:
            self.update_status(f"下載失敗 {title}: {str(e)}", item_id)
    
    def download_progress_hook(self, d, item_id):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                if total:
                    progress = (downloaded / total) * 100
                    self.progress_var.set(progress)
                    speed = d.get('speed', 0)
                    if speed:
                        speed_mb = speed / 1024 / 1024
                        self.update_status(f"下載中: {d['filename']} - {speed_mb:.1f}MB/s", item_id)
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
    
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("錯誤", "請輸入播放清單URL")
            return
        
        download_path = self.path_entry.get()
        if not os.path.exists(download_path):
            try:
                os.makedirs(download_path)
            except Exception as e:
                messagebox.showerror("錯誤", f"無法創建下載目錄: {str(e)}")
                return
        
        self.download_btn.config(state=tk.DISABLED)
        self.download_list.delete(*self.download_list.get_children())
        self.downloaded_count = 0
        self.progress_var.set(0)
        self.total_progress_var.set(0)
        
        threading.Thread(target=self.process_playlist, args=(url,), daemon=True).start()
    
    def process_playlist(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.update_status("正在獲取播放清單信息...")
                playlist_info = ydl.extract_info(url, download=False)
                
                if 'entries' not in playlist_info:
                    raise Exception("無法獲取播放清單信息")
                
                entries = [e for e in playlist_info['entries'] if e]
                self.total_videos = len(entries)
                self.update_status(f"找到 {self.total_videos} 個影片")
                
                max_workers = int(self.thread_var.get())
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = []
                    for index, entry in enumerate(entries, 1):
                        future = executor.submit(self.download_single_video, entry, index)
                        futures.append(future)
                    
                    for future in as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            self.update_status(f"下載失敗: {str(e)}")
                
                self.update_status("下載完成！")
                messagebox.showinfo("完成", "播放清單下載完成！")
        
        except Exception as e:
            self.update_status(f"發生錯誤: {str(e)}")
            messagebox.showerror("錯誤", str(e))
        
        finally:
            self.download_btn.config(state=tk.NORMAL)
            self.progress_var.set(0)
            self.total_progress_var.set(0)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, directory)

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubePlaylistDownloader(root)
    root.mainloop()
