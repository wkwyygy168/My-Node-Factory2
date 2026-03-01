import requests
import base64
import re

def universal_mirror_factory():
    # 你的核心镜像源列表
    sources = [
        "https://study.small1999.sbs/study/xuexi/v999/hneko?token=1dc7a802e70cfa93858e2fd6fe20aef6"
    ]
    
    yaml_results = []
    txt_results = []
    
    for url in sources:
        try:
            print(f"🚀 正在处理源: {url}")
            response = requests.get(url, timeout=15)
            content = response.text.strip()
            
            # --- 逻辑 A: 处理 YAML 后缀 (Clash 格式) ---
            if url.endswith(".yaml") or url.endswith(".yml"):
                # 提取 YAML 里的节点部分，防止全局配置冲突
                if "proxies:" in content:
                    # 仅截取 proxies: 之后的内容，确保 Karing 订阅不会因为多个 document 报错
                    proxy_part = content.split("proxies:")[1]
                    yaml_results.append(proxy_part)
                else:
                    yaml_results.append(content)
            
            # --- 逻辑 B: 处理 TXT 后缀 (明文/Base64 格式) ---
            else:
                # 尝试 Base64 暴力解密
                try:
                    temp_content = content + "=" * (-len(content) % 4)
                    decoded = base64.b64decode(temp_content).decode('utf-8', errors='ignore')
                    if "://" in decoded:
                        txt_results.append(decoded)
                    else:
                        txt_results.append(content)
                except:
                    txt_results.append(content)
                    
        except Exception as e:
            print(f"❌ 处理 {url} 失败: {e}")

    # --- 最终产出：YAML 镜像 ---
    # 我们为 YAML 镜像加一个标准头，把所有抓到的 proxies 拼接在下面
    final_yaml = "proxies:\n" + "\n".join(yaml_results)
    with open("nodes.yaml", "w", encoding="utf-8") as f:
        f.write(final_yaml)

    # --- 最终产出：TXT 镜像 ---
    # 合并所有明文链接
    final_txt = "\n".join(txt_results)
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(final_txt)
        
    print(f"✨ 镜像大功告成！YAML 镜像已生成，TXT 镜像已生成。")

if __name__ == "__main__":
    universal_mirror_factory()
