#!/usr/bin/env python
import sys
import os
import shutil
import markdown
import codecs
import re


class Article:
    title = ""
    html = ""
    standalone_target_name = ""


def print_help():
    print "no help yet"
    

def strip_extension(filename):
    return os.path.splitext(filename)[0]
    
    
def replace_extension(filename, new_extension):
    return strip_extension(filename) + new_extension


def prolog(source_dir):
    filename = os.path.join(source_dir, "prolog")
    if os.path.isfile(filename):
        return read_utf8(filename)
    else:
        return '<html><head><meta http-equiv="Content-Type" content="text/html;charset=utf-8"></head>'
    
    
def epilog(source_dir):
    filename = os.path.join(source_dir, "epilog")
    if os.path.isfile(filename):
        return read_utf8(filename)
    else:
        return "</html>"


def read_utf8(filename):
    with codecs.open(filename, mode="r", encoding="utf-8") as f:
        return f.read()


def write_utf8(filename, text):
    with codecs.open(filename, 'w', encoding="utf-8", errors="xmlcharrefreplace") as f:
        f.write(text)


def compile_markdown(source_name):
    md = read_utf8(source_name)
    html = markdown.markdown(md, extensions=['codehilite'])
    return html


def shall_copy(name):
    for ext in [".jpg", ".css"]:
        if name.endswith(ext): return True                
    return False
    

def is_special_filename(filename):
    return (filename == "prolog"
         or filename == "epilog")


def filename_to_title(f):
    return re.sub(ur"(\w)([A-Z])", ur"\1 \2", strip_extension(f))


def compose(articles, source_dir, target_name):
    body = ""
    index = ""
    for a in articles:
        index += u'<li><a href="#{0}">{0}</a></li>'.format(a.title)
        body += (u'<article>' +
                 u'<a name="{0}" href="{2}"><h1>{0}</h1></a>' +
                 u'{1}' +
                 u'<a href="#index">top</a>'
                 u'</article>' +
                 u'\n'
                ).format(a.title, a.html, os.path.basename(a.standalone_target_name))

    index = u'<a name="index"></a><ul>{0}</ul>'.format(index)
    html = prolog(source_dir)
    html += u'<h1><a href="{1}">{0}</a></h1>'.format(
                    filename_to_title(os.path.basename(source_dir)),
                    os.path.dirname(target_name))
    if len(articles) > 1:
        html += index
    html += body
    html += epilog(source_dir)
    write_utf8(target_name, html)
    
    # Also create standalone articles
    if len(articles) > 1:
        for a in articles:
            compose([a,], source_dir, a.standalone_target_name)


def build_recursively(source_dir, target_dir):
    print "building {0} -> {1}".format(source_dir, target_dir)
    if not os.path.isdir(target_dir):
        try:
            os.mkdir (target_dir)
        except OSError:
            print "error:cannot create target directory {0}".format(target_dir)
            return

    articles = []
    for f in os.listdir(source_dir):
        if is_special_filename(f):
            continue

        source_name = os.path.join(source_dir, f)
        target_name = os.path.join(target_dir, f)

        if os.path.isdir(source_name):
            build_recursively(source_name, target_name)
        elif os.path.isfile(source_name):
            if source_name.endswith(".md"):
                article = Article()
                article.html = compile_markdown(source_name)
                article.title = filename_to_title(f)
                article.standalone_target_name = replace_extension(target_name, ".html")
                articles.append(article)
            elif shall_copy(source_name):
                try:
                    shutil.copyfile(source_name, target_name)
                except IOError:
                    print "error:cannot copy {0} as {1}".format(source_name, target_name) 
                    return
            else:
                print "warning:unrecognized filename extension (ignoring): {0}".format(source_name)

    compose(articles, source_dir, os.path.join(target_dir, "index.html"))


def build (source_dir, target_dir, flags):
    if not os.path.isdir(source_dir):
        print "{0} doesn't exist."
        return    
    if os.path.isdir(target_dir) and (os.listdir(target_dir) != []) and (not "-f" in flags):
        print "error:target directory isn't empty. use -f to override"
        return
    build_recursively(source_dir, target_dir)


print "whew."
if len(sys.argv) <= 1:
    print_help()
    exit()
if sys.argv[1] == 'build':
    if len (sys.argv) < 4:
        print_help()
        exit()
    build(sys.argv[2], sys.argv[3], sys.argv[4:])
    

