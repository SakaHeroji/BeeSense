"""Optional daily quotas for the pinned Scweet account repository.

Scweet's public config requires positive integers. Nullable application quotas
are applied to its repository queries, preserving status, cooldown, lease and
authentication predicates. Usage counters remain intact.
"""

import time
from collections import Counter


def configure_daily_quotas(client, request_limit, tweet_limit):
    from Scweet.repos import AccountsRepo
    from Scweet.schema import AccountTable
    from Scweet.storage import session_scope
    from sqlalchemy import and_, func, or_, select, true
    from sqlalchemy.sql.visitors import iterate

    def columns(clause):
        return {getattr(part, "name", None) for part in iterate(clause)}

    class OptionalDailyQuotas(AccountsRepo):
        def _eligible_clauses(self, now_ts):
            clauses = super()._eligible_clauses(now_ts)
            quotas = []
            if request_limit is not None:
                quotas.append(
                    func.coalesce(AccountTable.daily_requests, 0) < request_limit
                )
            if tweet_limit is not None:
                quotas.append(func.coalesce(AccountTable.daily_tweets, 0) < tweet_limit)
            replacements = 0
            for index, clause in enumerate(clauses):
                if {"daily_requests", "daily_tweets"} <= columns(clause):
                    from Scweet.repos import _today_string

                    clauses[index] = or_(
                        AccountTable.last_reset_date.is_(None),
                        AccountTable.last_reset_date != _today_string(),
                        and_(*quotas) if quotas else true(),
                    )
                    replacements += 1
            if replacements != 1:
                raise RuntimeError("Unsupported Scweet daily quota predicates")
            return clauses

        def eligibility_diagnostics(self, now_ts=None, sample_limit=5):
            # Evaluate the same predicates used by acquire_leases, without reading
            # tokens/cookies into application diagnostics or resetting counters.
            clauses = self._eligible_clauses(now_ts or time.time())
            reasons = []
            names = {
                "daily_requests": "daily_limit",
                "daily_tweets": "daily_limit",
                "last_reset_date": "daily_limit",
                "lease_id": "leased",
                "available_til": "cooldown",
                "auth_token": "missing_auth_token",
                "csrf": "missing_csrf",
                "cookies_json": "missing_cookies",
                "bearer": "missing_bearer",
                "status": "status",
            }
            for clause in clauses:
                reasons.append(
                    next(
                        (
                            label
                            for col, label in names.items()
                            if col in columns(clause)
                        ),
                        "account_rule",
                    )
                )
            with session_scope(self.db_path) as session:
                rows = session.execute(
                    select(
                        AccountTable.id,
                        AccountTable.available_til,
                        *(
                            clause.label("rule_" + str(i))
                            for i, clause in enumerate(clauses)
                        ),
                    )
                ).all()
            blocked_counts, samples, eligible = Counter(), [], 0
            for row in rows:
                blocked = list(
                    dict.fromkeys(
                        reason for reason, passes in zip(reasons, row[2:]) if not passes
                    )
                )
                if not blocked:
                    eligible += 1
                    continue
                blocked_counts.update(blocked)
                if len(samples) < sample_limit:
                    samples.append(
                        {"id": row[0], "available_til": row[1], "reasons": blocked}
                    )
            return {
                "total": len(rows),
                "eligible": eligible,
                "blocked_counts": dict(blocked_counts),
                "blocked_samples": samples,
            }

    old = client._accounts_repo
    repo = OptionalDailyQuotas(
        old.db_path,
        lease_ttl_s=old.lease_ttl_s,
        daily_pages_limit=old.daily_pages_limit,
        daily_tweets_limit=old.daily_tweets_limit,
        require_auth_material=old.require_auth_material,
        default_bearer_token=old.default_bearer_token,
    )
    client._accounts_repo = repo
    client._runner.accounts_repo = repo
    client._api_engine.accounts_repo = repo
