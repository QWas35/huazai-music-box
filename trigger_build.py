# -*- coding: utf-8 -*-
"""
华仔音乐盒 - 一键触发 Gitee/GitHub 打包
自动创建 GitHub 仓库并触发 Actions 构建 APK
"""

import json
import requests
import time
import os

GITEE_TOKEN = "ccfa676fb156e6d75da60d009cddd92c"
GITEE_USERNAME = "can-love-hefei-city"

def trigger_github_build():
    """
    方案一：触发 GitHub Actions 打包
    需要先在 GitHub 创建仓库并推送代码
    """
    print("=" * 50)
    print("  华仔音乐盒 - GitHub Actions 打包")
    print("=" * 50)
    print()
    print("📌 使用步骤：")
    print("1. 访问 https://github.com/new 创建仓库")
    print("2. 仓库名: huazai-music-box")
    print("3. 选择 Private")
    print("4. 不要初始化 README")
    print("5. 创建后，获取 GitHub Token:")
    print("   Settings → Developer settings → Personal access tokens → Generate")
    print("6. 将 Token 填入下方 GITHUB_TOKEN")
    print()
    
    GITHUB_TOKEN = input("请输入 GitHub Personal Access Token (或按回车退出): ").strip()
    if not GITHUB_TOKEN:
        print("❌ 未输入 Token，退出")
        return
    
    GITHUB_USERNAME = input("请输入 GitHub 用户名: ").strip()
    if not GITHUB_USERNAME:
        print("❌ 未输入用户名，退出")
        return
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 1. 创建仓库
    print("\n[1/3] 创建 GitHub 仓库...")
    repo_data = {
        "name": "huazai-music-box",
        "description": "🎵 华仔音乐盒 Android多源音乐搜索播放器",
        "private": False,
        "auto_init": False
    }
    
    try:
        resp = requests.post("https://api.github.com/user/repos", 
                          headers=headers, json=repo_data)
        if resp.status_code == 201:
            print("✅ 仓库创建成功")
        else:
            print(f"⚠️ 仓库可能已存在: {resp.json().get('message', '')}")
    except Exception as e:
        print(f"❌ 创建仓库失败: {e}")
        return
    
    # 2. 推送代码
    print("\n[2/3] 配置 Git 并推送代码...")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    os.system(f'git remote remove github 2>nul')
    os.system(f'git remote add github https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/huazai-music-box.git')
    os.system('git push github master 2>nul || git push github main 2>nul')
    
    print("✅ 代码推送完成")
    
    # 3. 触发 Actions
    print("\n[3/3] 触发 GitHub Actions 构建...")
    try:
        resp = requests.post(
            f"https://api.github.com/repos/{GITHUB_USERNAME}/huazai-music-box/actions/workflows/build.yml/dispatches",
            headers=headers,
            json={"ref": "master"}
        )
        
        # 也尝试 main 分支
        if resp.status_code != 204:
            resp = requests.post(
                f"https://api.github.com/repos/{GITHUB_USERNAME}/huazai-music-box/actions/workflows/build.yml/dispatches",
                headers=headers,
                json={"ref": "main"}
            )
        
        if resp.status_code == 204:
            print("✅ Actions 构建已触发！")
            print(f"\n📱 查看构建进度: https://github.com/{GITHUB_USERNAME}/huazai-music-box/actions")
            print(f"📦 构建完成后在 Artifacts 中下载 APK")
            print(f"⏱️ 预计需要 15-20 分钟")
        else:
            print(f"⚠️ 触发失败: {resp.status_code}")
            print("请手动访问 Actions 页面触发构建")
    except Exception as e:
        print(f"❌ 触发失败: {e}")


if __name__ == "__main__":
    trigger_github_build()
    input("\n按回车退出...")
