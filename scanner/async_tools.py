import asyncio
import aiohttp
import socket
import os
import importlib.util
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return url, await response.text()
    except Exception:
        return url, ""
    

async def extract_links_async(start_url):
    async with aiohttp.ClientSession() as session:
        url, html = await fetch_page(session, start_url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        return [urljoin(start_url, a.get("href")) for a in soup.find_all("a", href=True)]
        
async def check_subdomain(session, subdomain):
    try:
        await asyncio.get_event_loop().getaddrinfo(subdomain, None)
        return subdomain
    except socket.gaierror:
        return None
    
async def brute_force_subdomains_async(domain, wordlist):
    tasks = []
    for prefix in wordlist:
        full_domain = f"{prefix}.{domain}"
        tasks.append(check_subdomain(None, full_domain))
    results = await asyncio.gather(*tasks)
    return [sub for sub in results if sub]


def load_plugins(plugin_folder="plugins"):
    plugins = []
    if not os.path.isdir(plugin_folder):
        return plugins
    
    for fname in os.listdir(plugin_folder):
        if fname.endswith(".py"):
            plugins_path = os.path.join(plugin_folder, fname)
            spec = importlib.util.spec_from_file_location(fname[:-3], plugins_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "run_plugin"):
                    plugins.append(mod)
        return plugins
    
def run_plugins(plugins, url, html, headers):
    results = []
    for plugin in plugins:
        try:
            result = plugin.run_plugin(url, html, headers)
            if result:
                results.append({plugin.__name__: result})
        except Exception as e:
            results.append({plugin.__name__: f"Error: {str(e)}"})
    return results