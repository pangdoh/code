import subprocess


def eval_js(js):
    try:
        node = subprocess.Popen(
            ["node", "-e", js], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, encoding='utf-8'
        )
        result, stderr = node.communicate()
        if node.returncode != 0:
            stderr = "Node.js Exception:\n%s" % (stderr or None)
            raise subprocess.CalledProcessError(node.returncode, "node -e ...", stderr)
    except OSError as e:
        if e.errno == 2:
            environmenterror = "Missing Node.js runtime. Node is required and must be in the PATH \
            (check with `node -v`). Your Node binary may be called `nodejs` rather than `node`, \
            in which case you may need to run `apt-get install nodejs-legacy` on some \
            Debian-based systems. (Please read the cfscrape.\
             README's Dependencies section: https://github.com/Anorov/cloudflare-scrape#dependencies."
            result = environmenterror
    except Exception as e:
        result = e
    finally:
        return result


filename = "nodejs/browser.js"
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
    res = eval_js(content)

    print(res)
