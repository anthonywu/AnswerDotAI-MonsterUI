# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_core.ipynb.

# %% auto 0
__all__ = ['HEADER_URLS', 'daisy_styles', 'fast_app', 'FastHTML', 'Theme']

# %% ../nbs/01_core.ipynb
import fasthtml.common as fh
from .foundations import *
from fasthtml.common import FastHTML, fast_app
from enum import Enum, auto
from fastcore.all import *
import httpx
from pathlib import Path

# %% ../nbs/01_core.ipynb
@delegates(fh.fast_app, but=['pico'])
def fast_app(*args, pico=False, **kwargs):
    "Create a FastHTML or FastHTMLWithLiveReload app with `bg-background text-foreground` to bodykw for frankenui themes"
    if 'bodykw' not in kwargs: kwargs['bodykw'] = {}
    if 'class' not in kwargs['bodykw']: kwargs['bodykw']['class'] = ''
    kwargs['bodykw']['class'] = stringify((kwargs['bodykw']['class'],'bg-background text-foreground'))
    return fh.fast_app(*args, pico=pico, **kwargs)

# %% ../nbs/01_core.ipynb
@delegates(fh.FastHTML, but=['pico'])
def FastHTML(*args, pico=False, **kwargs):
    "Create a FastHTML app and adds `bg-background text-foreground` to bodykw for frankenui themes"
    if 'bodykw' not in kwargs: kwargs['bodykw'] = {}
    if 'class' not in kwargs['bodykw']: kwargs['bodykw']['class'] = ''
    kwargs['bodykw']['class'] = stringify((kwargs['bodykw']['class'],'bg-background text-foreground'))
    bodykw = kwargs.pop('bodykw',{})
    return fh.FastHTML(*args, pico=pico, **bodykw, **kwargs)

# %% ../nbs/01_core.ipynb
def _headers_theme(color, mode='auto'):
    mode_script = {
        'auto': '''
            if (
                localStorage.getItem("mode") === "dark" ||
                (!("mode" in localStorage) &&
                window.matchMedia("(prefers-color-scheme: dark)").matches)
            ) {
                htmlElement.classList.add("dark");
            } else {
                htmlElement.classList.remove("dark");
            }
        ''',
        'light': 'htmlElement.classList.remove("dark");',
        'dark': 'htmlElement.classList.add("dark");'
    }
    
    return fh.Script(f'''
        const htmlElement = document.documentElement;
        {mode_script[mode]}
        htmlElement.classList.add(localStorage.getItem("theme") || "uk-theme-{color}");
    ''')

# %% ../nbs/01_core.ipynb
HEADER_URLS = {
        'franken_css': "https://unpkg.com/franken-ui@2.0.0-internal.40/dist/css/core.min.css",
#         'franken_tw_utils': "https://unpkg.com/franken-ui@2.0.0-internal.40/dist/css/utilities.min.css",
        'franken_js_core': "https://unpkg.com/franken-ui@2.0.0-internal.40/dist/js/core.iife.js",
        'franken_icons': "https://unpkg.com/franken-ui@2.0.0-internal.40/dist/js/icon.iife.js",
#         'icon_js': "https://cdn.jsdelivr.net/gh/answerdotai/monsterui@main/monsterui/icon.iife.js",
        'tailwind': "https://cdn.tailwindcss.com",
        'daisyui': "https://cdn.jsdelivr.net/npm/daisyui@4.12.22/dist/full.min.css",
        'highlight_js': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js",
        'highlight_python': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/python.min.js",
        'highlight_light_css': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-light.css",
        'highlight_dark_css': "https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/atom-one-dark.css",
        'highlight_copy': "https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.js",
        'highlight_copy_css': "https://cdn.jsdelivr.net/gh/arronhunt/highlightjs-copy/dist/highlightjs-copy.min.css",
}

def _download_resource(url, static_dir):
    "Download a single resource and return its local path"
    static = Path(static_dir)
    fname = static/f"{url[0]}.{'js' if 'js' in url[1] else 'css'}"
    content = httpx.get(url[1], follow_redirects=True).content
    fname.write_bytes(content)
    return (url[0], f"/{static_dir}/{fname.name}")

# %% ../nbs/01_core.ipynb
daisy_styles = Style("""
:root {
  --p: from hsl(var(--primary)) l c h;
  --pc: from hsl(var(--primary-foreground)) l c h;
  --s: from hsl(var(--secondary)) l c h;
  --sc: from hsl(var(--secondary-foreground)) l c h;
  --b2: from hsl(var(--card-background)) l c h;
  --b1: from hsl(var(--background)) l c h;
  --bc: from hsl(var(--foreground)) l c h;
  --b3: from hsl(var(--ring)) l c h;
  --er: from hsl(var(--destructive)) l c h;
  --erc: from hsl(var(--destructive-foreground)) l c h;
}
""")


# %% ../nbs/01_core.ipynb
class Theme(Enum):
    "Selector to choose theme and get all headers needed for app.  Includes frankenui + tailwind + daisyui + highlight.js options"
    def _generate_next_value_(name, start, count, last_values): return name
    slate = auto()
    stone = auto()
    gray = auto()
    neutral = auto()
    red = auto()
    rose = auto()
    orange = auto()
    green = auto()
    blue = auto()
    yellow = auto()
    violet = auto()
    zinc = auto()

    def _create_headers(self, urls, mode='auto', daisy=True, highlightjs=False):
        "Create header elements with given URLs"
        hdrs = [
            fh.Link(rel="stylesheet", href=urls['franken_css']),
#             fh.Link(rel="stylesheet", href=urls['franken_utils']),
            fh.Script(type="module", src=urls['franken_js_core']),
            fh.Script(type="module", src=urls['franken_icons']),
            fh.Script(src=urls['tailwind']),
            _headers_theme(self.value, mode=mode)]

        if daisy:
            hdrs += [fh.Link(rel="stylesheet", href=urls['daisyui']), daisy_styles]
            
        if highlightjs:
            hdrs += [
                fh.Script(src=urls['highlight_js']),
                fh.Script(src=urls['highlight_python']),
                fh.Link(rel="stylesheet", href=urls['highlight_light_css'], id='hljs-light'),
                fh.Link(rel="stylesheet", href=urls['highlight_dark_css'], id='hljs-dark'),
                fh.Script(src=urls['highlight_copy']),
                fh.Link(rel="stylesheet", href=urls['highlight_copy_css']),
                fh.Script('''
                    hljs.addPlugin(new CopyButtonPlugin());
                    hljs.configure({
                        cssSelector: 'pre code',
                        languages: ['python'],
                        ignoreUnescapedHTML: true
                    });
                    function updateTheme() {
                        const isDark = document.documentElement.classList.contains('dark');
                        document.getElementById('hljs-dark').disabled = !isDark;
                        document.getElementById('hljs-light').disabled = isDark;
                    }
                    new MutationObserver(mutations =>
                        mutations.forEach(m => m.target.tagName === 'HTML' &&
                            m.attributeName === 'class' && updateTheme())
                    ).observe(document.documentElement, { attributes: true });
                    updateTheme();
                    htmx.onLoad(hljs.highlightAll);
                ''', type='module'),
            ]

        return hdrs

    def headers(self, mode='auto', daisy=True, highlightjs=False):
        "Create frankenui and tailwind cdns"
        return self._create_headers(HEADER_URLS, mode=mode, daisy=daisy, highlightjs=highlightjs)    
    
    def local_headers(self, mode='auto', static_dir='static', daisy=True, highlightjs=False):
        "Create headers using local files downloaded from CDNs"
        Path(static_dir).mkdir(exist_ok=True)
        local_urls = dict([_download_resource(url, static_dir) for url in HEADER_URLS.items()])
        return self._create_headers(local_urls, mode=mode, daisy=daisy, highlightjs=highlightjs)
