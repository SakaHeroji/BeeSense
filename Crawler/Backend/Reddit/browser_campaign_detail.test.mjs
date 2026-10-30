import {test} from 'node:test';
import assert from 'node:assert/strict';
import {classifyCaptureFailure, rateLimitSeconds} from './browser_campaign_detail.mjs';

test('Chrome client block is distinguished from Reddit access challenge', () => {
  assert.equal(classifyCaptureFailure('www.reddit.com is blocked\nThis page has been blocked by Chrome\nERR_BLOCKED_BY_CLIENT'), 'CLIENT_BROWSER_BLOCK');
  assert.equal(classifyCaptureFailure('Verify you are human. Complete the CAPTCHA.'), 'ACCESS_BARRIER');
});
test('unrecognized browser failure does not claim the source post is missing', () => {
  assert.equal(classifyCaptureFailure(''), 'BROWSER_CAPTURE_ERROR_UNVERIFIED');
  assert.equal(classifyCaptureFailure('Something went wrong'), 'BROWSER_CAPTURE_ERROR_UNVERIFIED');
});
test('read the cooldown actually shown by Reddit', () => {
  assert.equal(rateLimitSeconds('Your request has been rate limited, please take a break for 246 seconds and try again.'), 246);
  assert.equal(rateLimitSeconds('Sign Up Log In'), null);
});
