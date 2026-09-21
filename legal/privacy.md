# Privacy Policy

**DRAFT, 2026-09-21. Not yet reviewed by counsel. Bracketed items must be filled in before publication.**

Effective date: [date]

buddy is made by [Company legal name] ("we", "us"). This policy explains what buddy collects, why, where it goes, and what you can do about it. buddy is unusual: it operates a computer on your behalf, so it sees and stores more than a typical web app. We have tried to say exactly what that means rather than hide it in general language.

## What buddy is

buddy gives you a computer in the cloud (a virtual machine we run for you) and an AI agent that uses it at your direction. You can watch the computer's screen, take over the mouse and keyboard, and hand it back. buddy can also connect to services you authorize (email, calendars, project tools) and act in them for you.

## What we collect

**Account information.** Your email address, display name, and sign-in method (email and password, or Google sign-in). Passwords are handled by our authentication provider, Supabase; we never see them.

**Your conversations and buddy's work.** Everything you type to buddy, everything buddy says, and a record of every action buddy takes (each tool call and its result). We keep this as a complete transcript for each session. It is the record of what buddy did for you and is how you can review its work.

**Your files.** Files you upload, files buddy creates, and the contents of folders you link. These are stored in our storage bucket and mirrored to your cloud computer.

**Your computer's screen.** While your cloud computer is awake, we capture its screen continuously so you can watch it and so buddy can see what it is doing. Frames are retained for [retention period] and then deleted, except frames kept inside a session transcript so buddy can refer back to what it saw.

**Your input during takeover.** When you take over the computer, your mouse and keyboard input passes through our servers to the computer. We may record takeover sessions (screen and input) so that buddy can learn how you use an application. Keystrokes typed into password fields are not recorded.

**Logins on your cloud computer.** If you sign in to a website inside your cloud computer, that site's cookies and session are stored in the computer's browser profile, the same as on your own machine. We back up your cloud computer's disk, including that browser profile, so that your computer can be restored if it is lost. Those backups are stored in our storage bucket and are protected by the storage provider's encryption at rest. We do not have a separate encryption key per user at this time.

**Connected services.** When you connect a service such as Gmail or Google Drive, you authorize buddy through OAuth. The access tokens are held by our integration provider, Composio, not by us. We store the fact that the connection exists and buddy's actions within the service appear in your transcripts.

**Usage and billing.** How long buddy spends working for you, how long your cloud computer is awake, and how much storage you use. If you buy a plan or credits, payment is handled by Stripe; we store a customer identifier and your entitlement, never your card.

**Technical information.** IP address, browser type, and operational logs needed to run the service. Operational logs are deleted after 30 days.

## How we use it

To provide buddy: run your computer, carry out your instructions, show you what happened, and restore your computer if it is lost. To bill you. To keep the service secure and to investigate abuse. To improve buddy, using aggregate statistics that do not identify you.

**We do not use your conversations, files, screen recordings or takeover recordings to train AI models unless you explicitly opt in.** If we ever offer that, it will be a separate, clearly labeled choice, off by default.

## Where your data goes

**AI model providers.** To do its work, buddy sends the content of your session to a large language model. That content can include your messages, screenshots of your cloud computer, and the contents of files buddy reads. Our current model provider is [provider name]. Providers process this data under their own terms; we use providers that do not train on API data.

**Infrastructure.** Supabase (database, storage, authentication), [E2B or current provider] (cloud computers), Composio (service connections), Stripe (payments), Postmark (account email), Vercel (this website). Each is a processor acting on our instructions.

**Third-party services you connect.** When buddy acts in a service on your behalf, that service receives whatever buddy sends it (an email, a form, a file), exactly as if you had done it.

**Google user data.** buddy's use of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements. We use Google user data only to provide the features you ask for, never for advertising, and never sell it.

We do not sell personal information. We do not share it with advertisers.

## How long we keep it

Account information: until you delete your account. Transcripts and files: until you delete them or your account. Screen frames: [retention period]. Cloud computer backups: the two most recent. Operational logs: 30 days. Billing records: as required by law after account deletion.

## Your choices

You can delete individual sessions and files at any time from within buddy. You can disconnect any connected service. You can delete your account, which removes your account information, transcripts, files, screen recordings, cloud computer and its backups within [30] days, except billing records we must retain. You can request an export of your transcripts and files. To do either, email [privacy@trybuddynow.com].

If you are in the European Economic Area, the United Kingdom, or California, you have additional rights to access, correct, delete and port your data, and to object to certain processing. Use the same address.

## Security

Data is encrypted in transit. Storage is encrypted at rest by our providers. Access to production systems is limited to [Company] staff who need it. Your cloud computer is isolated from other users' computers. If we learn of a breach affecting your data, we will notify you at your account email without undue delay.

## Cookies

buddy uses one cookie: a session cookie that keeps you signed in. It is strictly necessary for the service and is not used for tracking. Stripe sets its own cookies during checkout under Stripe's policy. We do not use analytics or advertising cookies. If that changes we will update this policy and ask for consent where the law requires it.

## Children

buddy is for people 18 and over. We do not knowingly collect data from anyone under 18.

## Changes

We will post changes here and update the effective date. If a change materially reduces your rights, we will email you before it takes effect.

## Contact

[Company legal name], [address]. Privacy questions: [privacy@trybuddynow.com]. Security reports: [security@trybuddynow.com].
