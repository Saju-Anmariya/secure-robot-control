# Security report: secure-robot-control

**Scope:** a simulated robot control API, tested locally against my own code.
**Method:** build an insecure v1, attack it, fix the findings in v2, re-run the
same attacks and add automated tests.

## Threat model

An attacker on the network can send requests to the API, can observe legitimate
traffic between operator and robot (and therefore capture and resend messages),
and can try to send requests as fast as possible. The attacker does not know the
shared secret.

## Findings in v1 and fixes in v2

| ID | Finding | Severity | Fix in v2 | Evidence |
|---|---|---|---|---|
| F1 | No authentication: anyone can command the robot | High | Every command must carry a valid HMAC signature | attack 1: 401 |
| F2 | No integrity protection: messages can be modified | High | Signature covers the action, so a changed action fails | attack 4: 401 "bad signature" |
| F3 | Replay: a captured valid command can be re-sent | High | Timestamp (30 s window) and one-time nonce | attack 2: 401 "replay detected" |
| F4 | No rate limiting: unlimited commands per second | Medium | 20 requests per 10 s per IP, checked first | attack 3: 287 of 300 blocked |
| F5 | No logging: attacks leave no trace | Medium | Every rejection logged with IP and reason | `security.log` |

## Design decisions

- The secret is loaded from an environment variable or a git-ignored file and is
  never in the code or repository history.
- Signatures are compared with `hmac.compare_digest` to avoid timing leaks.
- The rate limit runs before authentication, so floods are cheap to reject.
- A nonce is stored only after its signature is valid, so unauthenticated
  traffic cannot exhaust memory.
- The attack order matters: the flood attack runs last. While the rate limiter
  is active it rejects everything, which would hide whether the other defenses
  work (an early run showed this: tampering was blocked by the rate limiter and
  not by the signature check).

## Residual risks

1. **No TLS.** Signatures protect integrity and authenticity, not secrecy; an
   eavesdropper can still read commands. Production needs HTTPS.
2. **Shared secret.** One key for all operators; no per-user identity or
   revocation. A real system would use per-client keys or mTLS.
3. **In-memory state.** Rate limits and nonces live in one process and reset on
   restart; they do not work across several server instances (use Redis or similar).
4. **IP-based rate limiting** can be bypassed from many addresses and can punish
   users behind a shared NAT.
5. **`/state` is unauthenticated** read-only telemetry. It leaks the robot's
   position and should be protected in a real deployment.
6. **No key rotation** and no alerting beyond the log file.

## Next steps

Add HTTPS, per-client keys with rotation, protect `/state`, move nonce and rate
limit storage to Redis, and alert on repeated rejections.
