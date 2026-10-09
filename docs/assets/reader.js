// Reader for the ТЕНЗОРЫ notes: renders the Markdown files in the browser, no build step.
// Routes: #/ -> README.md (the list of lectures), #/lecture-04 -> lecture-04/lecture-04.md.
// The navigation is whatever README.md links to, in that order.
(function () {
  "use strict";

  const HOME = "README.md";
  const LECTURE_PATH = /^(lecture-\d+)\/\1\.md$/;          // lecture-04/lecture-04.md
  const ROOT = new URL("./", location.origin + location.pathname);

  // Identical configuration to scripts/render_preview.py, so the site shows what the checks saw.
  const md = window.markdownit({ html: true, linkify: false, typographer: false })
    .use(window.texmath, {
      engine: window.katex, delimiters: "dollars",
      katexOptions: { throwOnError: false, strict: false },
    });

  const content = document.getElementById("content");
  const navList = document.getElementById("nav-list");
  const toggle = document.querySelector(".nav-toggle");
  let lectures = [];                                         // [{slug, title, num, name, note}]

  const isExternal = (url) => /^([a-z][a-z0-9+.-]*:|\/\/|\/|#)/i.test(url);
  const rootRelative = (abs) => (abs.href.startsWith(ROOT.href) ? abs.href.slice(ROOT.href.length) : null);

  async function fetchText(path) {
    const res = await fetch(new URL(path, ROOT), { cache: "no-cache" });
    if (!res.ok) throw new Error(`${path}: ${res.status}`);
    return res.text();
  }

  // Render Markdown and fix relative URLs: they are relative to the .md file, not to index.html.
  function render(source, mdPath) {
    const box = document.createElement("div");
    box.innerHTML = md.render(source);
    const base = new URL(mdPath, ROOT);
    box.querySelectorAll("img[src]").forEach((img) => {
      const src = img.getAttribute("src");
      if (!isExternal(src)) img.src = new URL(src, base).href;
      img.loading = "lazy";
      img.decoding = "async";
    });
    box.querySelectorAll("a[href]").forEach((a) => {
      const href = a.getAttribute("href");
      if (isExternal(href)) return;
      const abs = new URL(href, base);
      const rel = rootRelative(abs);
      const m = rel && rel.match(LECTURE_PATH);
      a.href = m ? `#/${m[1]}` : abs.href;
    });
    // "*Рис. N. …*" right after a figure is its caption.
    box.querySelectorAll("p").forEach((p) => {
      const only = p.children.length === 1 && p.firstElementChild.tagName === "EM" && p.textContent.trim() === p.firstElementChild.textContent.trim();
      if (only && /^Рис\.\s*\d/.test(p.textContent.trim())) p.classList.add("figcaption");
    });
    box.querySelectorAll("blockquote").forEach((q) => {
      if (/^Черновик/.test(q.textContent.trim())) q.classList.add("draft");
    });
    return box;
  }

  async function loadNavigation() {
    const box = render(await fetchText(HOME), HOME);
    lectures = [...box.querySelectorAll('a[href^="#/lecture-"]')].map((a) => {
      const title = a.textContent.trim();
      const m = title.match(/^Лекция\s+(\d+)\.\s*(.*)$/);
      const li = a.closest("li");
      const rest = li ? li.textContent.replace(a.textContent, "") : "";
      return { slug: a.getAttribute("href").slice(2), title, num: m ? m[1] : "", name: m ? m[2] : title,
               note: /черновик/i.test(rest) ? "черновик" : "" };
    });
    navList.innerHTML = "";
    for (const l of lectures) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = `#/${l.slug}`;
      a.dataset.slug = l.slug;
      a.innerHTML = `<span class="num"></span><span><span class="name"></span><span class="tag"></span></span>`;
      a.querySelector(".num").textContent = l.num;
      a.querySelector(".name").textContent = l.name;
      a.querySelector(".tag").textContent = l.note;
      if (!l.note) a.querySelector(".tag").remove();
      li.appendChild(a);
      navList.appendChild(li);
    }
    return box;
  }

  function markCurrent(slug) {
    navList.querySelectorAll("a").forEach((a) => {
      if (a.dataset.slug === slug) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  async function pdfLink(slug) {
    const href = `${slug}/${slug}.pdf`;
    try {
      const res = await fetch(new URL(href, ROOT), { method: "HEAD", cache: "no-cache" });
      return res.ok ? new URL(href, ROOT).href : null;
    } catch { return null; }
  }

  function pager(slug) {
    const i = lectures.findIndex((l) => l.slug === slug);
    const nav = document.createElement("nav");
    nav.className = "pager";
    nav.setAttribute("aria-label", "Соседние лекции");
    const link = (l, cls, text) => {
      const a = document.createElement("a");
      a.className = cls; a.href = `#/${l.slug}`; a.textContent = text;
      nav.appendChild(a);
    };
    if (i > 0) link(lectures[i - 1], "prev", `← ${lectures[i - 1].title}`);
    if (i >= 0 && i < lectures.length - 1) link(lectures[i + 1], "next", `${lectures[i + 1].title} →`);
    return nav;
  }

  function show(nodes, title) {
    content.replaceChildren(...nodes);
    document.title = title ? `${title} — Тензоры` : "Тензоры — конспекты лекций";
    window.scrollTo(0, 0);
    content.focus({ preventScroll: true });
    document.body.classList.remove("nav-open");
    toggle.setAttribute("aria-expanded", "false");
  }

  function notFound(what) {
    const p = document.createElement("div");
    p.className = "error";
    p.innerHTML = `<h1>Не найдено</h1><p></p><p><a href="#/">К списку лекций</a></p>`;
    p.querySelector("p").textContent = what;
    show([p], "Не найдено");
  }

  let homeBox = null;
  async function route() {
    const slug = location.hash.replace(/^#\/?/, "").replace(/\/$/, "");
    try {
      if (!homeBox) homeBox = await loadNavigation();
      markCurrent(slug);
      if (!slug) {
        show([...homeBox.cloneNode(true).childNodes], "");
        return;
      }
      if (!/^lecture-\d+$/.test(slug)) return notFound(`Нет такой страницы: ${slug}`);
      const mdPath = `${slug}/${slug}.md`;
      const article = render(await fetchText(mdPath), mdPath);
      const h1 = article.querySelector("h1");
      const pdf = await pdfLink(slug);
      if (h1 && pdf) {
        const links = document.createElement("p");
        links.className = "doc-links";
        links.innerHTML = `<a>PDF</a>`;
        links.firstElementChild.href = pdf;
        h1.after(links);
      }
      show([...article.childNodes, pager(slug)], h1 ? h1.textContent.trim() : slug);
    } catch (err) {
      notFound(`Не удалось загрузить: ${err.message}`);
    }
  }

  toggle.addEventListener("click", () => {
    const open = document.body.classList.toggle("nav-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  window.addEventListener("hashchange", route);
  route();
})();
