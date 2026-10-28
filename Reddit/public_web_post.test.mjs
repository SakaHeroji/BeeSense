import {test} from 'node:test';
import assert from 'node:assert/strict';
import {parsePublicPost} from './public_web_post.mjs';

const candidate = {native_id:'abc123',title:'Biaya kuliah & beasiswa'};
const header = 'Biaya kuliah & beasiswa : r/indonesia (https://www.reddit.com/r/indonesia/comments/abc123/title/)\ncitetest Crawled: last month; Content type: text/html\n';
test('post section excludes comments and retains cache uncertainty', () => {
  const value=parsePublicPost(header+'L1: # Biaya kuliah & beasiswa\nL2: Teks sumber tentang UKT.\nL3: 【6†Bagikan】\nL4: Komentar tidak boleh masuk ke isi post.',candidate);
  assert.equal(value.text,'Teks sumber tentang UKT.');
  assert.equal(value.cache_note,'last month');
  assert.equal(value.source_capture_time_known,false);
});
test('reject another post or a login page despite a plausible URL', () => {
  assert.equal(parsePublicPost(header.replace('abc123','def456')+'L1: # Biaya kuliah & beasiswa',candidate),null);
  assert.equal(parsePublicPost(header+'L1: # Log In',candidate),null);
});
test('bound excerpts and mark truncated sections', () => {
  const value=parsePublicPost(header+'L1: # Biaya kuliah & beasiswa\nL2: '+Array(250).fill('kata').join(' ')+'\nL3: Share',candidate);
  assert.equal(value.text.split(/\s+/).length,180);
  assert.equal(value.excerpt_truncated,true);
});
test('select the matching post from a multi-page web response', () => {
  const other=header.replaceAll('abc123','def456').replaceAll('Biaya kuliah & beasiswa','Lainnya')+'L1: # Lainnya\nL2: Bukan target\nL3: Share\n';
  const value=parsePublicPost(other+header+'L1: # Biaya kuliah & beasiswa\nL2: Target\nL3: Share\n',candidate);
  assert.equal(value.text,'Target');
});
