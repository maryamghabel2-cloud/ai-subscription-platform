# Web3 Wallet Authentication and Identity

**Version:** v0.1.0

**Date:** 2026-07-24

**Status:** Proposed Architecture - Pending Owner, Security, Privacy, and
Compliance Approval

**Document Owner:** Security Architect / Identity

**Purpose:** Define wallet login as optional authentication method alongside
email and phone, with principles, chain support phases, separation from
payments, privacy, security, recovery, and compliance.

**Note:** Documentation only. No blockchain transactions, no platform token,
no secrets.

## Purpose

Define how Web3 wallet authentication will be supported as optional login
method alongside email and phone, with secure nonce challenge, domain binding,
and separation from payments.

## In Scope

- Decision to support wallet login as optional authentication method
- Supported identity methods: email, phone, wallet
- Wallet login principles, chain support phases, separation from payments,
  privacy, security, recovery, compliance

## Out of Scope

- Actual wallet authentication implementation and blockchain transaction code
  (future, reviewed)
- Platform token creation, DeFi interactions, payment signatures (explicitly out
  of scope for early phases)
- Final recovery method and compliance review (future PRs)

## Decision

Wallet login will be supported as an optional authentication method alongside
email and phone authentication.

- Wallet authentication must not replace all other login methods
- Email and Phone authentication remain primary methods
- Wallet authentication is optional, not forced, user choice
- Users may link multiple authentication methods for flexibility and recovery

## Supported Identity Methods

- **Email authentication:**
  - Existing method, password hashing bcrypt with pre-hash, opaque session
    tokens HttpOnly, Secure, SameSite, CSRF, refresh rotation
  - Email verification required for new accounts, rate limiting

- **Phone authentication:**
  - Optional method, OTP via SMS or voice, rate limiting, no long-term storage
    of phone numbers unless explicitly needed, privacy-aware

- **Wallet authentication:**
  - Optional method, uses signed nonce challenge, domain binding, timestamp and
    expiration, prevents replay attacks, stores only wallet address and
    verification metadata required for login
  - Must not replace all other login methods, must coexist with email and phone

## Wallet Login Principles

- Never ask for seed phrase or private key: platform must never ask user for
  seed phrase, private key, mnemonic, or keystore password
- Use signed nonce challenge: server generates random nonce, one-time use,
  expires after CONFIGURED_WALLET_SIGNATURE_EXPIRY, client signs nonce with wallet private key
  off-chain, server verifies signature server-side
- Bind signature to domain: signed message includes domain (e.g.,
  ai-subscription-platform.com), prevents phishing and replay across domains
- Include timestamp and expiration: signed message includes issued_at and
  expiration (e.g., CONFIGURED_NONCE_EXPIRATION), prevents old signatures reuse
- Prevent replay attacks: nonce one-time use, stored as used after verification,
  expires after short time, same nonce cannot be reused, same signature cannot
  be reused for different domain or different timestamp
- Store only wallet address and verification metadata required for login:
  wallet address (e.g., 0x..., or TON address), chain id, verification timestamp,
  last login, no private key, no seed phrase, no signature stored long-term
- Allow users to link and unlink wallets: user can link wallet to existing
  email/phone account, or create account with wallet only, or unlink wallet
  with re-authentication, link and unlink actions require re-authentication
- Support multiple linked wallets where appropriate: user may link EVM and TON
  wallets, or multiple EVM wallets, each verified separately, primary wallet
  for display, all linked wallets can be used for login

## Chain Support Phases

### Phase 1

- EVM-compatible wallet authentication using Sign-In with Ethereum style signed
  messages (EIP-4361 style)
- Message format: domain, address, statement, uri, version, chain_id, nonce,
  issued_at, expiration
- Signature verification server-side using EVM ecrecover
- Chain id verification, domain binding enforced, timestamp and expiration
  enforced, nonce one-time use and expiration enforced
- Supported wallets: MetaMask, WalletConnect-compatible, Rabby, etc. (examples,
  not permanent allowlist, use generic EVM wallet)

### Phase 2

- TON wallet authentication using TON Connect style proof (ton_proof)
- Message format: TON Connect proof with domain, payload, timestamp, etc.
- Signature verification server-side using TON signature verification
- Domain binding, timestamp, expiration, nonce one-time use
- Supported wallets: Tonkeeper, MyTonWallet, etc. (examples, not permanent)

### Phase 3

- Other chains only after security and demand review: e.g., Solana, Bitcoin
  via custom message signing, only if demand and security review pass, owner
  approval required, legal and compliance review required, no new chain without
  explicit approval

## Supported Crypto Payment Networks (Phase 1)

The platform will support the following networks for USDT and USDC top-up:

- TRON (TRC20) – most common in Iranian market
- BSC (BEP20) – significantly lower fees than TRON
- Polygon – very low fees
- Base – low fees, Coinbase L2
- TON – lowest fees, native Telegram integration

USDC will be supported alongside USDT on all listed networks.

Wallet Login (EVM) will cover BSC, Polygon, Base, and Ethereum with a single
Sign-In implementation.

TON uses TON Connect proof.

Explicit statement: Wallet login is for identity only. It does not grant any
payment authorization, fund movement, or DeFi permission. Separate explicit user
consent is required for any on-chain transaction.

## Separation from Payments

- Wallet login is strictly for identity verification and does not grant any
  payment, withdrawal, or DeFi authorization.
- Connecting a wallet for login does not allow the platform to initiate any
  on-chain transaction.
- Wallet login is identity, not payment authorization: connecting a wallet does
  not allow the platform to move funds, no allowance, no approval for spending,
  no withdrawal, no DeFi authorization
- Connecting a wallet does not allow the platform to move funds: no transfer,
  no approve, no permit, no transaction signing for payment without separate
  explicit user consent and separate signature, no on-chain transaction
  initiation
- Payment signatures and login signatures are separate: login uses signed nonce
  challenge with domain binding, payment uses separate transaction signature
  with amount, recipient, chain id, and explicit user confirmation in wallet UI
- DeFi interactions are out of scope for early phases: no DeFi, no staking, no
  swapping, no lending, no liquidity provision, no token approval for DeFi
  protocols
- A platform token is explicitly out of scope: do not create a platform token,
  do not implement blockchain transactions for token issuance, do not create
  tokenomics, do not promise token airdrop, no token

## Privacy

- Wallet addresses are pseudonymous, not anonymous: wallet address is
  pseudonymous identifier, public blockchain activity may be linkable to address
  via explorers, users must be informed
- Public blockchain activity may be linkable: transactions, balances, NFTs,
  token holdings may be visible on public explorers, linkable to address, may
  reveal identity patterns if address reused
- Clear warning: Public blockchain activity may be linkable even if the user
  logs in via wallet. Users must be warned that blockchain explorers may link
  their wallet address to public transactions, balances, NFTs, ENS names, and
  token holdings, even when using wallet login for identity.
- Users must be informed that wallet login can reduce platform-collected
  identity data (e.g., less email/phone needed) but may expose blockchain-linked
  identity patterns (e.g., public transactions, ENS name, NFT holdings)
- Wallet login should be optional, not forced: user choice, email and phone
  remain available, user can link multiple methods, can unlink wallet with
  re-authentication, can use email/phone only if prefers
- No permanent IP tracking for wallet login, no device fingerprinting by default,
  privacy-preserving abuse controls, additional tracking signals require Privacy,
  Security, Legal, Owner approval

## Security

- Nonce must be one-time use: store nonce as used after verification, prevent
  replay, same nonce cannot be used twice, even for same address
- Nonce must expire: e.g., CONFIGURED_NONCE_EXPIRATION, short-lived, e.g.,
  CONFIGURED_WALLET_SIGNATURE_EXPIRY, after expiration signature invalid
- Signature verification must happen server-side: never trust client-side
  verification, always verify server-side with library, check domain, timestamp,
  expiration, nonce, chain id, address
- Domain binding must be enforced: signed message must include expected domain
  (e.g., ai-subscription-platform.com), server must verify domain matches,
  prevents phishing and replay across domains
- Session creation must use existing secure cookie/session architecture:
  opaque session tokens HttpOnly, Secure, SameSite, CSRF, refresh rotation,
  CONFIGURED_WALLET_SESSION_LIFETIME session, CONFIGURED_WALLET_LINK_RETENTION refresh, get_client_ip only trusts X-Forwarded-For if
  in TRUSTED_PROXIES
- Wallet link and unlink actions require re-authentication: user must be logged
  in via existing method (email/phone/other wallet) and re-authenticate before
  linking or unlinking wallet, prevents account takeover via wallet link
- Suspicious wallet login attempts must be visible to the Security Agent:
  authentication failure rate above CONFIGURED_LIMIT, unusual wallet login
  pattern, multiple failed verifications, admin action outside business hours,
  cross-user data access attempt, detection signals, audit logging with metadata
  only, no raw sensitive content, content_fingerprint DISABLED_BY_DEFAULT

## Recovery

- A wallet-only user may lose access if the wallet is lost (private key lost,
  seed phrase lost, wallet app uninstalled without backup)
- Recovery for wallet-only accounts is an Open Decision.
- Users should be strongly encouraged to link at least one recovery method
  (email or phone) if they choose wallet-only login.
- Wallet-only accounts carry higher recovery risk. Users are strongly encouraged
  to link at least one traditional recovery method (email or phone).
  Wallet-only recovery is an Open Decision and will be designed with
  multi-signature or social recovery options in future phases. Users must be
  clearly warned during wallet-only signup about permanent loss risk if the
  wallet is lost or compromised.
- Recovery method is an Open Decision: e.g., email recovery if linked, phone
  recovery if linked, social recovery, multi-wallet, admin-assisted recovery
  with human approval and audit, no automatic recovery without re-authentication
- Users should be encouraged to link at least one recovery method if they want
  account recovery: e.g., link email or phone or second wallet, onboarding
  should explain risk of wallet-only account and encourage linking recovery
  method, but not forced
- No seed phrase or private key storage by platform, never ask for seed phrase

## Compliance

- Wallet login does not imply KYC: wallet authentication is not KYC, does not
  verify real-world identity, does not replace KYC if required for certain
  features (e.g., fiat payments, high-value transactions)
- Crypto payment, DeFi, token issuance, and revenue distribution require separate
  legal and compliance review: ZarinPal and crypto payment verification are
  separate from wallet login, DeFi interactions out of scope, platform token out
  of scope, token issuance and revenue distribution require legal, tax, KYC,
  finance, owner approval
- The product must not present wallet login as a way to evade law, sanctions,
  KYC, or provider rules: no bypassing sanctions, geographic restrictions, KYC,
  no using wallet login to hide prohibited end-user locations, no claiming
  professional authority, no evasion of law

## Related Documents

- Security Index: [../security/README.md](../security/README.md)
- Identity and Access Control: [../security/IDENTITY_AND_ACCESS_CONTROL.md](../security/IDENTITY_AND_ACCESS_CONTROL.md)
- Secrets and Key Management: [../security/SECRETS_AND_KEY_MANAGEMENT.md](../security/SECRETS_AND_KEY_MANAGEMENT.md)
- Security Agent Runtime: [../security/SECURITY_AGENT_RUNTIME.md](../security/SECURITY_AGENT_RUNTIME.md)
- Data Protection: [../security/DATA_PROTECTION_AND_ENCRYPTION.md](../security/DATA_PROTECTION_AND_ENCRYPTION.md)
- Channel Security: [../security/CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md](../security/CHANNEL_SECURITY_TELEGRAM_WEB_MOBILE.md)
- Wallet and Payments: WALLET_AND_PAYMENTS.md (planned, future - not clickable yet)

## Open Decisions

- Exact nonce format, length, expiration CONFIGURED_NONCE_EXPIRATION, storage
  and one-time use enforcement
- Domain binding exact message format and verification library
- Chain support phases exact wallets and libraries and rollout
- Recovery method for wallet-only users (Open Decision, requires security,
  privacy, legal, owner approval)
- Compliance review for wallet login and crypto payment and DeFi and token
- Owner, security, privacy, legal, compliance approval required for all decisions

## Planned Completion Stage

Phase 1 - Wallet Authentication (EVM), Phase 2 - TON, Phase 3 - Other chains after
review

## Status Note

Proposed Architecture - Pending Owner, Security, Privacy, and Compliance Approval.
This document is proposed architecture. It does not prove that the described controls, integrations, providers, wallet-login flows, MCP exposure, or search behavior are implemented, tested, deployed, or production-ready. Implementation requires separate code, tests, configuration, owner approval, and security review. No blockchain
transactions, no platform token, no secrets in this PR.
