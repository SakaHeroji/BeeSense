export function captureRenderedThread({nativeId, maxComments = 2000}) {
  const element = Array.from(document.querySelectorAll('shreddit-post')).find(post => post.id === 't3_' + nativeId);
  const banner = Array.from(document.querySelectorAll('[role="banner"], header')).map(item => item.innerText).join('\n');
  const page = {page_url: location.href, page_title: document.title,
    barrier_text: element ? banner : (document.body?.innerText || '').slice(0, 20000)};
  if (!element) return {...page, post: null, comments: []};
  const post = {
    native_id: nativeId, title: element.getAttribute('post-title'),
    text: element.querySelector('[id="' + element.id + '-post-rtjson-content"]')?.innerText ||
      Array.from(element.querySelectorAll('p')).map(p => p.innerText).join('\n\n'),
    published_at: element.getAttribute('created-timestamp'), permalink: element.getAttribute('permalink'),
    subreddit: element.getAttribute('subreddit-name'), post_type: element.getAttribute('post-type'),
    score_display: element.getAttribute('score'), comment_count_display: element.getAttribute('comment-count'),
    source_show_full_content: element.hasAttribute('show-full-content'),
  };
  const comments = Array.from(document.querySelectorAll('[role="article"]')).slice(0, maxComments).map(article => {
    const own = selector => Array.from(article.querySelectorAll(selector)).filter(child => child.closest('[role="article"]') === article);
    const link = own('a[href*="/comment/"]')[0];
    const commentId = link?.href.match(/\/comment\/([a-z0-9]+)\//)?.[1];
    const body = commentId ? article.querySelector('[id="t1_' + commentId + '-post-rtjson-content"]') : null;
    const parent = article.parentElement?.closest('[role="article"]');
    const parentLink = parent ? Array.from(parent.querySelectorAll('a[href*="/comment/"]')).find(child => child.closest('[role="article"]') === parent) : null;
    return {url: link?.href || null, parent_url: parentLink?.href || null,
      text: body?.innerText || own('p').map(p => p.innerText).join('\n\n'),
      published_at: own('time')[0]?.getAttribute('datetime') || null,
      published_display: own('time')[0]?.innerText || null};
  }).filter(row => row.url && row.text);
  return {...page, post, comments};
}
