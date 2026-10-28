// Parse a bounded post-section excerpt returned by the public web reader.
// This is intentionally not presented as a complete or live thread snapshot.
export function parsePublicPost(text, candidate, wordLimit = 200) {
  const sources = [...text.matchAll(/^[^\n]+ \((https:\/\/(?:www\.)?reddit\.com\/[^\n]+)\)\n(?=[^\n]*cite)/gm)];
  const sourceMatch = sources.find(match => match[1].match(/\/comments\/([a-z0-9]+)\//)?.[1] === candidate.native_id);
  const sourceUrl = sourceMatch?.[1];
  const nativeId = sourceUrl?.match(/\/comments\/([a-z0-9]+)\//)?.[1];
  if (!nativeId || nativeId !== candidate.native_id) return null;
  const nextSource = sources.find(match => match.index > sourceMatch.index);
  text = text.slice(sourceMatch.index, nextSource?.index ?? text.length);
  const lines = text.split('\n').map(line => line.match(/^L\d+:\s?(.*)$/)?.[1]).filter(line => line !== undefined);
  const titleIndex = lines.findIndex(line => /^#\s+/.test(line));
  if (titleIndex < 0) return null;
  const clean = value => value.replace(/【\d+†([^】†]*)(?:†[^】]*)?】/g, '$1').trim();
  const title = clean(lines[titleIndex].replace(/^#\s+/, ''));
  const normalize = value => value.normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
  if (!title || normalize(title) !== normalize(candidate.title)) return null;
  const body = [];
  let boundaryFound = false;
  for (const line of lines.slice(titleIndex + 1)) {
    const value = clean(line);
    if (/^(?:Share|Bagikan|Sort by:|Urutkan menurut:|Add a comment|Tambahkan komentar)$/i.test(value)) {
      boundaryFound = true;
      break;
    }
    body.push(value);
  }
  const fullSection = body.join('\n').trim();
  const budget = Math.max(0, Math.min(180, wordLimit - title.split(/\s+/).length));
  const words = [...fullSection.matchAll(/\S+/g)];
  const endpoint = words.length > budget && budget ? words[budget - 1].index + words[budget - 1][0].length : budget ? fullSection.length : 0;
  return {native_id: nativeId, title, text: fullSection.slice(0, endpoint), source_url: sourceUrl,
    cache_note: text.match(/Crawled:\s*([^;\n]+)/)?.[1] || 'provider cache age unknown',
    excerpt_truncated: words.length > budget || !boundaryFound,
    scope: 'post_section_excerpt_not_complete_thread', comment_extraction: 'not_available_from_this_source',
    source_capture_time_known: false};
}
